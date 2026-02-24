import os

import esoreader
import pandas as pd
import numpy as np

import plotly.express as px
import matplotlib.pyplot as plt
# import plotly.graph_objects as go
import datetime as dt

global eso_data
global df_trnsys_out
global df_air_temperatures
global df_heating_load
global df_cooling_load
global df_fluxes
global df_states
global df_loads
global df_misc
global df_window
global df_ventilation
global df_reference

import subprocess
import argparse
import locale

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def create_diagram(title: str, case: str, variant: str, left_axis_name: str, label1: str,
                   column1: pd.DataFrame, label2: str, column2: pd.DataFrame, label3: str, column3: pd.DataFrame,
                   create_monthly_mean : bool = False, reference_string : str = ""):
    """
    Creates a diagram with given data
    :param title: title of diagram
    :param label1: label of data 1
    :param column1: data 1 to be drawn
    :param label2: label of data 2
    :param column2: data 2 to be drawn
    :param label3: label of data 3
    :param column3: data 3 to be drawn
    """

    stepsize = 8759-1
    timesteps = []

    column2 = column2.shift(1)
    column2.fillna(0, inplace=True)

    for i in range(stepsize):
        timesteps.append(dt.datetime(2021, 1, 1) + dt.timedelta(hours=i))

    df = pd.DataFrame()
    df.insert(0, label1, column1[0:stepsize])
    df.insert(0, label2, column2[0:stepsize])
    df.insert(0, label3, column3[0:stepsize])
    df.insert(0, 'Time', timesteps)
    df = df.fillna(0)   # forward fill

    # print(df)

    fig = px.line(df, x="Time", y=df.columns[1:], template="plotly_white", title=title)

    # Set the name for the Y-axis (left axis)
    fig.update_layout(
        yaxis=dict(
            title=left_axis_name  # Replace with your desired axis name
        )
    )

    test = df.set_index('Time').resample('ME')

    if create_monthly_mean :
        df_monthly_mean = df.set_index('Time').resample('ME').sum()
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
        df_monthly_mean.index = df_monthly_mean.index.strftime('%b')

        try: 
            df_monthly_mean['min'] = df_reference[f"Case{case}_{reference_string}_min"]
            df_monthly_mean['max'] = df_reference[f"Case{case}_{reference_string}_max"]
            df_monthly_mean.to_csv(f"validation_results/Case{case}_{variant}/Case{case}_{variant}_{title}_monthly_mean.tsv", sep="\t", index=True)

            # Neue Figure
            plt.figure(figsize=(10, 6))
            
            # Min/Max als Linien überlagern
            plt.plot(df_monthly_mean['min'].values, linestyle='None', color='black', label='Reference Min', marker='x')
            plt.plot(df_monthly_mean['max'].values, linestyle='None', color='black', label='Reference Max', marker='x')

            # Plot: Mittelwerte als Balken
            ax = df_monthly_mean.drop(columns=['min', 'max']).plot(kind='bar', ax=plt.gca(), width=0.8, legend=True)
        except Exception as e:
            print(f"Could not add reference to '{title}'")

            # Neue Figure
            plt.figure(figsize=(10, 6))
            ax = df_monthly_mean.plot(kind='bar', ax=plt.gca(), width=0.8, legend=True)


        plt.title(f'{title} | case {case} {variant}')
        plt.xlabel('Month')
        plt.ylabel(f'{title}')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Legende aktualisieren
        plt.legend()

        # PDF speichern
        plt.savefig(f"validation_results/Case{case}_{variant}/Case{case}_{variant}_{title}_monthly_mean.svg", format='svg')
        plt.close()

        df_monthly_integral = df.set_index('Time').resample('ME').sum()
        df_monthly_integral.index = df_monthly_integral.index.strftime('%Y-%m-%d %H:%M')
        df_monthly_integral.to_csv(f"validation_results/Case{case}_{variant}/Case{case}_{variant}_{title}_monthly_integral.tsv", sep="\t", index=True)

        df_monthly_max = df.set_index('Time').resample('ME').max()
        df_monthly_max.index = df_monthly_max.index.strftime('%Y-%m-%d %H:%M')
        df_monthly_max.to_csv(f"validation_results/Case{case}_{variant}/Case{case}_{variant}_{title}_monthly_max.tsv", sep="\t", index=True)


    df.to_csv(f"validation_results/Case{case}_{variant}/Case{case}_{variant}_{title}.tsv", sep="\t", index=False)
    # fig.write_image(f"validation_results/{title}.pdf")
    # fig.show()


def filter_column(df: pd.DataFrame, containing_string: str) -> pd.Series:
    try:
        cols = [col for col in df.columns if containing_string in col]
        assert (len(cols) == 1)
        return df[[cols[0]]]
    except Exception as e:
        raise Exception(f"{bcolors.FAIL}Could not find variable '{containing_string}' in '{','.join(df.columns)}'")


