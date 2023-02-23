#!/usr/bin/env python
# coding: utf-8

# # <center>HW #1: Analyze Documents by Numpy</center>

# <div class="alert alert-block alert-warning">Each assignment needs to be completed independently. Never ever copy others' work (even with minor modification, e.g. changing variable names). Anti-Plagiarism software will be used to check all submissions. </div>

# **Instructions**: 
# - Please read the problem description carefully
# - Make sure to complete all requirements (shown as bullets) . In general, it would be much easier if you complete the requirements in the order as shown in the problem description
# - Follow the Submission Instruction to submit your assignment

# **Problem Description**
# 
# In this assignment, you'll write functions to analyze an article to find out the word distributions and key concepts. 
# 
# The packages you'll need for this assignment include `numpy` and `string`. Some useful functions:
# - string, list, dictionary: `split`, `count`, `index`,`strip`
# - numpy: `sum`, `where`,`log`, `argsort`,`argmin`, `argmax` 

# ## Q1. Define a function to analyze word counts in an input sentence
# 
# 
# Define a function named `tokenize(doc)` which does the following: 
# 
# * accepts a document (i.e., `doc` parameter) as an input
# * first splits a document into paragraphs by delimiter `\n\n` (i.e. two new lines)
# * for each paragraph, 
#     - splits it into a list of tokens by **space** (including tab, and new line). 
#         - e.g., `it's a hello world!!!` will be split into tokens `["it's", "a","hello","world!!!"]`  
#     - removes the **leading/trailing punctuations or spaces** of each token, if any 
#         - e.g., `world!!! -> world`, while `it's` does not change
#         - hint, you can import module *string*, use `string.punctuation` to get a list of punctuations (say `puncts`), and then use function `strip(puncts)` to remove leading or trailing punctuations in each token
#     - a token has at least two characters  
#     - converts all tokens into lower case 
#     - find the count of each unique token and save the count as a dictionary, named `word_dict`, i.e., `{world: 1, a: 1, ...}` 
# * creates another dictionary,say `para_dict`, where a key is the order of each paragraph in `doc`, and the value is the `word_dict` generated from this paragraph
# * returns the dictionary `para_dict` and the paragraphs in the document
#     

# In[1]:


import string
import pandas as pd
import numpy as np

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# In[2]:


import string
puncts = string.punctuation
puncts
para = "it's a hello world!!!"
tokens = para.split(" ")
import re
tokens = [re.sub('[^a-zA-Z0-9 \n\.\']','',each.strip()) for each in tokens]
tokens
tokens1 = [each.strip(puncts) for each in tokens]
tokens1 

t =[(i, v) for i,v in enumerate(tokens1)]
t
a = "it's a hello world!!!\nit is hello world again."
d = a.split()
d


# In[3]:


def tokenize(doc):#accepts a document (i.e., doc parameter) as an input
    
    para_dict, para = None, None
    
    # add your code here
    #first splits a document into paragraphs by delimiter \n\n (i.e. two new lines)
    para = doc.split('\n\n')
    #for each paragraph, splits it into a list of tokens by space (including tab, and new line).
    #e.g., "it's a hello world!!! will be split into tokens ["it's", "a","hello","world!!!"]
    import string
    puncts = string.punctuation
    #find the count of each unique token and save the count as a dictionary, named word_dict, i.e., {world: 1, a: 1, ...}
    def get_tokens(para): 
        tokens = para.split()
        tokens = [each.strip(puncts) for each in tokens]
        tokens = [token.lower() for token in tokens if len(token)>=2]
        word_dict={}
        for a_token in tokens:
            if a_token not in word_dict.keys():
                word_dict[a_token]=1
            else:
                word_dict[a_token] +=1
        return word_dict
    
    para_dict={}
    #creates another dictionary,say para_dict, where a key is the order of each paragraph in doc, 
    #and the value is the word_dict generated from this paragraph
    para_dict = {i : get_tokens(v) for i,v in enumerate(para)}
    #returns the dictionary para_dict and the paragraphs in the document
    return para_dict, para


# In[4]:


# test your code
doc = "it's a hello world!!!\nit is hello world again.\n\nThis is paragraph 2."
tokenize(doc)


# ## Q2. Generate a document term matrix (DTM) as a numpy array
# 
# 
# Define a function `get_dtm(doc)` as follows:
# - accepts a document, i.e., `doc`, as an input
# - uses `tokenize` function you defined in Q1 to get the word dictionary for each paragraph in the document 
# - pools the keys from all the word dictionaries to get a list of  unique words, denoted as `unique_words` 
# - creates a numpy array, say `dtm` with a shape (# of paragraphs x # of unique words), and set the initial values to 0. 
# - fills cell `dtm[i,j]` with the count of the `j`th word in the `i`th paragraph 
# - returns `dtm` and `unique_words`

