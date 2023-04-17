# -*- coding: utf-8 -*-
"""HW_3-Answer-KY.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pa5Bk_fZ3st4E0247JY2AruSoWd2gyE8

# HW3: Natural Language Processing

<div class="alert alert-block alert-warning">Each assignment needs to be completed independently. Never ever copy others' work (even with minor modification, e.g. changing variable names). Anti-Plagiarism software will be used to check all submissions. </div>

## Problem Description

In this assignment, we'll use what we learned in NLP module to compare ChatGPT-generated text with human-generated answers. A dataset with 200 questions and answers has been provided for you to use. The dataset can be found at https://huggingface.co/datasets/Hello-SimpleAI/HC3.


Please follow the instruction below to do the assessment step by step and answer all analysis questions.
"""

import pandas as pd

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

data = pd.read_csv("qa.csv")
data.head()

"""## Q1. Tokenize function

Define a function `tokenize(docs, lemmatized = True, remove_stopword = True, remove_punct = True)`  as follows:
   - Take three parameters: 
       - `docs`: a list of documents (e.g. questions)
       - `lemmatized`: an optional boolean parameter to indicate if tokens are lemmatized. The default value is True (i.e. tokens are lemmatized).
       - `remove_stopword`: an optional bookean parameter to remove stop words. The default value is True (i.e. remove stop words). 
   - Split each input document into unigrams and also clean up tokens as follows:
       - if `lemmatized` is turned on, lemmatize all unigrams.
       - if `remove_stopword` is set to True, remove all stop words.
       - if `remove_punct` is set to True, remove all punctuation tokens.
       - remove all empty tokens and lowercase all the tokens.
   - Return the list of tokens obtained for each document after all the processing. 
   
(Hint: you can use spacy package for this task. For reference, check https://spacy.io/api/token#attributes)
"""

import spacy 
nlp = spacy.load('en_core_web_sm')

def tokenize(docs, lemmatized=True, remove_stopword=True, remove_punct = True):   
    tokenized_docs = []
    for single_doc in docs:
      doc = nlp(single_doc)
      single_tokenized_docs =[]
      for word in doc:
        if lemmatized:
          add_word = str(word.lemma_)
        else:
          add_word = str(word)
        if remove_stopword:
          if word.is_stop:
            continue
        if remove_punct:
          if word.is_punct:
            continue
        single_tokenized_docs.append(add_word.lower())
      tokenized_docs.append(single_tokenized_docs)
    return tokenized_docs

# For simplicity, We will test one document

#print(data["question"].iloc[0] + "\n")
"""
print(f"1.lemmatized=True, remove_stopword=False, remove_punct = True:\n \
{tokenize(data['question'].iloc[0:1], lemmatized=True, remove_stopword=False, remove_punct = True)}\n")
"""


print(f"1.lemmatized=True, remove_stopword=False, remove_punct = True:\n \
{tokenize(data['question'].iloc[0:1], lemmatized=True, remove_stopword=False, remove_punct = True)}\n")

print(f"2.lemmatized=True, remove_stopword=True, remove_punct = True:\n \
{tokenize(data['question'].iloc[0:1], lemmatized=True, remove_stopword=True, remove_punct = True)}\n")

print(f"3.lemmatized=False, remove_stopword=False, remove_punct = True:\n \
{tokenize(data['question'].iloc[0:1], lemmatized=False, remove_stopword=False, remove_punct = True)}\n")

print(f"4.lemmatized=False, remove_stopword=False, remove_punct = False:\n \
{tokenize(data['question'].iloc[0:1], lemmatized=False, remove_stopword=False, remove_punct = False)}\n")

"""Test your function with different parameter configuration and observe the differences in the resulting tokens."""

# For simplicity, We will test one document

print(data["question"].iloc[0] + "\n")

print(f"1.lemmatized=True, remove_stopword=False, remove_punct = True:\n \
{tokenize(data['question'].iloc[0:1], lemmatized=True, remove_stopword=False, remove_punct = True)}\n")

print(f"2.lemmatized=True, remove_stopword=True, remove_punct = True:\n \
{tokenize(data['question'].iloc[0:1], lemmatized=True, remove_stopword=True, remove_punct = True)}\n")

print(f"3.lemmatized=False, remove_stopword=False, remove_punct = True:\n \
{tokenize(data['question'].iloc[0:1], lemmatized=False, remove_stopword=False, remove_punct = True)}\n")

