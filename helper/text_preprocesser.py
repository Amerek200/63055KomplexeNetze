import string

import networkx as nx
import nltk
import simplemma
# from HanTa import HanoverTagger as ht

WHITELIST = string.ascii_lowercase + "äüöß "


# TAGGER_DE = ht.HanoverTagger('morphmodel_ger.pgz') #for POS Tagging
# TAGGER_EN = ht.HanoverTagger('morphmodel_en.pgz')
#erster Anlauf ohne "ausgiebige" Nutzung anderer Module außer dem Lemmatizer.
#greedy=stronger reduction, might be closer to stemming (Wörter auf Wortstamm) than lemmatization (Flexation -> Grundform)
def prepareText(text, lemmatize=True, greedy=False):
    text = text.replace("\n", " ").strip().lower()
    text = "".join([c for c in text if c in WHITELIST])
    text = [word for word in text.split(" ") if len(word) > 0]
    if lemmatize:
        text = [ simplemma.lemmatize(token, lang='de', greedy=greedy) for token in text ]
    return text


####Allgemeine, zusammenfassende Methoden
def prepareTextWithLibaries(text: str, filterNouns=False, removeStopwords=True, language="de") -> list[str]:
    t = tokenize(text, language=language)
    t = filterTokens(lemmatize(t, language=language), removeStopwords=removeStopwords)

    # Solange imports nicht funktionieren, können auch keine Nomen gefiltert werden

    # if filterNouns:
    #     t = filterNounsAndNames(t)
    # return t

# Neue Methode, für simplere Umwandlung von Tokens in Graph
def convert_preprocessed_tokens_to_graph(tokens):
    graph = nx.Graph()
    total_tokens = len(tokens)

    for i in range(len(tokens) - 1):
        graph.add_edge(tokens[i], tokens[i + 1])

    return graph
def fileToGraph(filename, graph, filterNouns=False, removeStopwords=False, language="de"):
    totalTokens = 0
    with open(filename) as file:
        lastToken = None
        for line in file:
            tokens = prepareTextWithLibaries(line, filterNouns=filterNouns, removeStopwords=removeStopwords, language=language)
            # we have to remember the last token per line to connect with first token of next line
            if len(tokens) > 0:
                if lastToken != None:
                    graph.add_edge(lastToken, tokens[0])
                lastToken = tokens[-1]
                totalTokens = totalTokens + len(tokens)
            for i in range(len(tokens)-1):
                graph.add_edge(tokens[i], tokens[i+1])
    print(str.format("processed {0} tokens in total. Resulting graph has {1} nodes and {2} edges.", totalTokens, len(graph.nodes), len(graph.edges)))
    return graph

#removes stopwords, punctuation, and every non alphabetic token
def filterTokens(text: list, removeStopwords=False, language="de") -> list[str]:
    punctuation = set(string.punctuation)
    if not removeStopwords:
        return [ word for word in text if word.isalpha() and word not in punctuation ]
    stop = getStopwords(language)
    stopAndPunctuation = stop.union(punctuation)
    return [ word for word in text if word.isalpha() and word not in stopAndPunctuation ]

def lemmatize(text: list, greedy=True, language="de"):
    return [ simplemma.lemmatize(token, lang=language, greedy=greedy) for token in text ]

#### Hilfsmethoden
def tokenize(text: str, language="de"):
    if language == "de":
        lang = "german"
    elif language == "en":
        lang = "english"
    else:
        raise ValueError("language must be de or en")
    return nltk.word_tokenize(text, language=lang)

def getStopwords(language):
    if language == "de":
        return set(nltk.corpus.stopwords.words("german"))
    elif language == "en":
        return set(nltk.corpus.stopwords.words("english"))
    else:
        raise ValueError("language must be de or en")

def removeStopwords(text: list, language="de"):
    stop = getStopwords(language)
    return [ word for word in text if word not in stop ]

def removePunctuation(text: list):
    punctuation = string.punctuation
    return [word for word in text if word not in punctuation ]

def removeNonAlphabetToken(text: list):
    return [ word for word in text if word.isalpha() ]

# def filterNounsAndNames(token : list[str], language="de"):
#     keepTags = [ "NN", "NE" ] #NN = Noun, NE = Name
#     return [ word for word in token if any(tag in getTags(word, language=language) for tag in keepTags) ]

#Tagger sollte aus Performancegründen nicht mit jedem Aufruf geladen werden. Daher global.
# def getTags(word, language="de"):
#     if language == "de":
#         tagger = TAGGER_DE
#     elif language == "en":
#         tagger = TAGGER_EN
#     else:
#         raise ValueError("language must be de or en")
#     return [ res[0] for res in tagger.tag_word(word) ] #res[0] = tag, res[1] = propability