# In[5]:


def get_dtm(doc):
    dtm, all_words = None, None
    dtm=[]
    all_words=[]
    # add your code here
    #uses tokenize function to get the word dictionary for each paragraph in the document
    para_dict, para = tokenize(doc)
    #pools the keys from all the word dictionaries to get a list of unique words
    for para_tokens in para_dict.values():
        [all_words.append(token) for token in para_tokens if token not in all_words]
    #creates a numpy array, say dtm with a shape (# of paragraphs x # of unique words), and set the initial values to 0.
    dtm = np.zeros((len(para), len(all_words)))
    #fills cell dtm[i,j] with the count of the jth word in the ith paragraph
    for i, para_num in enumerate(para_dict):
        for j, token in enumerate(all_words):
            if token in para_dict[para_num]:
                dtm[i][j] =para_dict[i][token]
    return dtm, all_words


# In[6]:


doc = "it's a hello world!!!\nit is hello world again.\n\nThis is paragraph 2."
tokenize(doc)
dtm, all_words = get_dtm(doc)
dtm
all_words


# ##### A test document. This document can be found at https://www.wboi.org/npr-news/2023-01-26/everybody-is-cheating-why-this-teacher-has-adopted-an-open-chatgpt-policy
# 
# doc = open("chatgpt_npr.txt", 'r').read()
# dtm, all_words = get_dtm(doc)

# In[7]:


doc = open("chatgpt_npr.txt", 'r').read() 
dtm, all_words = get_dtm(doc)


# In[8]:


print(doc)


# In[9]:


# To ensure dtm is correct, check what words in a paragraph have been captured by dtm

p = 6 # paragraph id

[w for i,w in enumerate(all_words) if dtm[p][i]>0] 


# ## Q3 Analyze DTM Array 
# 
# 
# **Don't use any loop in this task**. You should use array operations to take the advantage of high performance computing.
# 

# Define a function named `analyze_dtm(dtm, words, paragraphs)` which:
# * takes an array $dtm$ and $words$ as an input, where $dtm$ is the array you get in Q2 with a shape $(m \times n)$, and $words$ contains an array of words corresponding to the columns of $dtm$.
# * calculates the paragraph frequency for each word $j$, e.g. how many paragraphs contain word $j$. Save the result to array $df$. $df$ has shape of $(n,)$ or $(1, n)$. 
# * normalizes the word count per paragraph: divides word count, i.e., $dtm_{i,j}$, by the total number of words in paragraph $i$. Save the result as an array named $tf$. $tf$ has shape of $(m,n)$. 
# * for each $dtm_{i,j}$, calculates $tfidf_{i,j} = \frac{tf_{i, j}}{1+log(df_j)}$, i.e., divide each normalized word count by the log of the paragraph frequency of the word (add 1 to the denominator to avoid dividing by 0).  $tfidf$ has shape of $(m,n)$ 
# * prints out the following (hint: you can zip words and their values into a list so that there is no need for loop during printing):
#     
#     - the total number of words in the document represented by $dtm$ 
#     - the number of paragraphs and the number of unique words in the document
#     - the most frequent top 10 words in this document    
#     - top-10 words that show in most of the paragraphs, i.e. words with the top 10 largest $df$ values (show words and their $df$ values) 
#     - the shortest paragraph (i.e., the one with the least number of words) 
#     - top-5 words with the largest $tfidf$ values in the longest sentence (show words and values) 
# 
# Note, for all the steps, **do not use any loop**. Just use array functions and broadcasting for high performance computation.
# 
# Your answer may be different from the example output, since words may have the same values in the dtm but are kept in positions

# In[196]:


