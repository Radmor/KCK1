# -*- coding: utf-8 -*-
import csv
#import pandas
from os import listdir
import matplotlib.pyplot as plt
import glob
import os
import numpy as np


data_dir_path='data'
files=[]
#generations_amount


class AverageObject(object):
    def __init__(self,generation,games_played,average):
        self.generation=generation
        self.games_played=games_played
        self.average=average


def list_file_paths(dir_path):
    return [os.path.join(dir_path,file) for file in listdir(dir_path)]

def input_data(csvFile):
        csvData=list(csv.reader(csvFile))[1:]

        return [[float(item) for item in row] for row in csvData]
        '''
        for row in csvData:
            print (', '.join(row))
        return csvData
        '''

def print_data(data):
    for row in data:
        print (', '.join(row))

def open_all_files(files_paths_list):
    return [open(filePath) for filePath in files_paths_list]

def close_all_files(files_list):
    for file in files_list:
        file.close()

def input_raw_data_from_all_files(data_files):
    return [input_data(data_file) for data_file in data_files]

def process_raw_data(raw_data):
    return [AverageObject(int(row[0]),int(row[1]),sum(row[2:])/len(row[2:])) for row in raw_data]

def process_all_raw_data(raw_datas):
    return [process_raw_data(raw_data) for raw_data in raw_datas]

def test_figure():
    plt.figure(figsize=(6.7, 6.7))
    plt.plot([100,200,300,400],[0.1,0.2,0.8,0.9])
    plt.savefig('myplot.pdf')
    plt.close()

def create_plots(average_data):
    figure=plt.figure(figsize=(6.7, 6.7))

    f, (line_subplot, box_subplot) = plt.subplots(1, 2, sharey=True)
    #line_subplot=figure.add_subplot(111)
    #box_subplot=figure.add_subplot(211)
    create_line_plot(line_subplot,average_data)


    plt.savefig('myplot.pdf')
    plt.close()

def get_algorithms_names_list(files_names_list):
    return []


def create_line_plot(subplot,data):

    algorithm_names=['2cel-rs.csv','cel.csv','cel-rs.csv','rsel.csv','2cel.csv']
    generationsAmount=len(data[0])
    second_x_axis_step=int(generationsAmount/5)
    max_games_played=500 # w tysiącach
    for algorithm in data:
        subplot.plot([item.games_played/1000 for item in algorithm],[item.average*100 for item in algorithm])
    subplot.set_ylabel('Odsetek wygranych gier [%]')
    subplot.set_xlabel('Rozegranych gier (×1000)')
    subplot.set_xticks(range(0,500+1,100))
    subplot.set_xlim([0,max_games_played])


    new_tick_locations = range(0,generationsAmount+1,second_x_axis_step)

    subplot2=subplot.twiny()
    #subplot2.set_xlim(subplot.get_xlim())
    subplot2.set_xticks(new_tick_locations)
    subplot2.set_xticklabels(new_tick_locations)
    subplot2.set_xlabel('Pokolenia')


data_files_paths=list_file_paths(data_dir_path)
print(data_files_paths)
'''
algorithms_names={
    '2cel-rs.csv':,
    'cel.csv':,
    'cel-rs.csv':,
    'rsel.csv':,
    '2cel.csv':


}
'''

data_files=open_all_files(data_files_paths)
raw_data=input_raw_data_from_all_files(data_files)
data=process_all_raw_data(raw_data)

#print_data(raw_data[0])

#print(raw_data)

#test_figure()
create_plots(data)

close_all_files(data_files)
