import esoreader
import pandas as pd
import matplotlib.pyplot as plt

# Pfad zur .eso-Datei
eso_path = "eplusout.eso"

# Laden der Datei
eso = esoreader.read_from_path(eso_path)
print(eso.find_variable('Sunlit'))

# Beispiel: Zone Mean Air Temperature extrahieren 
data = eso.to_frame("Surface Outside Face Sunlit Fraction", frequency="hourly", key="ZONE SUBSURFACE 1  ")

# Als CSV speichern
data.to_csv("shading-factor.csv", sep="\t")

# Plot
data.plot(title="Shading factor", ylabel="---")
plt.tight_layout()
plt.show()

