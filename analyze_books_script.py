from importlib import reload
import logging
import sys
import time
from datetime import datetime

import pandas as pd
import numpy as np
import networkx as nx
import nx_parallel as nxp

from os import listdir
from os.path import isfile, join

# Importieren und neu laden (damit aktuelle Änderungen übernommen werden)
import config
from helper import graph_analyzer, file_preprocesser
reload(config)
reload(file_preprocesser)
reload(graph_analyzer)


from helper.file_preprocesser import prepare_text_with_libraries, convert_preprocessed_tokens_to_graph, extract_metadata_from_file_name
from helper.graph_analyzer import parallel_get_distance_measures, parallel_get_betweenness_list, get_powerlaw_result
import config

LOGGER_NAME = "Logger"
LOG_PATH = "data/output/analyze_books_script.log"
OUTPUT_FILE = str.format("data/output/output_{0}.csv", datetime.now().strftime("%d_%m_%H_%M_%S")) 


def run():
    initLogger()
    logger = logging.getLogger(LOGGER_NAME)
    logger.info("################################")
    logger.info("Logger initialized")
    nx.config.backends.parallel.active = config.PARALLEL
    nx.config.backends.parallel.n_jobs = config.N_JOBS
    logger.info(str.format("NetworkX backend config: {0}", nx.config.backends))

    process_files(True, config.LINK_DISTANCE)
    process_files(False, config.LINK_DISTANCE)

def process_files(remove_stopwords: bool, link_distance: int):
    logger = logging.getLogger(LOGGER_NAME)
    logger.info(str.format("starting process_files with remove_stopwords: {0}, link_distance: {1}", remove_stopwords, link_distance))
    proccess_files_start_time = time.time()

    start_time = time.time()
    # Liste mit Dateinamen von Büchern
    file_name_list = [f for f in listdir(config.DATA_PATH) if isfile(join(config.DATA_PATH, f))]
    # Liste mit Inhalten von Dateien
    file_content_list = [" ".join(open(join(config.DATA_PATH, f)).readlines()) for f in file_name_list]
    # Tabelle erstellen mit Spalten "title" und "content"
    df = pd.DataFrame({'file_name': file_name_list, 'file_content': file_content_list})
    file_metadata = df["file_name"].apply(extract_metadata_from_file_name).apply(pd.Series)
    df[["author", "title", "language"]] = file_metadata
    df["token_list"] = df.apply(
        lambda row : prepare_text_with_libraries(
            row["file_content"], 
            remove_stopwords=remove_stopwords, 
            language=row["language"]
        ), 
        axis=1
    )
    df["token_list_length"] = df["token_list"].apply(lambda text: len(text))
    # Infos in df schreiben
    df["stopwords_removed"] = remove_stopwords
    df["link_distance"] = link_distance
    logger.info(str.format("Einlesen beendet in: {0}", time.time() - start_time))
    start_time = time.time()
    
    # Graph erstellen
    df["graph"] = df["token_list"].apply(lambda g: convert_preprocessed_tokens_to_graph(g, link_distance))
    logger.info(str.format("Graphen erstellen beendet in: {0}", time.time() - start_time))
    start_time = time.time()

    # Basismetriken: Knotenanzahl und Kantenanzahl
    df["node_count"] = df["graph"].apply(lambda g: len(g.nodes))
    df["edge_count"] = df["graph"].apply(lambda g: len(g.edges))

    # Knotengrade
    df["degree_list"] = df["graph"].apply(lambda g: np.array([deg for node, deg in g.degree ]))

    df["average_degree"] = df["degree_list"].apply(lambda degree_list: np.mean(degree_list))
    df["median_degree"] = df["degree_list"].apply(lambda degree_list: np.median(degree_list))
    logger.info(str.format("Degree Werte berechnen beendet in: {0}", time.time() - start_time))
    start_time = time.time()

    # Falls eingeschaltet: Parallele Berechnungen
    if config.PARALLEL:
        distance_measures = df["graph"].apply(parallel_get_distance_measures).apply(pd.Series)
        df[["diameter", "average_distance"]] = distance_measures
        df["betweenness_list"] = df["graph"].apply(parallel_get_betweenness_list)
        logger.info(str.format("distance measures und betweenness beendet in: {0}", time.time() - start_time))
        start_time = time.time()   

    # Ansonsten (NICHT parallel)
    else:
        df["diameter"] = df["graph"].apply(lambda g: nx.diameter(g))
        df["average_distance"] = df["graph"].apply(lambda g: nx.average_shortest_path_length(g))
        df["betweenness_list"] = df["graph"].apply(lambda g : np.array( list(nx.betweenness_centrality(g).values()) ))
        logger.info(str.format("distance measures und betweenness beendet in: {0}", time.time() - start_time))
        start_time = time.time() 

    # powerlaw-Eigenschaften der Knotenverteilung bestimmen
    powerlaw_result = df["degree_list"].apply(get_powerlaw_result).apply(pd.Series)
    df[["powerlaw_alpha_value", "powerlaw_xmin_value"]] = powerlaw_result
    logger.info(str.format("powerlaw beendet in: {0}", time.time() - start_time))
    start_time = time.time() 

    # Betweenness aus Liste der Einzelwerte
    df["betweenness_min"] = df["betweenness_list"].apply(np.min)
    df["betweenness_max"] = df["betweenness_list"].apply(np.max)
    df["betweenness_average"] = df["betweenness_list"].apply(np.mean)
    df["betweenness_standard_deviation"] = df["betweenness_list"].apply(np.std)
    logger.info(str.format("betweenness Einzelwerte beendet in: {0}", time.time() - start_time))
    start_time = time.time() 

    # Clustering
    df["average_clustering"] = df["graph"].apply(lambda g: nx.average_clustering(g))
    logger.info(str.format("clustering beendet in: {0}", time.time() - start_time))
    start_time = time.time() 

    # Nur bestimmte Spalten sollen in Datei geschrieben werden
    df[config.ATTRIBUTES_VISIBLE_IN_FILE].to_csv(OUTPUT_FILE, index=False, mode='a')
    logger.info("Ergebnisse in output geschrieben.")
    logger.info(str.format("process_files beendet in: {0}", time.time() - proccess_files_start_time))
    return


def initLogger():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("data/output/analyze_books_script.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    sys.excepthook = logUncaughtExceptions

def logUncaughtExceptions(exc_type, exc_value, exc_traceback):
    logger = logging.getLogger(LOGGER_NAME)
    logger.critical("Uncaught exception:", exc_info=(exc_type, exc_value, exc_traceback))



if __name__ == '__main__':
    run()