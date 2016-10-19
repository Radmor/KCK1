# -*- coding: utf-8 -*-
import csv
# import pandas
from os import listdir
import matplotlib.pyplot as plt
import os
import numpy as np

data_dir_path = 'data'
files = []


# generations_amount

# obiekt przechowujący numer generacji, liczbę rozegranych gier i średni wynik ze wszystkich runów, wykorzystywany przy tworzeniu wykresu liniowego
class AverageObject(object):
    def __init__(self, generation, games_played, average):
        self.generation = generation
        self.games_played = games_played
        self.average = average


# zwraca listę ścieżek do plików względem tego skryptu
def list_file_paths(dir_path):
    return [os.path.join(dir_path, file) for file in listdir(dir_path)]


# zwraca listę nazw plików z danymi
def list_file_names(dir_path):
    return listdir(dir_path)


# zwraca tablicę wartości zawartych w danym pliku, pomija pierwszy rząd będący słownym opisem kolumn, rzutuje dane w stringach na floaty
def input_data(csvFile):
    csvData = list(csv.reader(csvFile))[1:]
    return [[float(item) for item in row] for row in csvData]


# funkcja pomocnicza do wypisywania danych
def print_data(data):
    for row in data:
        print(', '.join(row))


# funkcja otwierająca wszystkie pliki i zwracająca ich deskryptory
def open_all_files(files_paths_list):
    return [open(filePath) for filePath in files_paths_list]


# funkcja zamykajaca pliki
def close_all_files(files_list):
    for file in files_list:
        file.close()


# zwracajaca liste tablic zawierajacych nieobrobione dane z plikow
def input_raw_data_from_all_files(data_files):
    return [input_data(data_file) for data_file in data_files]


# funkcja przygotowujaca dane z jednego pliku do formatu uzywanego przy wykresie liniowym
def process_raw_data(rawData):
    return [AverageObject(int(row[0]), int(row[1]), sum(row[2:]) / len(row[2:])) for row in rawData]


def process_all_raw_data(rawDatas):
    return [process_raw_data(rawData) for rawData in rawDatas]

def process_raw_data_to_box_data(rawData):
    return [float(item)*100 for item in rawData[-1][2:]]

def process_all_raw_data_to_box_data(rawDatas):
    return [process_raw_data_to_box_data(rawData) for rawData in rawDatas]


# funkcja zwracajaca nazwy algorytmów będące labelami na legendzie bądź przy osi
def get_algorithms_names_list(files_names_list):
    return []


def get_markers(file_names):
    markers_dict = {
        '2cel-rs.csv': "o",
        'cel.csv': "v",
        'cel-rs.csv': "D",
        'rsel.csv': "s",
        '2cel.csv': "d",
    }

    return [markers_dict[file_name] for file_name in file_names]


def get_algorithm_names(file_names):
    algorithm_names_dict = {'2cel-rs.csv': '1-Evol-RS',
                            'cel.csv': '2-Coev',
                            'cel-rs.csv': '1-Coev',
                            'rsel.csv': '2-Coev-RS',
                            '2cel.csv': '1-Coev-RS',
                            }
    return [algorithm_names_dict[file_name] for file_name in file_names]


# funkcja tworzaca wykres liniowy
def create_line_plot(subplot, data,filesNames):
    generationsAmount = len(data[0])

    markersAmount = 8
    markEveryStep = int(generationsAmount / markersAmount)
    markers = get_markers(filesNames)

    algorithm_names = get_algorithm_names(filesNames)

    second_x_axis_step = int(generationsAmount / 5)
    max_games_played = 500  # w tysiącach
    for index, algorithm in enumerate(data):
        subplot.plot([item.games_played / 1000 for item in algorithm], [item.average * 100 for item in algorithm],
                     label=algorithm_names[index], marker=markers[index], markersize=5, markevery=markEveryStep)
    subplot.set_ylabel('Odsetek wygranych gier [%]')
    subplot.set_xlabel('Rozegranych gier (×1000)')
    subplot.set_xticks(range(0, 500 + 1, 100))
    subplot.set_xlim([0, max_games_played])
    subplot.legend(loc=0, fancybox=True, framealpha=0.7, prop={'size': 12})
    subplot.grid(True)

    new_tick_locations = range(0, generationsAmount + 1, second_x_axis_step)

    subplotTwin = subplot.twiny()
    subplotTwin.set_xticks(new_tick_locations)
    subplotTwin.set_xticklabels(new_tick_locations)
    subplotTwin.set_xlabel('Pokolenia')

def create_box_plot(subplot,data,filesNames):
    algorithm_names = get_algorithm_names(filesNames)

    subplot.boxplot(data, labels=algorithm_names,notch=True, showmeans=True,meanprops = {'marker':'o', 'markeredgecolor':'black','linewidth':10,'markerfacecolor':'blue', 'markersize' : 6})
    #subplot.scatter([np.mean(row) for row in data],[1,2,3,4,5])
    subplot.set_xticklabels(subplot.xaxis.get_majorticklabels(), rotation=25)
    subplot.yaxis.tick_right()
    subplot.set_ylim([60, 100])
    subplot.grid(True)


# funkcja tworzaca wykresy
def create_plots(averageData, boxData):
    #figure = plt.figure(figsize=(6.7, 6.7))

    filesNames=list_file_names(data_dir_path)
    f, (lineSubplot, boxSubplot) = plt.subplots(1, 2, sharey=True)
    create_line_plot(lineSubplot, averageData,filesNames)
    create_box_plot(boxSubplot,boxData,filesNames)

    plt.savefig('myplot.pdf')
    plt.close()


# main
data_files_paths = list_file_paths(data_dir_path)
data_files = open_all_files(data_files_paths)
raw_data = input_raw_data_from_all_files(data_files)
averageData = process_all_raw_data(raw_data)
boxData= process_all_raw_data_to_box_data(raw_data)
create_plots(averageData, boxData)

close_all_files(data_files)
