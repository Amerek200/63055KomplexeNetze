# Aufbau des Repositorys
Der Code orientiert sich im wesentlichen an der schriftlichen Ausarbeitung:

Zuerst wurden zu den in der Arbeit genannten Büchern **Co-Occurence-Netzwerke gebildet, um dann zu diesen jeweils die Netzwerkmetriken zu erfassen**. Dieser Vorgang findet in `analyze_books.ipynb` statt. Die Bücher können als txt-Dateien im Ordner `data/input` abgelegt werden (die Benennung der Bücher sollte diesem Namensschema folgen: `Autor_Buchtitel_Sprache.txt`). Dann werden die Metriken zu den Netzen berechnet, um die Ergebnisse im Verzeichnis `data/output` unter dem Dateinamen `output.csv` zu speichern.

Bevor diese Analyse stattfindet kann `combine_files.py` ausgeführt werden, um **alle txt-Dateien aus dem input-Verzeichnis innerhalb einer großen txt-Datei zu kombinieren** (indem wir alle anderen txt-Dateien einfach aneinanderhängen). Das Ergebnis der Ausführung ist die neue Datei `ALL_ALL_DE.txt`. Diese kann wie die anderen txt-Dateien von `analyze_books.ipynb` benutzt werden, um die allgemeine Analyse der deutschen Sprache durchzuführen. 

Falls umgestellt werden soll, **welche Metriken in der `output.csv` gespeichert werden** sollen, kann die Konstante `ATTRIBUTES_VISIBLE_IN_FILE` in der Datei `config.py` verändert werden. Diese Datei enthält allgemeine Konfigurationsparameter zu unserem Projekt. Hier kann bspw. auch die **Nachbarschaftsdistanz** umgestellt werden, welche bei der Erstellung der Co-Occurence-Graphen genutzt wird. 

Für das **Einlesen der Dateien, das Erstellen der Graphen und das Berechnen mancher Metriken** wurden **Hilfsfunktionen** erstellt (wie bspw. die Methode `convert_preprocessed_tokens_to_graph`, in welcher die Umwandlung von Token-Liste zu Graph stattfindet). Die Hilfsfunktionen sind innerhalb der Dateien `file_preprocessor.txt` und `graph_analyzer.txt` im Verzeichnis `helper` auffindbar. 

**Weitergehende Analysen auf den Daten (bspw. Visualisierungen)** wurden in dem Verzeichnis `data_analysis` durchgeführt. 
Für die **Klassifikation** nutzten wir die Dateien `classifiers_mixed_languages.ipynb` (sprachunabhängige Klassifikation) und `classifiers_separated_languages.ipynb` (sprachabhängige Klassifikation). Aus dem `helper` Verzeichnis haben wir das `normalizer`-Modul genutzt, um die Daten vor der Klassifikation zu normalisieren. 
Die Datei `scatter_matrix.ipynb` dient dazu, die in der Arbeit genannten **Streumatrizen** darzustellen.
In `regiment_plot.ipynb` wird die **Trennung der Exponenten** visualisiert. 
