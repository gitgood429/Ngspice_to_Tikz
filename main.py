import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib
import os
from pathlib import Path


def main():
    input_folder = Path("simulation_data")
    Path("tex_files").mkdir(exist_ok=True)
    for file in input_folder.iterdir():
        if file.suffix == ".txt":
            print(f"reading simulation data from {file.stem}")
            try:
                simulation_data = read_file(file)
                create_tikz(simulation_data)
                print(f"Tex file created: {simulation_data.output_path}")
            except Exception as ex:
                print(f"Problem reading file {file.stem}. This file will be skipped. Error code: {ex}")
        else:
            print(f"{file.stem} is not a txt file and will be skipped")


def read_file(file_from_ngspice):
    """
    path to from Ngspice (Xschem) AC Simulation. Simulation command should include:
    set filetype=ascii
    wrdata yourfilename.txt vector to be plotted
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
            y_values.append(float(values[1]))
    return SimulationData(file_from_ngspice, y_values, int(x_values[0].split("e")[-1]), int(x_values[-1].split("e")[-1]))


def create_tikz(simulation_data):
    x = np.logspace(simulation_data.start_of_range, simulation_data.end_of_range, simulation_data.range)
    fig, ax = plt.subplots()
    ax.plot(x, simulation_data.y_values)
    ax.set_xscale("log")
    tikzplotlib.save(simulation_data.output_path)


def plot(simulation_data):
    x = np.logspace(simulation_data.start_of_range, simulation_data.end_of_range, simulation_data.range)
    fig, ax = plt.subplots()
    ax.plot(x, simulation_data.y_values)
    ax.set_xscale("log")
    plt.show()


class SimulationData:
    def __init__(self, file_name, y_values, start_of_range, end_of_range):
        self.file_name = file_name
        self.output_path = os.path.join("tex_files", file_name.stem + ".tex")
        self.y_values = y_values
        self.start_of_range = start_of_range
        self.end_of_range = end_of_range
        self.range = len(y_values)


main()
