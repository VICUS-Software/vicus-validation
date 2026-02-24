#!/usr/bin/env python3
"""Generate missing NANDRAD input files for BESTEST cases.

Reads Case600_v1.nandrad and Case900_v1.nandrad as templates, applies
case-specific modifications, and writes the results to data/nandrad/.
"""

import copy
import os
import re
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NANDRAD_DIR = os.path.join(BASE_DIR, "data", "nandrad")

# IBK namespace URI used for parsing/writing
IBK_NS = "urn:ibk"
ET.register_namespace("IBK", IBK_NS)

# Shorthand for creating IBK-prefixed tags
def _ibk(tag):
    return f"{{{IBK_NS}}}{tag}"

# ---------------------------------------------------------------------------
# Template loading helpers
# ---------------------------------------------------------------------------

def load_template(name):
    """Load a .nandrad XML file, injecting IBK namespace for parsing."""
    path = os.path.join(NANDRAD_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # Inject xmlns:IBK on root element so ET can parse IBK: prefixed tags
    text = text.replace(
        '<NandradProject fileVersion="2.0">',
        f'<NandradProject fileVersion="2.0" xmlns:IBK="{IBK_NS}">'
    )
    return ET.ElementTree(ET.fromstring(text))


def deep_copy_tree(tree):
    """Return an independent deep copy of an ElementTree."""
    root_copy = copy.deepcopy(tree.getroot())
    return ET.ElementTree(root_copy)


def write_tree(tree, case_name):
    """Write tree to data/nandrad/Case{case_name}_v1.nandrad.

    Strips the injected xmlns:IBK declaration from output so the file
    matches the original NANDRAD format.
    """
    path = os.path.join(NANDRAD_DIR, f"Case{case_name}_v1.nandrad")
    raw = ET.tostring(tree.getroot(), encoding="unicode", xml_declaration=False)
    # Remove the injected namespace declaration
    raw = raw.replace(f' xmlns:IBK="{IBK_NS}"', '')
    # Write with XML declaration
    with open(path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
        f.write(raw)
        f.write('\n')
    print(f"  Written: {path}")


# ---------------------------------------------------------------------------
# Modification helpers
# ---------------------------------------------------------------------------

def find_project(root):
    return root.find("Project")


def update_zone_display_name(root, case_label):
    """Update the Zone displayName to include the case label."""
    project = find_project(root)
    for zone in project.iter("Zone"):
        old = zone.get("displayName", "")
        # Replace "Case XXX..." pattern
        new = re.sub(r"Case \d+[\w ]*\.", f"Case {case_label}.", old)
        zone.set("displayName", new)


def update_comment(root, case_label):
    """Update ProjectInfo Comment to reference the case."""
    project = find_project(root)
    pi = project.find("ProjectInfo")
    if pi is not None:
        comment = pi.find("Comment")
        if comment is not None:
            old = comment.text or ""
            new = re.sub(r"Case\d+", f"Case{case_label.replace(' ', '')}", old)
            comment.text = new


def replace_glazing(root, u_value, shgc_hemis, shgc_angles, shgc_values, display_name):
    """Replace the WindowGlazingSystem properties."""
    project = find_project(root)
    for wgs in project.iter("WindowGlazingSystem"):
        wgs.set("displayName", display_name)
        for child in list(wgs):
            if child.tag == _ibk("Parameter"):
                name = child.get("name", "")
                if name == "ThermalTransmittance":
                    child.text = str(u_value)
                elif name == "SHGCHemis":
                    child.text = str(shgc_hemis)
            elif child.tag == "LinearSplineParameter":
                for sub in child:
                    if sub.tag == "X":
                        sub.text = shgc_angles
                    elif sub.tag == "Y":
                        sub.text = shgc_values


def update_solar_distribution(root, floor, ceiling, walls):
    """Update SolarLoadsDistributionModel fractions.

    The 'lost' fraction goes to RadiationLoadFractionZone (zone air node).
    """
    project = find_project(root)
    zone_frac = round(100.0 - floor - ceiling - walls, 1)
    for child in project.iter(_ibk("Parameter")):
        name = child.get("name", "")
        if name == "RadiationLoadFractionFloor":
            child.text = str(floor)
        elif name == "RadiationLoadFractionCeiling":
            child.text = str(ceiling)
        elif name == "RadiationLoadFractionWalls":
            child.text = str(walls)
        elif name == "RadiationLoadFractionZone":
            child.text = str(zone_frac)


def set_thermostat_2020(root):
    """Change thermostat schedule from 20,27 deadband to 20,20."""
    project = find_project(root)
    for dc in project.iter("DailyCycle"):
        values_elem = dc.find("Values")
        if values_elem is not None and "CoolingSetpointSchedule" in (values_elem.text or ""):
            values_elem.text = "CoolingSetpointSchedule [C]:20;HeatingSetpointSchedule [C]:20;"


def remove_hvac(root, case_suffix):
    """Remove Thermostats and IdealHeatingCoolingModels + related schedules/objectlists."""
    project = find_project(root)
    models = project.find("Models")
    if models is not None:
        for tag in ("Thermostats", "IdealHeatingCoolingModels"):
            elem = models.find(tag)
            if elem is not None:
                models.remove(elem)

    # Remove thermostat and idealheatcool schedule groups
    schedules = project.find("Schedules")
    if schedules is not None:
        sg = schedules.find("ScheduleGroups")
        if sg is not None:
            to_remove = []
            for group in sg.findall("ScheduleGroup"):
                ol = group.get("objectList", "")
                if "Thermostat" in ol:
                    to_remove.append(group)
            for g in to_remove:
                sg.remove(g)

    # Remove thermostat and idealheatcool object lists
    ol_section = project.find("ObjectLists")
    if ol_section is not None:
        to_remove = []
        for ol in ol_section.findall("ObjectList"):
            name = ol.get("name", "")
            if "Thermostat" in name or "IdealHeatCool" in name:
                to_remove.append(ol)
        for o in to_remove:
            ol_section.remove(o)

    # Rename remaining object list references with FF suffix
    _rename_testfall_suffix(root, case_suffix)


def _rename_testfall_suffix(root, case_suffix):
    """Rename 'Testfall 600' -> 'Testfall {case_suffix}' in schedules, models, object lists."""
    project = find_project(root)
    # Walk all elements and update text/attributes containing the old pattern
    old_patterns = ["Testfall 600", "Testfall 900"]
    new_name = f"Testfall {case_suffix}"
    for elem in project.iter():
        # Check attributes
        for attr_name, attr_val in list(elem.attrib.items()):
            for old in old_patterns:
                if old in attr_val:
                    elem.set(attr_name, attr_val.replace(old, new_name))
        # Check text
        if elem.text:
            for old in old_patterns:
                if old in elem.text:
                    elem.text = elem.text.replace(old, new_name)


def update_wall_insulation_low_mass(root, thickness, mat_id):
    """Update the wall ConstructionType (id=3) middle layer for low-mass cases.

    In Case600, wall is: Plasterboard(0.012) / Fiberglass(0.066, matId=1010002) / WoodSiding(0.009)
    For Case680: replace fiberglass with foam insulation (different thickness and matId).
    """
    project = find_project(root)
    for ct in project.iter("ConstructionType"):
        if ct.get("id") == "3":
            ct.set("displayName", "Low-Mass Case: Exterior Wall (increased insulation)")
            ml = ct.find("MaterialLayers")
            if ml is not None:
                layers = ml.findall("MaterialLayer")
                if len(layers) >= 2:
                    # Middle layer (index 1) is the insulation
                    layers[1].set("thickness", str(thickness))
                    layers[1].set("matId", str(mat_id))


def update_roof_insulation(root, thickness):
    """Update the roof ConstructionType (id=2) fiberglass layer thickness."""
    project = find_project(root)
    for ct in project.iter("ConstructionType"):
        if ct.get("id") == "2":
            ct.set("displayName", ct.get("displayName", "").replace("Roof", "Roof (increased insulation)"))
            ml = ct.find("MaterialLayers")
            if ml is not None:
                layers = ml.findall("MaterialLayer")
                if len(layers) >= 2:
                    # Middle layer (index 1) is the fiberglass
                    layers[1].set("thickness", str(thickness))


def add_foam_material(root):
    """Add Foam Insulation material (id=1010008) if not already present."""
    project = find_project(root)
    materials = project.find("Materials")
    if materials is None:
        return
    # Check if already present
    for mat in materials.findall("Material"):
        if mat.get("id") == "1010008":
            return
    # Add it
    foam = ET.SubElement(materials, "Material")
    foam.set("id", "1010008")
    foam.set("displayName", "Foam Insulation")
    _add_ibk_param(foam, "Density", "kg/m3", "10")
    _add_ibk_param(foam, "HeatCapacity", "J/kgK", "1400")
    _add_ibk_param(foam, "Conductivity", "W/mK", "0.04")


def _add_ibk_param(parent, name, unit, value):
    """Add an IBK:Parameter element using the registered namespace."""
    p = ET.SubElement(parent, _ibk("Parameter"))
    p.set("name", name)
    p.set("unit", unit)
    p.text = value


def update_wall_insulation_high_mass(root, thickness):
    """Update the wall ConstructionType (id=3) foam insulation layer for high-mass cases.

    In Case900, wall is: ConcreteBlock(0.1) / FoamInsulation(0.0615, matId=1010008) / WoodSiding(0.009)
    For Case980: increase foam insulation thickness to 0.2452m.
    """
    project = find_project(root)
    for ct in project.iter("ConstructionType"):
        if ct.get("id") == "3":
            ct.set("displayName", "High-Mass Case: Exterior Wall (increased insulation)")
            ml = ct.find("MaterialLayers")
            if ml is not None:
                layers = ml.findall("MaterialLayer")
                if len(layers) >= 2:
                    # Middle layer (index 1) is the foam insulation
                    layers[1].set("thickness", str(thickness))


# ---------------------------------------------------------------------------
# Case 960 — Two-zone sunspace (special handling)
# ---------------------------------------------------------------------------

def generate_case960(tree600, tree900):
    """Generate Case 960 — two-zone sunspace.

    Back zone: lightweight (Case 600 construction), no south windows,
               heated/cooled with 20,27 thermostat, 200W internal gains.
    Sun zone:  heavyweight (Case 900 construction), south-facing windows,
               free-floating, 0W internal gains.
    Common wall: 0.20m concrete block between zones.
    """
    tree = deep_copy_tree(tree600)
    root = tree.getroot()
    project = find_project(root)

    # --- Zone setup ---
    zones = project.find("Zones")
    # Update existing zone (id=3) as back zone
    for zone in zones.findall("Zone"):
        zone.set("displayName", "Case 960.Back Zone(ID=3)")
        # Back zone: 8x6x2.7
        for p in zone.findall(_ibk("Parameter")):
            if p.get("name") == "Area":
                p.text = "48"
            elif p.get("name") == "Volume":
                p.text = "129.6"

    # Add sun zone (id=4)
    sun_zone = ET.SubElement(zones, "Zone")
    sun_zone.set("id", "4")
    sun_zone.set("displayName", "Case 960.Sun Zone(ID=4)")
    sun_zone.set("type", "Active")
    _add_ibk_param(sun_zone, "Area", "m2", "16")
    _add_ibk_param(sun_zone, "Volume", "m3", "43.2")

    # --- Construction Instances ---
    ci_section = project.find("ConstructionInstances")

    # Remove existing south wall and window surfaces (ids 7, 9, 11) from back zone
    # Back zone loses its south-facing windows — replaced by common wall
    to_remove = []
    for ci in ci_section.findall("ConstructionInstance"):
        cid = ci.get("id")
        # Remove south wall (id=7) and window surfaces (id=9,11)
        if cid in ("7", "9", "11"):
            to_remove.append(ci)
    for ci in to_remove:
        ci_section.remove(ci)

    # Add common wall between back zone and sun zone (id=20)
    common_wall = _make_construction_instance(
        ci_id="20", display_name="Common Wall Back-Sun (ID=20)",
        ct_id="4", orientation="180", inclination="90",
        area="21.6",  # 8m x 2.7m
        interface_a_zone="3", interface_a_usage="Wall",
        interface_a_htc="1.8",
        interface_b_zone="4", interface_b_usage="Wall",
        interface_b_htc="1.8",
        interior=True  # Both sides are interior
    )
    ci_section.append(common_wall)

    # Add sun zone surfaces
    # Sun zone floor (id=30)
    sun_floor = _make_exterior_ci(
        ci_id="30", display_name="Sun Zone Floor (ID=30)",
        ct_id="5", orientation="270", inclination="180", area="16",
        interface_a_zone="4", interface_a_usage="Floor", interface_a_htc="3.7",
        interface_b_htc="5.2", solar_abs="0.6"
    )
    ci_section.append(sun_floor)

    # Sun zone ceiling (id=31)
    sun_ceiling = _make_exterior_ci(
        ci_id="31", display_name="Sun Zone Ceiling (ID=31)",
        ct_id="2", orientation="90", inclination="0", area="16",
        interface_a_zone="4", interface_a_usage="Ceiling", interface_a_htc="1.7",
        interface_b_htc="21.8", solar_abs="0.6", ext_solar_abs="0.6"
    )
    ci_section.append(sun_ceiling)

    # Sun zone east wall (id=32)
    sun_east = _make_exterior_ci(
        ci_id="32", display_name="Sun Zone Wall East (ID=32)",
        ct_id="6", orientation="90", inclination="90", area="5.4",
        interface_a_zone="4", interface_a_usage="Wall", interface_a_htc="1.8",
        interface_b_htc="21.6", solar_abs="0.6", ext_solar_abs="0.6"
    )
    ci_section.append(sun_east)

    # Sun zone west wall (id=33)
    sun_west = _make_exterior_ci(
        ci_id="33", display_name="Sun Zone Wall West (ID=33)",
        ct_id="6", orientation="270", inclination="90", area="5.4",
        interface_a_zone="4", interface_a_usage="Wall", interface_a_htc="1.8",
        interface_b_htc="21.6", solar_abs="0.6", ext_solar_abs="0.6"
    )
    ci_section.append(sun_west)

    # Sun zone south wall + windows (id=34, 35)
    sun_south_left = _make_exterior_ci_with_window(
        ci_id="34", display_name="Sun Zone Surface south left (ID=34)",
        ct_id="6", orientation="180", inclination="90", area="6",
        interface_a_zone="4", interface_a_htc="4.5",
        interface_b_htc="17.8",
        win_id="40", win_display="Sun Zone Window left (ID=40)",
        win_area="5.99", glazing_id="1040003"
    )
    ci_section.append(sun_south_left)

    sun_south_right = _make_exterior_ci_with_window(
        ci_id="35", display_name="Sun Zone Surface south right (ID=35)",
        ct_id="6", orientation="180", inclination="90", area="6",
        interface_a_zone="4", interface_a_htc="4.5",
        interface_b_htc="17.8",
        win_id="41", win_display="Sun Zone Window right (ID=41)",
        win_area="5.99", glazing_id="1040003"
    )
    ci_section.append(sun_south_right)

    # --- Construction Types ---
    ct_section = project.find("ConstructionTypes")

    # Add common wall construction type (id=4): single concrete block layer
    ct_common = ET.SubElement(ct_section, "ConstructionType")
    ct_common.set("id", "4")
    ct_common.set("displayName", "Common Wall: Concrete Block")
    ml = ET.SubElement(ct_common, "MaterialLayers")
    layer = ET.SubElement(ml, "MaterialLayer")
    layer.set("thickness", "0.20")
    layer.set("matId", "1010007")

    # Add high-mass floor construction type (id=5) from Case 900
    ct_floor = ET.SubElement(ct_section, "ConstructionType")
    ct_floor.set("id", "5")
    ct_floor.set("displayName", "High-Mass Case: Raised Floor")
    ml2 = ET.SubElement(ct_floor, "MaterialLayers")
    layer1 = ET.SubElement(ml2, "MaterialLayer")
    layer1.set("thickness", "0.08")
    layer1.set("matId", "1010009")
    layer2 = ET.SubElement(ml2, "MaterialLayer")
    layer2.set("thickness", "1.007")
    layer2.set("matId", "1010005")

    # Add high-mass exterior wall construction type (id=6) from Case 900
    ct_hmwall = ET.SubElement(ct_section, "ConstructionType")
    ct_hmwall.set("id", "6")
    ct_hmwall.set("displayName", "High-Mass Case: Exterior Wall")
    ml3 = ET.SubElement(ct_hmwall, "MaterialLayers")
    layer_a = ET.SubElement(ml3, "MaterialLayer")
    layer_a.set("thickness", "0.1")
    layer_a.set("matId", "1010007")
    layer_b = ET.SubElement(ml3, "MaterialLayer")
    layer_b.set("thickness", "0.0615")
    layer_b.set("matId", "1010008")
    layer_c = ET.SubElement(ml3, "MaterialLayer")
    layer_c.set("thickness", "0.009")
    layer_c.set("matId", "1010003")

    # --- Materials: add high-mass materials not in Case 600 ---
    materials = project.find("Materials")
    _ensure_material(materials, "1010007", "Concrete Block", "1400", "1000", "0.51")
    _ensure_material(materials, "1010008", "Foam Insulation", "10", "1400", "0.04")
    _ensure_material(materials, "1010009", "Concrete Slab", "1400", "1000", "1.13")

    # --- Schedules: add sun zone internal loads (0W) + ventilation ---
    schedules = project.find("Schedules")
    sg = schedules.find("ScheduleGroups")

    # Sun zone internal loads schedule (0W)
    sun_il_group = ET.SubElement(sg, "ScheduleGroup")
    sun_il_group.set("objectList", "InternalLoads-Testfall 960SZ")
    sun_sched = ET.SubElement(sun_il_group, "Schedule")
    sun_sched.set("type", "AllDays")
    ET.SubElement(sun_sched, "StartDayOfTheYear").text = "0"
    ET.SubElement(sun_sched, "EndDayOfTheYear").text = "364"
    dc_container = ET.SubElement(sun_sched, "DailyCycles")
    dc = ET.SubElement(dc_container, "DailyCycle")
    dc.set("interpolation", "Constant")
    ET.SubElement(dc, "TimePoints").text = "0"
    ET.SubElement(dc, "Values").text = "EquipmentHeatLoadPerAreaSchedule [W/m2]:0;LightingHeatLoadPerAreaSchedule [W/m2]:0;PersonHeatLoadPerAreaSchedule [W/m2]:0;"

    # Sun zone ventilation schedule (empty)
    sun_vent_group = ET.SubElement(sg, "ScheduleGroup")
    sun_vent_group.set("objectList", "Ventilation-Testfall 960SZ")

    # --- Models ---
    models = project.find("Models")

    # Add ventilation model for sun zone
    vent_models = models.find("NaturalVentilationModels")
    sun_vent = ET.SubElement(vent_models, "NaturalVentilationModel")
    sun_vent.set("id", "5")
    sun_vent.set("displayName", "Testfall 960SZ")
    sun_vent.set("modelType", "Constant")
    ET.SubElement(sun_vent, "ZoneObjectList").text = "Ventilation-Testfall 960SZ"
    _add_ibk_param(sun_vent, "VentilationRate", "1/h", "0.414")

    # Add internal loads model for sun zone
    il_models = models.find("InternalLoadsModels")
    sun_il = ET.SubElement(il_models, "InternalLoadsModel")
    sun_il.set("id", "2")
    sun_il.set("displayName", "Testfall 960SZ")
    sun_il.set("modelType", "Scheduled")
    ET.SubElement(sun_il, "ZoneObjectList").text = "InternalLoads-Testfall 960SZ"
    _add_ibk_param(sun_il, "EquipmentRadiationFraction", "---", "0.6")
    _add_ibk_param(sun_il, "PersonRadiationFraction", "---", "0")
    _add_ibk_param(sun_il, "LightingRadiationFraction", "---", "0")

    # --- Object Lists: add sun zone object lists ---
    ol_section = project.find("ObjectLists")

    _add_object_list(ol_section, "InternalLoads-Testfall 960SZ", "4", "Zone")
    _add_object_list(ol_section, "Ventilation-Testfall 960SZ", "4", "Zone")

    # Update existing back zone object lists to filter only zone 3
    # (Thermostat and IdealHeatCool should only apply to back zone)
    # They already filter on id=3, so no change needed.

    # Update zone display name
    update_zone_display_name(root, "960")

    # Solar distribution: use back zone defaults (same as Case 600)
    # Sun zone has different distribution but SurfaceTypeFactor model
    # applies globally — we keep the back zone values since it's the
    # primary controlled zone.

    return tree


def _ensure_material(materials, mid, name, density, cp, conductivity):
    """Add material if not already present."""
    for mat in materials.findall("Material"):
        if mat.get("id") == mid:
            return
    m = ET.SubElement(materials, "Material")
    m.set("id", mid)
    m.set("displayName", name)
    _add_ibk_param(m, "Density", "kg/m3", density)
    _add_ibk_param(m, "HeatCapacity", "J/kgK", cp)
    _add_ibk_param(m, "Conductivity", "W/mK", conductivity)


def _add_object_list(ol_section, name, filter_id, ref_type):
    ol = ET.SubElement(ol_section, "ObjectList")
    ol.set("name", name)
    ET.SubElement(ol, "FilterID").text = filter_id
    ET.SubElement(ol, "ReferenceType").text = ref_type


def _make_construction_instance(ci_id, display_name, ct_id, orientation, inclination,
                                 area, interface_a_zone, interface_a_usage,
                                 interface_a_htc, interface_b_zone, interface_b_usage,
                                 interface_b_htc, interior=False):
    """Create a ConstructionInstance element with two interfaces (interzone wall)."""
    ci = ET.Element("ConstructionInstance")
    ci.set("id", ci_id)
    ci.set("displayName", display_name)
    ET.SubElement(ci, "ConstructionTypeId").text = ct_id
    _add_ibk_param(ci, "Orientation", "Deg", orientation)
    _add_ibk_param(ci, "Inclination", "Deg", inclination)
    _add_ibk_param(ci, "Area", "m2", area)

    ia = ET.SubElement(ci, "InterfaceA")
    ia.set("id", "1")
    ia.set("zoneId", interface_a_zone)
    ia.set("usage", interface_a_usage)
    hc_a = ET.SubElement(ia, "InterfaceHeatConduction")
    hc_a.set("modelType", "Constant")
    _add_ibk_param(hc_a, "HeatTransferCoefficient", "W/m2K", interface_a_htc)
    sa_a = ET.SubElement(ia, "InterfaceSolarAbsorption")
    sa_a.set("modelType", "Constant")
    _add_ibk_param(sa_a, "AbsorptionCoefficient", "---", "0.6")

    ib = ET.SubElement(ci, "InterfaceB")
    ib.set("id", "2")
    ib.set("zoneId", interface_b_zone)
    ib.set("usage", interface_b_usage)
    hc_b = ET.SubElement(ib, "InterfaceHeatConduction")
    hc_b.set("modelType", "Constant")
    _add_ibk_param(hc_b, "HeatTransferCoefficient", "W/m2K", interface_b_htc)
    if interior:
        sa_b = ET.SubElement(ib, "InterfaceSolarAbsorption")
        sa_b.set("modelType", "Constant")
        _add_ibk_param(sa_b, "AbsorptionCoefficient", "---", "0.6")

    return ci


def _make_exterior_ci(ci_id, display_name, ct_id, orientation, inclination, area,
                       interface_a_zone, interface_a_usage, interface_a_htc,
                       interface_b_htc, solar_abs="0.6", ext_solar_abs=None):
    """Create a ConstructionInstance with interior (A) and exterior (B) interfaces."""
    ci = ET.Element("ConstructionInstance")
    ci.set("id", ci_id)
    ci.set("displayName", display_name)
    ET.SubElement(ci, "ConstructionTypeId").text = ct_id
    _add_ibk_param(ci, "Orientation", "Deg", orientation)
    _add_ibk_param(ci, "Inclination", "Deg", inclination)
    _add_ibk_param(ci, "Area", "m2", area)

    ia = ET.SubElement(ci, "InterfaceA")
    ia.set("id", "1")
    ia.set("zoneId", interface_a_zone)
    ia.set("usage", interface_a_usage)
    hc_a = ET.SubElement(ia, "InterfaceHeatConduction")
    hc_a.set("modelType", "Constant")
    _add_ibk_param(hc_a, "HeatTransferCoefficient", "W/m2K", interface_a_htc)
    sa_a = ET.SubElement(ia, "InterfaceSolarAbsorption")
    sa_a.set("modelType", "Constant")
    _add_ibk_param(sa_a, "AbsorptionCoefficient", "---", solar_abs)

    ib = ET.SubElement(ci, "InterfaceB")
    ib.set("id", "2")
    ib.set("zoneId", "0")
    ib.set("usage", "Other")
    hc_b = ET.SubElement(ib, "InterfaceHeatConduction")
    hc_b.set("modelType", "Constant")
    _add_ibk_param(hc_b, "HeatTransferCoefficient", "W/m2K", interface_b_htc)
    if ext_solar_abs:
        sa_b = ET.SubElement(ib, "InterfaceSolarAbsorption")
        sa_b.set("modelType", "Constant")
        _add_ibk_param(sa_b, "AbsorptionCoefficient", "---", ext_solar_abs)
    lwe = ET.SubElement(ib, "InterfaceLongWaveEmission")
    lwe.set("modelType", "Constant")
    _add_ibk_param(lwe, "Emissivity", "---", "0.9")

    return ci


def _make_exterior_ci_with_window(ci_id, display_name, ct_id, orientation, inclination,
                                    area, interface_a_zone, interface_a_htc,
                                    interface_b_htc, win_id, win_display, win_area,
                                    glazing_id):
    """Create exterior CI with an embedded window."""
    ci = _make_exterior_ci(
        ci_id, display_name, ct_id, orientation, inclination, area,
        interface_a_zone, "Wall", interface_a_htc, interface_b_htc,
        solar_abs="0.6", ext_solar_abs="0.6"
    )
    eo = ET.SubElement(ci, "EmbeddedObjects")
    win = ET.SubElement(eo, "EmbeddedObject")
    win.set("id", win_id)
    win.set("displayName", win_display)
    _add_ibk_param(win, "Area", "m2", win_area)
    w = ET.SubElement(win, "Window")
    w.set("glazingSystemId", glazing_id)
    return ci


# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------

def main():
    print("Loading templates...")
    tree600 = load_template("Case600_v1.nandrad")
    tree900 = load_template("Case900_v1.nandrad")

    # -----------------------------------------------------------------------
    # Group A: Low-mass variants (based on Case 600)
    # -----------------------------------------------------------------------
    print("\n--- Group A: Low-mass variants ---")

    # Case 660: Low-E Argon Windows
    print("Generating Case 660...")
    t = deep_copy_tree(tree600)
    r = t.getroot()
    update_zone_display_name(r, "660")
    replace_glazing(r,
        u_value=1.19, shgc_hemis=0.377,
        shgc_angles="0 10 20 30 40 50 60 70 80 90 ",
        shgc_values="0.440 0.443 0.438 0.432 0.422 0.403 0.361 0.278 0.148 0 ",
        display_name="Low-E Argon Window Case 660")
    update_solar_distribution(r, floor=64.5, ceiling=17.0, walls=15.8)
    write_tree(t, "660")

    # Case 670: Single-Pane Windows
    print("Generating Case 670...")
    t = deep_copy_tree(tree600)
    r = t.getroot()
    update_zone_display_name(r, "670")
    replace_glazing(r,
        u_value=5.16, shgc_hemis=0.787,
        shgc_angles="0 10 20 30 40 50 60 70 80 90 ",
        shgc_values="0.864 0.864 0.862 0.859 0.851 0.831 0.785 0.673 0.424 0 ",
        display_name="Single-Pane Window Case 670")
    update_solar_distribution(r, floor=64.1, ceiling=16.6, walls=15.3)
    write_tree(t, "670")

    # Case 680: Increased Insulation
    print("Generating Case 680...")
    t = deep_copy_tree(tree600)
    r = t.getroot()
    update_zone_display_name(r, "680")
    add_foam_material(r)
    update_wall_insulation_low_mass(r, thickness=0.250, mat_id=1010008)
    update_roof_insulation(r, thickness=0.400)
    write_tree(t, "680")

    # Case 680FF: Free-Float Increased Insulation
    print("Generating Case 680FF...")
    t = deep_copy_tree(tree600)
    r = t.getroot()
    add_foam_material(r)
    update_wall_insulation_low_mass(r, thickness=0.250, mat_id=1010008)
    update_roof_insulation(r, thickness=0.400)
    remove_hvac(r, "680FF")
    update_zone_display_name(r, "680 FF")
    write_tree(t, "680FF")

    # Case 685: 20,20 Thermostat
    print("Generating Case 685...")
    t = deep_copy_tree(tree600)
    r = t.getroot()
    update_zone_display_name(r, "685")
    set_thermostat_2020(r)
    write_tree(t, "685")

    # Case 695: Increased Insulation + 20,20 Thermostat
    print("Generating Case 695...")
    t = deep_copy_tree(tree600)
    r = t.getroot()
    update_zone_display_name(r, "695")
    add_foam_material(r)
    update_wall_insulation_low_mass(r, thickness=0.250, mat_id=1010008)
    update_roof_insulation(r, thickness=0.400)
    set_thermostat_2020(r)
    write_tree(t, "695")

    # -----------------------------------------------------------------------
    # Group B: High-mass variants (based on Case 900)
    # -----------------------------------------------------------------------
    print("\n--- Group B: High-mass variants ---")

    # Case 980: High-Mass Increased Insulation
    print("Generating Case 980...")
    t = deep_copy_tree(tree900)
    r = t.getroot()
    update_zone_display_name(r, "980")
    update_wall_insulation_high_mass(r, thickness=0.2452)
    update_roof_insulation(r, thickness=0.4)
    write_tree(t, "980")

    # Case 980FF: Free-Float High-Mass Increased Insulation
    print("Generating Case 980FF...")
    t = deep_copy_tree(tree900)
    r = t.getroot()
    update_wall_insulation_high_mass(r, thickness=0.2452)
    update_roof_insulation(r, thickness=0.4)
    remove_hvac(r, "980FF")
    update_zone_display_name(r, "980 FF")
    write_tree(t, "980FF")

    # Case 985: High-Mass 20,20 Thermostat
    print("Generating Case 985...")
    t = deep_copy_tree(tree900)
    r = t.getroot()
    update_zone_display_name(r, "985")
    set_thermostat_2020(r)
    write_tree(t, "985")

    # Case 995: High-Mass Increased Insulation + 20,20 Thermostat
    print("Generating Case 995...")
    t = deep_copy_tree(tree900)
    r = t.getroot()
    update_zone_display_name(r, "995")
    update_wall_insulation_high_mass(r, thickness=0.2452)
    update_roof_insulation(r, thickness=0.4)
    set_thermostat_2020(r)
    write_tree(t, "995")

    # -----------------------------------------------------------------------
    # Group C: Special case
    # -----------------------------------------------------------------------
    print("\n--- Group C: Case 960 (sunspace) ---")

    print("Generating Case 960...")
    t = generate_case960(tree600, tree900)
    write_tree(t, "960")

    print("\nDone! Generated 11 NANDRAD case files.")


if __name__ == "__main__":
    main()
