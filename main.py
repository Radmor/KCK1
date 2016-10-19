# -*- coding: utf-8 -*-
import csv
from os import listdir
import matplotlib.pyplot as plt
import os

data_dir_path = 'data'


# obiekt przechowujący numer generacji, liczbę rozegranych gier i średni wynik ze wszystkich runów, wykorzystywany przy tworzeniu wykresu liniowego
class AverageObject(object):
    def __init__(self, generation, games_played, average):
        self.generation = generation
        self.games_played = games_played
        self.average = average


# zwraca listę ścieżek do plików względem tego skryptu
def list_file_paths(dir_path):
    return [os.path.join(dir_path, file) for file in listdir(dir_path)]


# funkcja zwracajaca listę nazw plików z danymi
def list_file_names(dir_path):
    return listdir(dir_path)


# funkcja zwracajaca tablicę wartości zawartych w danym pliku, pomija pierwszy rząd będący słownym opisem kolumn, rzutuje dane w stringach na floaty
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


# funkcja przygotowująca dane z jednego pliku do formatu używanego przy wykresie liniowym
def process_raw_data(rawData):
    return [AverageObject(int(row[0]), int(row[1]), sum(row[2:]) / len(row[2:])) for row in rawData]


def process_all_raw_data(rawDatas):
    return [process_raw_data(rawData) for rawData in rawDatas]


# funkcja przygotowująca dane z jednego pliku do formatu używanego przy wykresie pudełkowym
def process_raw_data_to_box_data(rawData):
    return [float(item) * 100 for item in rawData[-1][2:]]


def process_all_raw_data_to_box_data(rawDatas):
    return [process_raw_data_to_box_data(rawData) for rawData in rawDatas]


# funkcja zwracająca listę kolorów odpowiadających kolejności plików
def get_colors(file_names):
    colors_dict = {
        '2cel-rs.csv': 'red',
        'cel.csv': 'black',
        'cel-rs.csv': 'green',
        'rsel.csv': 'blue',
        '2cel.csv': 'magenta',
    }
    return [colors_dict[file_name] for file_name in file_names]


# funkcja zwracająca listę markerów odpowiadających kolejności plików
def get_markers(file_names):
    markers_dict = {
        '2cel-rs.csv': 'D',
        'cel.csv': 's',
        'cel-rs.csv': 'v',
        'rsel.csv': 'o',
        '2cel.csv': 'd',
    }
    return [markers_dict[file_name] for file_name in file_names]


# funkcja zwracajaca nazwy algorytmów będące labelami na legendzie bądź przy osi
def get_algorithm_names(file_names):
    algorithm_names_dict = {
        '2cel-rs.csv': '2-Coev-RS',
        'cel.csv': '1-Coev',
        'cel-rs.csv': '1-Coev-RS',
        'rsel.csv': '1-Evol-RS',
        '2cel.csv': '2-Coev',
    }
    return [algorithm_names_dict[file_name] for file_name in file_names]


# funkcja tworzaca wykres liniowy
def create_line_plot(subplot, data, filesNames):
    generationsAmount = len(data[0])  # liczba generacji

    markersAmount = 8  # liczba markerów
    markEveryStep = int(generationsAmount / markersAmount)
    markers = get_markers(filesNames)

    algorithm_names = get_algorithm_names(filesNames)
    colors = get_colors(filesNames)

    second_x_axis_step = int(generationsAmount / 5)  # ile ticków na dodatkowej osi x
    max_games_played = 500  # w tysiącach

    for index, algorithm in enumerate(data):
        subplot.plot([item.games_played / 1000 for item in algorithm], [item.average * 100 for item in algorithm],
                     label=algorithm_names[index], color=colors[index], marker=markers[index], markersize=5,
                     markevery=markEveryStep)

    subplot.set_ylabel(r'Odsetek wygranych gier [\%]')  # dodanie opisów osi
    subplot.set_xlabel(r'Rozegranych gier ($\times$ 1000)')
    subplot.set_xticks(range(0, 500 + 1, 100))  # kolejne ticki dla osi x
    subplot.set_xlim([0, max_games_played])  # ograniczenia na wartości na osi x
    subplot.legend(loc=0, framealpha=0.7, prop={'size': 11}, fancybox=True, )  # dodanie legendy
    subplot.grid(True)  # pokazanie siatki

    new_tick_locations = range(0, generationsAmount + 1, second_x_axis_step)

    subplotTwin = subplot.twiny()  # zdublowanie wykresu w celu ustawienia drugiej osi x
    subplotTwin.set_xticks(new_tick_locations)  # okreslenie tickow drugiej osi
    subplotTwin.set_xticklabels(new_tick_locations)  # nadanie tickom etykiet
    subplotTwin.set_xlabel('Pokolenia')  # ustawienie opisu drugiej osi x


# funkcja tworzaca wykres pudelkowy
def create_box_plot(subplot, data, filesNames):
    algorithm_names = get_algorithm_names(filesNames)

    subplot.boxplot(data, labels=algorithm_names, notch=True, showmeans=True,
                    meanprops={'marker': 'o', 'markeredgecolor': 'black', 'linewidth': 10, 'markerfacecolor': 'blue',
                               'markersize': 6}, flierprops={'marker': '+', 'markeredgecolor': 'blue'})
    subplot.set_xticklabels(subplot.xaxis.get_majorticklabels(), rotation=25)
    subplot.yaxis.tick_right()
    subplot.set_ylim([60, 100])
    subplot.grid(True)


# funkcja tworzaca wykresy
def create_plots(averageData, boxData):
    # figure = plt.figure(figsize=(6.7, 6.7))

    # Poprawienie wizualnej strony opisów przez zastosowanie latexa
    plt.rc('font', family='serif')
    plt.rc('text', usetex=True)

    filesNames = list_file_names(data_dir_path)

    # stworzenie dwóch "podwykresów"
    f, (lineSubplot, boxSubplot) = plt.subplots(1, 2, sharey=True, figsize=(6.7, 5.4))

    # wywolanie funkcji tworzacych wykresy
    create_line_plot(lineSubplot, averageData, filesNames)
    create_box_plot(boxSubplot, boxData, filesNames)

    # zapisanie wykresu do pliku
    plt.savefig('wykres.pdf')
    plt.close()


def main():
    data_files_paths = list_file_paths(data_dir_path)  # pobranie listy plików
    data_files = open_all_files(data_files_paths)  # pobranie deskryptorów plików
    raw_data = input_raw_data_from_all_files(data_files)  # wczytanie surowych danych z plikow csv
    averageData = process_all_raw_data(raw_data)
    boxData = process_all_raw_data_to_box_data(raw_data)
    create_plots(averageData, boxData)  # tworzenie wykresow
    close_all_files(data_files)  # zamkniecie plikow z danymi


if __name__ == '__main__':
    main()
