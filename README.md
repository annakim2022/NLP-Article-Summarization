# NLP-Article-Summarization
## Brief Overview

Our code has five modules representing the different models/methods used to generate our extractive summaries: 
- title_bias_model.py: implentation of the model that took into account and placed an heavier emphasis on terms that appear in the title of the article
- named_entity_recognition.py: implementation of the model that tracks and recognizes named entities and their appearances throughout the article in the form of pronouns
- tfidf_model.py: implementation of the model that compares tfidf vectors
- mixed_model.py: implementation of the model that attempts to utilize all methods used

The models above are called in the article_summarizer.py file which takes a single user input (URL link to a Wikipeidia article) and prints out the summary generated for this article by all five of our models.


## How to compile, set up, deploy, and use your system

To set up the code, start by making a virtual environment utilizing tools such as pip or conda. Then install the requirements listed in the requirements.txt by running the command `pip install -r requirements.txt`. To use the program, navigate to the article_summarizer.py file and run it. The program will prompt you to enter the URL for a Wikipedia article you'd like to have summarized. The article_summarizer.py will go through the models represented by the other five classes and generate five uniquely generated summaries.

## Limitations in your current implementation

This current implementation only works on Wikipedia articles as it splices article titles stored in the '<title>' tag of Wikipedia articles. Wikipedia titles always end with a " - Wikipedia" closing substring. 
