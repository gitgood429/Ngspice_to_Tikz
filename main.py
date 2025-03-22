import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib
import os
from pathlib import Path


def main():
    input_folder = Path("simulation_data")
    for file in input_folder.iterdir():
        if file.suffix == ".txt":
            print(f"reading simulation data from {file.stem}")
            simulation_data = read_file(file)
            create_tikz(simulation_data)
        else:
            print(f"{file.stem} is not a txt file and will be skipped")


def read_file(file_from_ngspice):
    """
    path to from Ngspice (Xschem) AC Simulation. Simulation command should include:
    set filetype=ascii
    wrdata yourfilename.txt vector to be plotted
    """
    xvalues = []
    yvalues = []
    with open(file_from_ngspice, "r") as input:
        for line in input:
            values = line.strip().split(" ")
            while "" in values:
                values.remove("")
            if len(values) < 2:
                continue
            xvalues.append(values[0])
            yvalues.append(float(values[1]))
    return SimulationData(file_from_ngspice, yvalues, int(xvalues[0].split("e")[-1]), int(xvalues[-1].split("e")[-1]))


def create_tikz(simulation_data):
    x = np.logspace(simulation_data.start_of_range, simulation_data.end_of_range, simulation_data.range)
    fig, ax = plt.subplots()
    ax.plot(x, simulation_data.y_values)
    ax.set_xscale("log")
    output_path = os.path.join("tex_files", simulation_data.file_name.stem + ".tex")
    print(output_path)
    tikzplotlib.save(output_path)


def plot(simulation_data):
    x = np.logspace(simulation_data.start_of_range, simulation_data.end_of_range, simulation_data.range)
    fig, ax = plt.subplots()
    ax.plot(x, simulation_data.y_values)
    ax.set_xscale("log")
    plt.show()


class SimulationData:
    def __init__(self, file_name, y_values, start_of_range, end_of_range):
        self.file_name = file_name
        self.y_values = y_values
        self.start_of_range = start_of_range
        self.end_of_range = end_of_range
        self.range = len(y_values)


main()





"""   
def plot(file_from_ngspice):
    xvalues = []
    yvalues = []
    with open(file_from_ngspice, "r") as input:
        for line in input:
            values = line.strip().split(" ")
            while "" in values:
                values.remove("")
            if len(values) < 2:
                continue
            print(float(values[1]))
            xvalues.append(float(values[0]))
            yvalues.append(float(values[1]))
    print(xvalues)
    o = np.logspace(6, 10, 4001)
    x = range(0, len(yvalues))
    fig, ax = plt.subplots()
    ax.plot(o, yvalues)
    ax.set_xscale("log")
    plt.show()
    #tikzplotlib.save("test.tex")
"""