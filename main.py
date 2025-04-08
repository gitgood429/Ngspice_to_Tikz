import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib
import os
from pathlib import Path


def main(y_exponent=1):
    #y_exponent e.g. 1e-3 for milli
    input_folder = Path("simulation_data")
    Path("tex_files").mkdir(exist_ok=True)
    for file in input_folder.iterdir():
        if file.suffix == ".txt":
            print(f"reading simulation data from {file.stem}")
            try:
                if "ac" in file.stem.lower():
                    simulation_data = read_file_ac(file, y_exponent)
                    create_tikz_log(simulation_data)
                    print(f"DC Tex file created: {simulation_data.output_path}")
                elif "dc" in file.stem.lower():
                    simulation_data = read_file_dc(file, y_exponent)
                    create_tikz_lin(simulation_data)
                    print(f"AC Tex file created: {simulation_data.output_path}")
                elif "smith" in file.stem.lower():
                    simulation_data = read_file_smith(file)
                    create_tikz_lin(simulation_data)
                    print(f"Smith Tex file created: {simulation_data.output_path}")
                    print(r"Beware that the '\addplot' part of this file has to be inserted in a smith chart")
                else:
                    print("please add 'dc', 'ac' or 'smith' to the filename to specify the plot type")
            except Exception as ex:
                print(f"Problem reading file {file.stem}. This file will be skipped. Error code: {ex}")
        else:
            print(f"{file.stem} is not a txt file and will be skipped")


def read_file_dc(file_from_ngspice, y_exponent):
    """
    path to from Ngspice (Xschem) AC Simulation. Simulation command should include:
    set filetype=ascii
    wrdata yourfilename.txt vector
    """
    x_values = []
    y_values = []
    with open(file_from_ngspice, "r") as input:
        for line in input:
            values = line.strip().split(" ")
            while "" in values:
                values.remove("")
            if len(values) < 2:
                continue
            x_values.append(float(values[0]))
            y_values.append(float(values[1])/y_exponent)
    return SimulationData(file_from_ngspice, x_values, y_values)


def read_file_ac(file_from_ngspice, y_exponent):
    """
    path to from Ngspice (Xschem) AC Simulation. Simulation command should include:
    set filetype=ascii
    wrdata yourfilename.txt vector
    """
    x_values = []
    y_values = []
    with open(file_from_ngspice, "r") as input:
        for line in input:
            values = line.strip().split(" ")
            while "" in values:
                values.remove("")
            if len(values) < 2:
                continue
            x_values.append(values[0])
            y_values.append(float(values[1])/y_exponent)
    return SimulationData(file_from_ngspice, x_values, y_values, int(x_values[0].split("e")[-1]), int(x_values[-1].split("e")[-1]))

def read_file_smith(file_from_ngspice):
    """
    path to from Ngspice (Xschem) AC Simulation. Simulation command should include:
    set filetype=ascii
    wrdata yourfilename.txt re(vector) im(vector)
    """
    re_values = []
    im_values = []
    with open(file_from_ngspice, "r") as input:
        for line in input:
            values = line.strip().split(" ")
            while "" in values:
                values.remove("")
            if len(values) < 2:
                continue
            re_values.append(float(values[1]))
            im_values.append(float(values[3]))
    return SimulationData(file_from_ngspice, re_values, im_values)


def create_tikz_lin(simulation_data):
    fig, ax = plt.subplots()
    ax.plot(simulation_data.x_values, simulation_data.y_values)
    tikzplotlib.save(simulation_data.output_path)


def create_tikz_log(simulation_data):
    x = np.logspace(simulation_data.start_of_range, simulation_data.end_of_range, simulation_data.range)
    fig, ax = plt.subplots()
    ax.plot(x, simulation_data.y_values)
    ax.set_xscale("log")
    tikzplotlib.save(simulation_data.output_path)


def plot_lin(simulation_data):
    """
    not used, but useful for debugging, opens plot window
    """
    fig, ax = plt.subplots()
    ax.plot(simulation_data.y_values, simulation_data.y_values)
    plt.show()


def plot_log(simulation_data):
    """
    not used, but useful for debugging, opens plot window
    """
    x = np.logspace(simulation_data.start_of_range, simulation_data.end_of_range, simulation_data.range)
    fig, ax = plt.subplots()
    ax.plot(x, simulation_data.y_values)
    ax.set_xscale("log")
    plt.show()


class SimulationData:
    def __init__(self, file_name, x_values, y_values, start_of_range=0, end_of_range=0):
        self.file_name = file_name
        self.output_path = os.path.join("tex_files", file_name.stem + ".tex")
        self.x_values = x_values
        self.y_values = y_values
        self.start_of_range = start_of_range
        self.end_of_range = end_of_range
        self.range = len(y_values)

main()