def analyze_dtm(dtm, words, paragraphs):
    
    # add your code here
    # calculates the paragraph frequency for each word  𝑗, e.g. how many paragraphs contain word  𝑗. Save the result to array  𝑑𝑓. 𝑑𝑓 has shape of  (𝑛,) or  (1,𝑛)
    frequency = np.sum(dtm, axis=0) 
    dtm1 = np.where(dtm, 1, 0)
    df = np.sum(dtm1, axis=0) #paragraph frequency for each word  
    #print("shape of dtm - ", dtm.shape, dtm1.shape)
    #print("shape of df - ", df.shape)
    tf = np.divide(dtm, np.sum(dtm, axis=1, keepdims = True))#normalizes the word count per paragraph: divides word count, i.e.,  𝑑𝑡𝑚𝑖,𝑗  by the total number of words in paragraph  𝑖
    #print("tf shape - ", tf.shape)
    tfidf = tf/(1+np.log(df)) #for each  𝑑𝑡𝑚𝑖,𝑗 , calculates  𝑡𝑓𝑖𝑑𝑓𝑖,𝑗=𝑡𝑓𝑖,𝑗1+𝑙𝑜𝑔(𝑑𝑓𝑗)
    #print("tfIDF shape - ", tfidf.shape)
    
    fx = frequency.argsort()
    dfx = df.argsort()
    top10_frequencies = frequency[fx][:-10:-1]
    top10_words = words[fx][:-10:-1]
    top10_df_values = df[dfx][:-10:-1]
    top10_df_words = words[dfx][:-10:-1]
    
    #shortest paragraph --
    para_words = np.sum(dtm, axis=1)
    location_shortpara = np.argsort(para_words)[0]
    location_longpara = np.argsort(para_words)[-1]
    #longest paragraph -- 
    tfidf_values = tfidf[location_longpara]
    tfidfx  = np.argsort(tfidf_values)
    
    top5_tfidf_values = tfidf_values[tfidfx]
    top5_words = words[tfidfx]
    
    print("\nThe total number of words:\n",np.sum(dtm)) #the total number of words in the document represented by  𝑑𝑡𝑚
    print("\nthe number of paragraphs:", dtm.shape[0],", the number of unique words in the document: ",dtm.shape[1])  #the number of paragraphs and the number of unique words in the document
    print("\nThe top 10 frequent words:\n", list(zip(top10_words, top10_frequencies))) #the most frequent top 10 words in this document
    print("\nThe top 10 words with highest df values:\n", list(zip(top10_df_words, top10_df_values)))
    print("\nThe shortest paragraph :\n", paragraphs[location_shortpara])
    print("\nThe top 5 words with the highest tf-idf values in the longest paragraph:\n",list(zip(top5_words[-5:],top5_tfidf_values[-5:])))


# In[197]:


para_dict, paragraphs = tokenize(doc)

# convert words in numpy arrays so that you can use array slicing
words = np.array(all_words)

analyze_dtm(dtm, words, paragraphs)


# ## Q4. Find co-occuring words (Bonus) 
# 
# Can you leverage $dtm$ array you generated to find what words frequently coocur with a specific word? For example, "students" and "chatgpt" coocur in 4 paragraphs. 
# 
# Define a function `find_coocur(w1, w2, dtm, words)`, which returns the paragraphs containong both words w1 and w2.
# 
# Use a pdf file to describe your ideas and also implement your ideas. Again, `DO NOT USE LOOP`! 
# 

# In[253]:


def find_coocur(w1, w2, dtm, words, paragraphs):
    
    result = []
    # add your code here
    # find location of the words having both words
    w1_index = np.where(words == w1)[0]
    w2_index = np.where(words == w2)[0]
    
    #get the dtm matrix of both locations
    w1_dtm = dtm[:,w1_index]
    w2_dtm = dtm[:,w2_index]
    
    #get arrays of satisfying conditions
    para_position = np.where((w1_dtm!=0) & (w2_dtm!=0))[0]
     
    #get the paragra[hs location with matching para_position wher eboth words occur
    result = np.array(paragraphs)[para_position]
    return result


# In[254]:


ps = find_coocur('chatgpt','students',dtm, words, paragraphs)
len(ps)
ps


# **Put everything together and test using main block**

# In[255]:


# best practice to test your class
# if your script is exported as a module,
# the following part is ignored
# this is equivalent to main() in Java

if __name__ == "__main__":  
    
    # Test Question 1
    doc = "it's a hello world!!!\nit is hello world again.\n\nThis is paragraph 2."
    print("Test Question 1")
    para_dict, paragraphs = tokenize(doc)
    print(tokenize(doc))
    
    
    # Test Question 2
    print("\nTest Question 2")
    dtm, all_words = get_dtm(doc)

    print(dtm)
    print(all_words)
    
    
    #3 Test Question 3
    
    doc = open("chatgpt_npr.txt", 'r').read()
    
    para_dict, paragraphs = tokenize(doc)
    dtm, all_words = get_dtm(doc)

    print("\nTest Question 3")
    words = np.array(all_words)

    tfidf = analyze_dtm(dtm, words, paragraphs)


# In[ ]:





# In[ ]:




