import bs4 as bs
from bs4 import BeautifulSoup
from nltk.tag.brill import Word
import requests
import urllib.request   
import re
import nltk
import heapq

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

def format_title(url):
    scraped_data = urllib.request.urlopen(url)
    article = scraped_data.read()

    parsed_article = bs.BeautifulSoup(article,'lxml')
    reqs = requests.get(url)
    parser = BeautifulSoup(reqs.text, 'html.parser')

    # Parse through HTML Title Tag -> article_title
    article_title = ""
    for title in parser.find_all('title'):
        article_title += (title.get_text())

    article_title = article_title[:len(article_title)-12] # cut out the ' - Wikepedia' substring at the end of every title

    article_title = re.sub(r'\[[0-9]*\]', ' ', article_title)
    article_title = re.sub(r'\s+', ' ', article_title)
    formatted_article_title = re.sub('[^a-zA-Z]', ' ', article_title)
    formatted_article_title = re.sub(r'\s+', ' ', formatted_article_title)
    return formatted_article_title, article_title

stopwords = nltk.corpus.stopwords.words('english')

def calculate_title_term_frequencies(formatted_article_title):
    title_term_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_title):
        if word not in stopwords:
            if word not in title_term_frequencies:
                title_term_frequencies[word] = 1
            else:
                title_term_frequencies += 1
    return title_term_frequencies

def freq_in_title(term, title_term_frequencies):
    freq = 0
    try:
        freq = title_term_frequencies[term]
    except:
        pass
    return freq

def format_article(url):
    scraped_data = urllib.request.urlopen(url)
    article = scraped_data.read()

    parsed_article = bs.BeautifulSoup(article,'lxml')

    paragraphs = parsed_article.find_all('p')

    article_text = ""

    for p in paragraphs:
        article_text += p.text

    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    sentence_list = nltk.sent_tokenize(article_text)
    return formatted_article_text, sentence_list

def calculate_word_frequencies(formatted_article_text):
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    return word_frequencies

stopwords = nltk.corpus.stopwords.words('english')

def title_biased_sentence_scores(sentence_list, word_frequencies, title_term_frequencies):
    sentence_scores = {}
    title_biased_modifiers = {}
    for sent in sentence_list:
        num_title_terms = 0
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    title_biased_modifier = (freq_in_title(word, title_term_frequencies)*.3)
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word] + title_biased_modifier
                        num_title_terms += 1
                    else:
                        sentence_scores[sent] += word_frequencies[word] + title_biased_modifier
                        num_title_terms += 1
        try:
            title_biased_modifiers[sent] = title_biased_modifier * num_title_terms
        except:
            pass
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

def generate_summary(url):
    article_title = format_title(url)[1]
    formatted_title = format_title(url)[0]
    title_term_frequencies = calculate_title_term_frequencies(formatted_title)
    maximum_title_frequency = max(title_term_frequencies.values())
    for word in title_term_frequencies.keys():
        title_term_frequencies[word] = (title_term_frequencies[word]/maximum_title_frequency)
    
    text = format_article(url)[0]
    sentences = format_article(url)[1]
    word_frequencies = calculate_word_frequencies(text)
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)
    title_biased_modifiers = title_biased_sentence_scores(sentences, word_frequencies, title_term_frequencies)[1]
    return title_biased_sentence_scores(sentences, word_frequencies, title_term_frequencies), title_biased_modifiers