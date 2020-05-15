import tkinter
from tkinter import filedialog
import re
import pathlib
import os
import shutil

root = tkinter.Tk()
root.withdraw()  # use to hide tkinter window


class NextFile(Exception):
    pass


def search_for_file_path():
    current_dir = os.getcwd()
    temp_dir = filedialog.askdirectory(parent=root, initialdir=current_dir, title='Please select a directory')
    if len(temp_dir) > 0:
        print("You chose: %s" % temp_dir)
    return temp_dir


def list_dir(path):
    directories = []
    for dir_var in os.listdir(path):
        directories.append(os.path.join(path, dir_var))
    return directories


print('Escolha o caminho de partida')
source_path = search_for_file_path()

print('Escolha o caminho de destino')
destination_path = search_for_file_path()


if destination_path and source_path:
    file_list = list_dir(source_path)
    directories_list = list_dir(destination_path)

    for file in file_list:
        try:
            file_name = pathlib.Path(file).stem.upper()

            match_name = []
            for directory in directories_list:
                path_joined = os.path.join(directory, os.path.split(file)[1])
                if os.path.exists(path_joined):
                    print(f'Arquivo {os.path.split(file)[1]} já existe em {directory}')
                    raise NextFile
                directory_folder = os.path.split(directory)[1].upper()
                match = 0
                for text in str.split(file_name):
                    if re.search(text + r'\b', directory_folder):
                        match += 1
                match_name.append(match)
            best_match = 0
            match_index = 0
            for i in range(len(match_name)):
                if match_name[i] > best_match:
                    match_index = i
                    best_match = match_name[i]
            if best_match > 0:
                shutil.copy(file, directories_list[match_index])
                print(f'Arquivo {os.path.split(file)[1]} foi copiado para {directories_list[match_index]}')
            else:
                print(f'Nenhuma pasta valida para o arquivo {os.path.split(file)[1]}')

        except NextFile:
            continue
    print('Arquivos transferidos.')

else:
    print('Cancelado.')
    input()
    exit()

input('\nAperte Enter para sair')
exit()
