# Allgemeiner Pfad zu den Daten
from os import listdir
from os.path import isfile, join

DATA_PATH = "data/input/"

# Liste mit Dateinamen von Büchern
file_name_list = [f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH, f)) and "cleaned" in f]

# Liste mit Inhalten von Dateien
file_content_list = [" ".join(open(join(DATA_PATH, f)).readlines()) + " " for f in file_name_list]


with open(DATA_PATH + "ALL_ALL_DE.txt", "w") as f:
    for content in file_content_list:
        f.writelines(content)
