import bs4 as bs
import urllib.request
import re
import nltk
import heapq

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm


def generate_summary(url):
    scraped_data = urllib.request.urlopen(url)
    article = scraped_data.read()

    parsed_article = bs.BeautifulSoup(article,'lxml')

    paragraphs = parsed_article.find_all('p')

    article_text = ""

    for p in paragraphs:
        article_text += p.text



    # print(article_text)
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    sentence_list = nltk.sent_tokenize(article_text)
    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1


    maximum_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)


    # Named Entity Recognition
    nlp = en_core_web_sm.load()
    spacy_text = nlp(formatted_article_text)
    labels = [x.label_ for x in spacy_text.ents]
    # print(Counter(labels))

    items = [x.text for x in spacy_text.ents]
    top_entities = {}
    for lst in Counter(items).most_common(10):
        top_entities[lst[0].lower()] = lst[1]
        # print(top_entities)
    #########
    top = 0
    for i in top_entities.values():
        if i > top:
            top = i

    sentence_scores = {}
    ner_modifier = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            ner_modifier_weight = 0
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if word in top_entities.keys():
                        ner_modifier_weight = top_entities[word] / top
                        ner_modifier[sent] = ner_modifier_weight
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word] + ner_modifier_weight
                    else:
                        sentence_scores[sent] += word_frequencies[word] + ner_modifier_weight
                    try:
                        ner_modifier[sent].add(ner_modifier_weight)
                    except:
                        ner_modifier[sent] = ner_modifier_weight

    # print(sentence_scores)
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    # print(summary)
    return summary, ner_modifier