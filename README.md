# NLP-Article-Summarization
## Brief Overview

Our code has five modules representing the different models/methods used to generate our extractive summaries: 
- title_bias_model.py: implentation of the model that took into account and placed an heavier emphasis on terms that appear in the title of the article
- named_entity_recognition.py: implementation of the model that tracks and recognizes named entities and their appearances throughout the article in the form of pronouns
- tfidf_model.py: implementation of the model that compares tfidf vectors
- mixed_model.py: implementation of the model that attempts to utilize all methods used

The models above are called in the article_summarizer.py file which takes a single user input (URL link to a Wikipeidia article) and prints out the summary generated for this article by all five of our models.


## How to compile, set up, deploy, and use your system


## Limitations in your current implementation