def read_data(nandrad_directory: str, eso_file: str, trnsys_result_file: str, reference_file: str):
    # read eso file
    global eso_data
    eso_data = esoreader.read_from_path(eso_file)

    # read trnsys data
    global df_trnsys_out
    df_trnsys_out = pd.read_csv(trnsys_result_file, encoding='latin1', delim_whitespace=True)
    df_trnsys_out = df_trnsys_out.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # read nandrad folder
    global df_air_temperatures
    df_air_temperatures = pd.read_csv(f"{nandrad_directory}/results/AirTemperature-Hourly.tsv", sep='\t')

    global df_cooling_load
    df_cooling_load = pd.read_csv(f"{nandrad_directory}/results/IdealCoolingLoad-mean-Hourly.tsv", sep='\t')

    global df_heating_load
    df_heating_load = pd.read_csv(f"{nandrad_directory}/results/IdealHeatingLoad-mean-Hourly.tsv", sep='\t')

    global df_window
    df_window = pd.read_csv(f"{nandrad_directory}/results/WindowOutputs.tsv", sep='\t')

    global df_ventilation
    df_ventilation = pd.read_csv(f"{nandrad_directory}/results/VentilationHeatLoad-mean-Hourly.tsv", sep='\t')
    
    global df_reference
    df_reference = pd.read_csv(reference_file, sep='\t')
    df_reference.set_index('Month', inplace=True)


def validate(title: str, left_axis_name: str, df: pd.DataFrame, nandrad_string: str,
             energy_plus_string: str, key: str = "", trnsys_string: str = "",
             conversion_nandrad: float = 1.0, conversion_energy_plus: float = 1.0, conversion_trnsys: float = 1.0, variant: str = "", case: str = "",
             substract: str = "", substract_key: str = "", substract_conversion: float = 1.0,
             create_monthly_mean : bool = False, unit : str = "", reference_string : str = ""):
    try:
        # first we compare the window
        df_nandrad = filter_column(df, nandrad_string)

        if df_nandrad.empty:
            raise Exception(f"Could not find NANDRAD variable '{nandrad_string}'")

        # filter energy plus data
        df_energy_plus = eso_data.to_frame(energy_plus_string, frequency="hourly", key=key)

        if df_energy_plus.empty:
            raise Exception(f"Could not find EnergyPlus variable '{energy_plus_string}' and key '{key}'")

        if len(substract) != 0:
            df_energy_plus_substract = eso_data.to_frame(substract, frequency="hourly", key=substract_key)
            if df_energy_plus_substract.empty:
                raise Exception(f"Could not substract EnergyPlus variable '{substract}'")
            df_energy_plus[key] = df_energy_plus.values - substract_conversion * df_energy_plus_substract.values

        # Fit correct time step
        # df_energy_plus = df_energy_plus.iloc[1:, ]
        df_trnsys = df_trnsys_out[trnsys_string][1:]
        df_trnsys = df_trnsys.apply(pd.to_numeric, errors="coerce")  # ersetzt nicht-konvertierbares mit NaN

        # Create diagram
        print(f"{bcolors.OKBLUE}Generate validation data '{title}'")
        create_diagram(title, case, variant, left_axis_name,
                       f"NANDRAD [{unit}]", conversion_nandrad * df_nandrad,
                       f"EnergyPlus [{unit}]", conversion_energy_plus * df_energy_plus,
                       f"TRNSYS [{unit}]", conversion_trnsys * df_trnsys,
                       create_monthly_mean = create_monthly_mean, reference_string = reference_string)

    except Exception as e:
        print(f"{bcolors.WARNING}Could not validate '{title} (Error: {e}). Skipping.")