print(f"4.lemmatized=False, remove_stopword=False, remove_punct = False:\n \
{tokenize(data['question'].iloc[0:1], lemmatized=False, remove_stopword=False, remove_punct = False)}\n")

"""## Q2. Sentiment Analysis


Let's check if there is any difference in sentiment between ChatGPT-generated and human-generated answers.


Define a function `compute_sentiment(generated, reference, pos, neg )` as follows:
- take four parameters:
    - `gen_tokens` is the tokenized ChatGPT-generated answers by the `tokenize` function in Q1.
    - `ref_tokens` is the tokenized human answers by the `tokenize` function in Q1.
    - `pos` (`neg`) is the list of positive (negative) words, which can be find in Canvas NLP module.
- for each ChatGPT-generated or human answer, compute the sentiment as `(#pos - #neg )/(#pos + #neg)`, where `#pos`(`#neg`) is the number of positive (negative) words found in each answer. If an answer contains none of the positive or negative words, set the sentiment to 0.
- return the sentiment of ChatGPT-generated and human answers as two columns of DataFrame.


Analysis: 
- Try different tokenization parameter configurations (lemmatized, remove_stopword, remove_punct), and observe how sentiment results change.
- Do you think, in general, which tokenization configuration should be used? Why does this configuration make the most senese?
- Do you think, overall, ChatGPT-generated answers are more posive or negative than human answers? Use data to support your conclusion.

"""

gen_tokens = tokenize(data["chatgpt_answer"], lemmatized=False, remove_stopword=False, remove_punct = False)
ref_tokens = tokenize(data["human_answer"], lemmatized=False, remove_stopword=False, remove_punct = False)

pos = pd.read_csv("positive-words.txt", header = None)
pos.head()

neg = pd.read_csv("negative-words.txt", header = None)
neg.head()

def compute_sentiment(gen_tokens, ref_tokens, pos, neg ):
    result = None
    g_positive_tokens = g_negative_tokens = []
    r_positive_tokens = r_negative_tokens = []
    # add your code here
    gen_sentiment = []
    for generated in gen_tokens:
      g_positive_tokens = g_negative_tokens = []
      g_positive_tokens = [token for token in generated if token in pos]
      g_negative_tokens = [token for token in generated if token in neg]
      # (#pos - #neg )/(#pos + #neg)
      try :
        generated_sentiment = (len(g_positive_tokens)- len(g_negative_tokens))/(len(g_positive_tokens)+len(g_negative_tokens))
        gen_sentiment.append(generated_sentiment)
      except ZeroDivisionError:
        gen_sentiment.append(0)
    ref_sentiment = []
    for reference in ref_tokens:
      r_positive_tokens = r_negative_tokens = []
      r_positive_tokens = [token for token in reference if token in pos]
      r_negative_tokens = [token for token in reference if token in neg]
      # (#pos - #neg )/(#pos + #neg)
      try :
        reference_sentiment = (len(r_positive_tokens)- len(r_negative_tokens))/(len(r_positive_tokens)+len(r_negative_tokens))
        ref_sentiment.append(reference_sentiment)
      except ZeroDivisionError:
        ref_sentiment.append(0)
      
    result = pd.DataFrame({'gen_sentiment':gen_sentiment, 'ref_sentiment':ref_sentiment})
    return result

result = compute_sentiment(gen_tokens, 
                           ref_tokens, 
                           pos[0].values,
                           neg[0].values)
result.head()

result = compute_sentiment(gen_tokens, 
                           ref_tokens, 
                           pos[0].values,
                           neg[0].values)
result.head()

