import ase 
from ase.io import read, write  
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rc('font',**{'family':'sans-serif','sans-serif':['Arial']})
mpl.rcParams['font.size'] = 16

colours = {
    "green": "#00B828",
    "yellow": "#FFD900",
    "purple": "#800FF2",
    "blue": "#0073FF",
    "orange": "#FF5000",
    "grey": "#B3B3B3",
}

plt.rcParams.update({
    'xtick.major.width': 2,     # x-tick thickness
    'ytick.major.width': 2,     # y-tick thickness
    'xtick.major.size': 5,        # x-tick length
    'ytick.major.size': 5,        # y-tick length
    'axes.linewidth': 2,         # Thickness of axis border (applies to spines)
    'lines.linewidth': 2
})

def write_geom(filename):
    """
    Reads a Quantum Espresso input file and writes the atomic positions to an XSF file.
    Input: filename (str) - the full name of the Quantum Espresso input file 
    Output: ASE atoms object, function also writes an XSF file with the atomic positions
    """
    atoms = read(f"{filename}", format='espresso-in') 
    write(f"{filename}.xsf", atoms) 
    return atoms

def plot_dos(e_range=5.0, file_name="work.dos", spin_polarized=True):
    """
    Plots the density of states from Quantum Espresso output files.
    Input: file_name (str) - the base name of the Quantum Espresso output files (without extension)
           e_range (float) - the energy range around the Fermi energy to plot
           spin_polarized (bool) - whether the calculation was spin-polarized
    Output: a plot of the density of states, saved as a PDF file
            fermi energy
    """
    with open(f"{file_name}") as f:
        first_line = f.readline()
        if spin_polarized:
            e_fermi = float(first_line.split()[9])
        else:
            e_fermi = float(first_line.split()[8])
    energy_limits = [e_fermi - e_range, e_fermi + e_range]
    dos = np.genfromtxt(f"{file_name}", skip_header=1) 

    fig, ax = plt.subplots(1, 1)
    if spin_polarized:
        dos_up = dos[:, 1]
        dos_dn = dos[:, 2]
        ax.plot(dos[:, 0], dos_up, color = colours["orange"], label="spin up") 
        ax.plot(dos[:, 0], -dos_dn, color = colours["blue"], label="spin down") 
        ax.legend()
    else:  
        ax.plot(dos[:, 0], dos[:, 1], color = "k") 
    ax.axvline(e_fermi, linestyle='dashed', color = "k") # fermi energy as vertical line
    ax.axhline(0, linestyle='-', color = "k") # fermi energy as horizontal line
    ax.set_xlim(energy_limits)
    ax.set_ylim(-1.1 * np.max(dos[:, 1]), 1.1 * np.max(dos[:, 1]))
    ax.set_ylabel("number of states")
    ax.tick_params(labelleft=False, left=False)
    fig.savefig(f"dos.pdf", bbox_inches='tight') # save the figure as a pdf
    plt.show() # show the figure
    return e_fermi
