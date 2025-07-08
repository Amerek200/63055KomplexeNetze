# Allgemeiner Pfad zu den Daten
DATA_PATH = "data/input"

# networkX-Einstellungen
PARALLEL = True
N_JOBS = 4

# Textverarbeitung
REMOVE_STOPWORDS = True
LINK_DISTANCE = 1
FIXED_TOKEN_COUNT = 13062

# Ausgabe
ATTRIBUTES_VISIBLE_IN_FILE = [
    "author",
    "title",
    "language",
    "token_list_length",
    "node_count",
    "edge_count",
    "average_degree",
    "median_degree",
    "diameter",
    "average_distance",
    "betweenness_min",
    "betweenness_max",
    "betweenness_average",
    "betweenness_standard_deviation",
    "average_clustering",
    "powerlaw_alpha_value",
    "powerlaw_xmin_value",
    "stopwords_removed",
    "link_distance",
    "fixed_token_count"
]