"""## Q3: Performance Evaluation


Next, we evaluate how accurate the ChatGPT-generated answers are, compared to the human-generated answers. One widely used method is to calculate the `precision` and `recall` of n-grams. For simplicity, we only calculate bigrams here. You can try unigram, trigram, or n-grams in the same way.


Define a funtion `bigram_precision_recall(gen_tokens, ref_tokens)` as follows:
- take two parameters:
    - `gen_tokens` is the tokenized ChatGPT-generated answers by the `tokenize` function in Q1.
    - `ref_tokens` is the tokenized human answers by the `tokenize` function in Q1.
- generate bigrams from each tokenized document in `gen_tokens` and `ref_tokens`.
- for each pair of ChatGPT-generated and human answers: 
    - find the overlapping bigrams between them.
    - compute `precision` as the number of overlapping bigrams divided by the total number of bigrams from the ChatGPT-generated answer. In other words, the bigram in the ChatGPT-generated answer is considered as a predicted value. The `precision` measures the percentage of correctly generated bigrams out of all the generated bigrams.
    - compute `recall` as the number of overlapping bigrams divided by the total number of bigrams from the human answer. In other words, the `recall` measures the percentage of bigrams from the human answer can be successfully retrieved.
- return the precision and recall for each pair of answers.


Analysis: 
- Try different tokenization parameter configurations (lemmatized, remove_stopword, remove_punct), and observe how precison and recall change.
- Which tokenization configuration can render the highest average precision and recall scores across all questions?
- Do you think, overall, ChatGPT is able to mimic human in answering these questions?


"""

def bigram_precision_recall(gen_tokens, ref_tokens):
    
    result = None
    # add your code here
    import nltk
    ob=[]
    for g,r in zip(gen_tokens, ref_tokens):
      gen_bigrams = nltk.bigrams(g)
      ref_bigrams = nltk.bigrams(r)
      g_bigram_value = [(x,y) for (x,y) in gen_bigrams ]
      r_bigram_value = [(x,y) for (x,y) in ref_bigrams ]
      overlapping_bigram = [(x,y) for (x,y) in r_bigram_value if (x,y) in g_bigram_value ]
      #the percentage of correctly generated bigrams out of all the generated bigrams
      precision = len(overlapping_bigram)/len(g_bigram_value)
      #measures the percentage of bigrams from the human answer can be successfully retrieved.
      recall = len(overlapping_bigram)/len(r_bigram_value)
      ob.append((overlapping_bigram,precision, recall))
    result = pd.DataFrame(ob, columns =["overlapping", "precision", "recall"])
    return result

result = bigram_precision_recall(gen_tokens, ref_tokens)
result.head()

result = bigram_precision_recall(gen_tokens, 
                                 ref_tokens)
result.head()

"""## Q4 Compute TF-IDF

Define a function `compute_tf_idf(tokenized_docs)` as follows: 
- Take paramter `tokenized_docs`, i.e., a list of tokenized documents by `tokenize` function in Q1
- Calculate tf_idf weights as shown in lecture notes (Hint: feel free to reuse the code segment in NLP Lecture Notes (II))
- Return the smoothed normalized `tf_idf` array, where each row stands for a document and each column denotes a word. 
"""

import nltk
#nltk.download()

def compute_tfidf(tokenized_docs):
    # add your code here
    import numpy as np
    from sklearn.preprocessing import normalize
    import nltk, re, string

    smoothed_tf_idf = None

    def get_doc_tokens(doc):
        token_count={token:doc.count(token) for token in set(doc)}
        return token_count
    docs_tokens={idx:get_doc_tokens(doc) \
             for idx,doc in enumerate(tokenized_docs)} 
    dtm = pd.DataFrame.from_dict(docs_tokens,orient="index")
    dtm = dtm.fillna(0)
    # sort by index (i.e. doc id)
    dtm = dtm.sort_index(axis = 0)
    # convert dtm to numpy arrays
    tf=dtm.values
    # sum the value of each row
    doc_len=tf.sum(axis=1)
    doc_len[:,None]
    # divide dtm matrix by the doc length matrix
    tf=np.divide(tf, doc_len[:,None])
    # set float precision to print nicely
    np.set_printoptions(precision=2)
    df=np.where(tf>0,1,0)
    smoothed_idf=np.log(np.divide(len(tokenized_docs)+1, np.sum(df, axis=0)+1))+1
    smoothed_tf_idf=normalize(tf*smoothed_idf)
    return smoothed_tf_idf

question_tokens = tokenize(data["question"], lemmatized=True, remove_stopword=False, remove_punct = True)
dtm = compute_tfidf(question_tokens)
print(f"1.lemmatized=True, remove_stopword=False, remove_punct = True:\n \
Shape: {dtm.shape}\n")

question_tokens = tokenize(data["question"], lemmatized=True, remove_stopword=True, remove_punct = True)
dtm = compute_tfidf(question_tokens)
print(f"2.lemmatized=True, remove_stopword=True, remove_punct = True:\n \
Shape: {dtm.shape}\n")