if __name__ == '__main__':

    # Hier Varianten eintragen

    # General information ============================================================
    # v1 - Komplett passiv
    # v2 - mit internen Lasten
    # v3 - Strahlung langwellig / kurzwellig, keine interne Lasten
    # v4 - TARP Modell
    # v5 - Infiltration, mit internen Lasten
    # v6 - Mit Fenster, komplett passiv, mit Übergangskoeeffizienten
    # v7 - Ohne Fenster mit internen Lasten und ideale Konditionierung
    # ================================================================================

    cwd = os.getcwd()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--case", help="Specifiy the test-case (e.g. 600)", default=630)
    parser.add_argument("-v", "--variant", help="Specifiy the test-case variant with format 'vX' where X is the concrete variant (e.g. v1)", default='v1')
    parser.add_argument("-w", "--windows", help="Specifiy the window names with the following format 'window1,window2'", default='ZONE SUBSURFACE 1')
    args = parser.parse_args()
    
    # just for renaming
    case = args.case
    variant = args.variant
    temp_windows = args.windows
    
    windows = temp_windows.split(",")

    # Output directory
    nandrad   = cwd + f"/data/nandrad/Case{case}_{variant}"
    eso       = cwd + "/data/energyplus/eplusout.eso"
    trnsys    = cwd + f"/data/trnsys/CASE{case}.out"
    reference = cwd + f"/data/reference/monthly-references.tsv"

    # Weather file
    weather_file = cwd + "/data/climate/725650TYCST.epw"

    if os.name == 'nt':
        # Define the path to the EnergyPlus executable
        energyplus_executable = "C:/EnergyPlusV9-0-1/energyplus.exe"

        # NANDRAD solver
        nandrad_executable = "C:/Program Files/VICUS-Software/VICUS/NandradSolver.exe"
    else:
        # Define the path to the EnergyPlus executable
        energyplus_executable = "/home/hirth/Applikationen/EnergyPlus-9-0-1/energyplus"

        # NANDRAD solver
        nandrad_executable = cwd + "/bin/NandradSolver"

    # Define the path to the IDF file
    idf_file = cwd + f"/data/energyplus/Case{case}_{variant}.idf"
    nandrad_file = cwd + f"/data/nandrad/Case{case}_{variant}.nandrad"
    
    # Specify the working directory
    variant_path =  cwd + f"/validation_results_old/Case{case}_{variant}"

    if not os.path.exists(variant_path):
        os.mkdir(variant_path)

    # =========================================================================

    try:
        # Create the subprocess command
        # And call nandrad and energyplus solver
        command_energyplus = [energyplus_executable, '-w', weather_file, idf_file]
        command_nandrad = [nandrad_executable, '-x', nandrad_file]

        # Run the subprocess
        # print("Executing command:", " ".join(command_energyplus))
        subprocess.run(command_energyplus, check=True, cwd= cwd + "/data/energyplus")

        # print("Executing command:", " ".join(command_nandrad))
        subprocess.run(command_nandrad, check=True, cwd= cwd + "/data/nandrad")

        # Read nandrad and eso data
        read_data(nandrad, eso, trnsys, reference)

        # J in Wh/m2 -> /(0.00027777777777778 * 48)
        factor_energy_plus = 1 / (3600 * 1000)
        factor_nandrad = 1 / 1000

        # Air Temperature
        validate("Air Temperature", "C", df_air_temperatures, f"AirTemperature", "Zone Mean Air Temperature", 
                 trnsys_string="Tzone", variant=variant, case=case, unit="C")

        # Window outputs
        validate("Transmitted solar radiation window", "W/m²", df_window, f"WindowSolarRadiationFluxSum",
                 "Zone Windows Total Transmitted", trnsys_string="QTransmitted", variant=variant, case=case, conversion_nandrad=(1./12), conversion_energy_plus=(1./3600/12), unit="W/m2", conversion_trnsys=1000, create_monthly_mean=True)

        validate("Absorbed window radiation", "W", df_window, f"WindowSolarRadiationFluxSum",
                  "Zone Windows Total Heat Loss Energy",
                  "ZONE ONE", trnsys_string="QTransmitted", variant=variant, case=case, conversion_energy_plus=(1./3600), unit="W/m2")
        
        for win in windows:
            validate("Heat conduction window", "W", df_window, f"WindowHeatConductionLoad",
                    "Surface Window Net Heat Transfer Rate",
                    win, trnsys_string="QTransmitted", conversion_nandrad=1./12, conversion_energy_plus=2./12, variant=variant, case=case, substract="Zone Windows Total Transmitted",
                    substract_conversion=0.5*(1./3600), unit="W/m2")

        # Heating
        validate("Heating Load", "kWh", df_heating_load, f"Heating", "Zone Air System Sensible Heating Energy", variant=variant, case=case, 
                 create_monthly_mean=True, trnsys_string="Qheat", conversion_energy_plus=factor_energy_plus, conversion_nandrad=factor_nandrad, unit="kWh", reference_string="heating")
       
        # Cooling
        validate("Cooling Load", "kWh",  df_cooling_load, f"Cooling", "Zone Air System Sensible Cooling Energy", variant=variant, case=case, 
                 create_monthly_mean=True, trnsys_string="Qcool", conversion_energy_plus=factor_energy_plus, conversion_nandrad=factor_nandrad, unit="kWh", reference_string="cooling")
      

        print(f"{bcolors.OKGREEN}Finished validation.{bcolors.ENDC}")
    except Exception as e:
        print(f'{bcolors.FAIL}Could not validate NANDRAD / EnergyPlus.\n{e}{bcolors.ENDC}')
