import string

import networkx as nx
import nltk
import simplemma

# from HanTa import HanoverTagger as ht

WHITELIST = string.ascii_lowercase + "äüöß "


def extract_metadata_from_file_name(file_name):
    splitted_name = file_name[:-4].split("_")
    author = splitted_name[0]
    title = splitted_name[1]
    language = splitted_name[2]
    return author, title, language


def prepare_text(text, lemmatize=True, greedy=False):
    text = text.replace("\n", " ").strip().lower()
    text = "".join([c for c in text if c in WHITELIST])
    text = [word for word in text.split(" ") if len(word) > 0]
    if lemmatize:
        text = [simplemma.lemmatize(token, lang='de', greedy=greedy) for token in text]
    return text


####Allgemeine, zusammenfassende Methoden
def prepare_text_with_libraries(text: str, filterNouns=False, remove_stopwords=True, language="de") -> list[str]:
    t = tokenize(text, language=language)
    t = filter_tokens(lemmatize(t, language=language), remove_stopwords=remove_stopwords, language=language)

    return t



# Aktualisierte, verbesserte Methode
def convert_preprocessed_tokens_to_graph(tokens, neighbour_distance):
    graph = nx.Graph()
    total_tokens = len(tokens)

    for i in range(len(tokens) - neighbour_distance):
        for d in range(1, neighbour_distance + 1):
            graph.add_edge(tokens[i], tokens[i + d])

    return graph


# removes stopwords, punctuation, and every non alphabetic token
def filter_tokens(text: list, remove_stopwords=False, language="de") -> list[str]:
    punctuation = set(string.punctuation)
    if not remove_stopwords:
        return [word for word in text if not word.isdigit() and word not in punctuation]
    stop = get_stopwords(language)
    stop_and_punctuation = stop.union(punctuation)
    return [word for word in text if not word.isdigit() and word.lower() not in stop_and_punctuation]


def lemmatize(text: list, greedy=True, language="de"):
    return [simplemma.lemmatize(token, lang=language, greedy=greedy) for token in text]


#### Hilfsmethoden
def tokenize(text: str, language="de"):
    if language == "de":
        lang = "german"
    elif language == "en":
        lang = "english"
    else:
        raise ValueError("language must be de or en")
    return nltk.word_tokenize(text, language=lang)


def get_stopwords(language):
    if language == "de":
        return set(nltk.corpus.stopwords.words("german"))
    elif language == "en":
        return set(nltk.corpus.stopwords.words("english"))
    else:
        raise ValueError("language must be de or en")