question_tokens = tokenize(data["question"], lemmatized=False, remove_stopword=False, remove_punct = True)
dtm = compute_tfidf(question_tokens)
print(f"3.lemmatized=False, remove_stopword=False, remove_punct = True:\n \
Shape: {dtm.shape}\n")

question_tokens = tokenize(data["question"], lemmatized=False, remove_stopword=False, remove_punct = False)
dtm = compute_tfidf(question_tokens)
print(f"4.lemmatized=False, remove_stopword=False, remove_punct = False:\n \
Shape: {dtm.shape}\n")

"""Try different tokenization options to see how these options affect TFIDF matrix:"""

# Test tfidf generation using questions

question_tokens = tokenize(data["question"], lemmatized=True, remove_stopword=False, remove_punct = True)
dtm = compute_tfidf(question_tokens)
print(f"1.lemmatized=True, remove_stopword=False, remove_punct = True:\n \
Shape: {dtm.shape}\n")

question_tokens = tokenize(data["question"], lemmatized=True, remove_stopword=True, remove_punct = True)
dtm = compute_tfidf(question_tokens)
print(f"2.lemmatized=True, remove_stopword=True, remove_punct = True:\n \
Shape: {dtm.shape}\n")

question_tokens = tokenize(data["question"], lemmatized=False, remove_stopword=False, remove_punct = True)
dtm = compute_tfidf(question_tokens)
print(f"3.lemmatized=False, remove_stopword=False, remove_punct = True:\n \
Shape: {dtm.shape}\n")

question_tokens = tokenize(data["question"], lemmatized=False, remove_stopword=False, remove_punct = False)
dtm = compute_tfidf(question_tokens)
print(f"4.lemmatized=False, remove_stopword=False, remove_punct = False:\n \
Shape: {dtm.shape}\n")

"""## Q5. Assess similarity. 


Define a function `assess_similarity(question_tokens, gen_tokens, ref_tokens)`  as follows: 
- Take three inputs:
   - `question_tokens`: tokenized questions by `tokenize` function in Q1
   - `gen_tokens`: tokenized ChatGPT-generated answers by `tokenize` function in Q1
   - `ref_tokens`: tokenized human answers by `tokenize` function in Q1
- Concatenate these three token lists into a single list to form a corpus
- Calculate the smoothed normalized tf_idf matrix for the concatenated list using the `compute_tfidf` function defined in Q3.
- Split the tf_idf matrix into sub-matrices corresponding to `question_tokens`, `gen_tokens`, and `ref_tokens` respectively
- For each question, find its similarities to the paired ChatGPT-generated answer and human answer.
- For each pair of ChatGPT-generated answer and human answer, find their similarity
- Print out the following:
    - the question which has the largest similarity to the ChatGPT-generated answer.
    - the question which has the largest similarity to the human answer.
    - the pair of ChatGPT-generated and human answers which have the largest similarity.
- Return a DataFrame with the three columns for the similarities among questions and answers.



Analysis: 
- Try different tokenization parameter configurations (lemmatized, remove_stopword, remove_punct), and observe how similarities change.
- Based on similarity, do you think ChatGPT-generate answers are more (or less) relevant to questions than human answers?
"""

from sklearn.metrics.pairwise import cosine_similarity

