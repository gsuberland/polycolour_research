import colour
from colour import *
from colour.plotting import *
import numpy as np
from scipy.interpolate import interp1d

with open("_names.txt") as file:
    names = [line.rstrip().split(": ") for line in file]
with open("_luminosities.txt") as file:
    luminosities = [line.rstrip().split(": ") for line in file]
luminosities = [[lum[0], float(lum[1])] for lum in luminosities]

sds = []
for colour_name in names:
    name = colour_name[0]
    friendly_name = colour_name[1]
    print("processing " + name + " (" + friendly_name + ") ...")
    with open(name + ".txt") as file:
        spectrum_data = [line.rstrip().split(": ") for line in file]
    spectrum_data = [[float(sp[0]), float(sp[1])] for sp in spectrum_data]
    spx = [sp[0] for sp in spectrum_data]
    spy = [sp[1] for sp in spectrum_data]
    spf = interp1d(spx, spy)
    spectrum_points = {};
    spectrum_point_strings = []
    for wl in range(380, 781):
        pwr = spf(wl).max()
        spectrum_points[wl] = pwr
        spectrum_point_strings.append(str(wl) + ": " + str(pwr) + "\n")
    
    with open(name + "_interp.txt", 'w') as file:
        file.writelines(spectrum_point_strings)
    
    sd = SpectralDistribution(spectrum_points)
    sd.name = friendly_name
    sds.append(sd)
    plot = plot_single_sd(sd, colour.colorimetry.MSDS_CMFS_STANDARD_OBSERVER['cie_10_1964'], standalone=False)[0]
    plot.savefig(name + "_spectrum_cie_1964_10deg.png", dpi=300)
    plot = plot_sds_in_chromaticity_diagram_CIE1976UCS([sd], colour.colorimetry.MSDS_CMFS_STANDARD_OBSERVER['cie_10_1964'], standalone=False)[0]
    plot.savefig(name + "_chromaticity_cie_1964_10deg.png", dpi=300)
    plot = plot_sds_in_chromaticity_diagram_CIE1931([sd], standalone=False)[0]
    plot.savefig(name + "_chromaticity_cie_1931_2deg.png", dpi=300)
    
plot = plot_sds_in_chromaticity_diagram_CIE1976UCS(sds, colour.colorimetry.MSDS_CMFS_STANDARD_OBSERVER['cie_10_1964'], standalone=False)[0]
plot.savefig("all_chromaticity_cie_1964_10deg.png", dpi=300)
plot = plot_sds_in_chromaticity_diagram_CIE1931(sds, standalone=False)[0]
plot.savefig("all_chromaticity_cie_1931_2deg.png", dpi=300)