def assess_similarity(question_tokens, gen_tokens, ref_tokens):
    from sklearn.metrics import pairwise_distances
    import numpy as np
    result = None
    
    # Add your code here
    corpus = question_tokens+gen_tokens+ref_tokens
    smoothed_normalized_tf_idf = compute_tfidf(corpus)
    print(smoothed_normalized_tf_idf)
    
    question_tokens_tfidf = compute_tfidf(question_tokens)
    gen_tokens_tfidf = compute_tfidf(gen_tokens)
    ref_tokens_tfidf = compute_tfidf(ref_tokens)

    question_token_sim = 1-pairwise_distances(question_tokens_tfidf, metric = 'cosine')
    question_gen_sim = 1-pairwise_distances(gen_tokens_tfidf, metric = 'cosine')
    gen_ref_sim = 1-pairwise_distances(ref_tokens_tfidf, metric = 'cosine')
    
    np.argsort(question_token_sim)[:,::-1][0,0:2]
    np.argsort(question_gen_sim)[:,::-1][0,0:2]
    np.argsort(gen_ref_sim)[:,::-1][0,0:2]
 

    question_tokens_tfidf= question_tokens[smoothed_normalized_tf_idf]
    gen_tokens_tfidf = gen_tokens[smoothed_normalized_tf_idf]
    ref_tokens_tfidf = ref_tokens[smoothed_normalized_tf_idf]

    question_token_sim = 1-pairwise_distances(question_tokens_tfidf, metric = 'cosine')
    question_gen_sim = 1-pairwise_distances(gen_tokens_tfidf, metric = 'cosine')
    gen_ref_sim = 1-pairwise_distances(ref_tokens_tfidf, metric = 'cosine')
    

    #result = pd.DataFrame({question_token_sim, question_gen_sim,gen_ref_sim})  

    
    """
    Split the tf_idf matrix into sub-matrices corresponding to question_tokens, gen_tokens, and ref_tokens respectively
    For each question, find its similarities to the paired ChatGPT-generated answer and human answer.
    For each pair of ChatGPT-generated answer and human answer, find their similarity
    Print out the following:

    the question which has the largest similarity to the ChatGPT-generated answer.
    the question which has the largest similarity to the human answer.
    the pair of ChatGPT-generated and human answers which have the largest similarity.
    Return a DataFrame with the three columns for the similarities among questions and answers.
    """
    return result

# Once case is tested here. 

question_tokens = tokenize(data["question"], lemmatized=False, remove_stopword=False, remove_punct = False)
gen_tokens = tokenize(data["chatgpt_answer"], lemmatized=False, remove_stopword=False, remove_punct = False)
ref_tokens = tokenize(data["human_answer"], lemmatized=False, remove_stopword=False, remove_punct = False)

result = assess_similarity(question_tokens, gen_tokens, ref_tokens)
result.head()

# You need to test other cases so that you can answer the analysis questions

# Once case is tested here. 

question_tokens = tokenize(data["question"], lemmatized=False, remove_stopword=False, remove_punct = False)
gen_tokens = tokenize(data["chatgpt_answer"], lemmatized=False, remove_stopword=False, remove_punct = False)
ref_tokens = tokenize(data["human_answer"], lemmatized=False, remove_stopword=False, remove_punct = False)

result = assess_similarity(question_tokens, gen_tokens, ref_tokens)
result.head()

# You need to test other cases so that you can answer the analysis questions

"""## Q6 (Bonus): Further Analysis (Open question)


- Can you find at least three significant differences between ChatGPT-generated and human answeres? Use data to support your answer.
- Based on these differences, are you able to design a classifier to identify ChatGPT generated answers? Implement your ideas using traditional machine learning models, such as SVM, decision trees.

## Test

Please move all your unit tests into the main block to make grading easy!
"""

if __name__ == "__main__":  
    
    # Test queston 1:
    print("# Test queston 1:")
    question_tokens = tokenize(data["question"], lemmatized=False, remove_stopword=False, remove_punct = False)
    gen_tokens = tokenize(data["chatgpt_answer"], lemmatized=False, remove_stopword=False, remove_punct = False)
    ref_tokens = tokenize(data["human_answer"], lemmatized=False, remove_stopword=False, remove_punct = False)
    
    # Test question 2
    print("# Test question 2")
    #pos = pd.read_csv("../Notes/NLP/positive-words.txt", header = None)
    #neg = pd.read_csv("../Notes/NLP/negative-words.txt", header = None)
    pos = pd.read_csv("positive-words.txt", header = None)
    neg = pd.read_csv("negative-words.txt", header = None)

    result = compute_sentiment(gen_tokens, 
                           ref_tokens, 
                           pos[0].values,
                           neg[0].values)
    print(result.head())
    
    # Test question 3
    print("# Test question 3")
    result = bigram_precision_recall(gen_tokens, 
                                 ref_tokens)
    print(result.head())
    
    
    # Test question 4
    print("# Test question 4")
    dtm = compute_tfidf(question_tokens)
    print(f"1.lemmatized=False, remove_stopword=False, remove_punct = False:\n \
    Shape: {dtm.shape}\n")
    
    # Test question 5
    print("# Test question 5")
    result = assess_similarity(question_tokens, gen_tokens, ref_tokens)
    print(result.head())
