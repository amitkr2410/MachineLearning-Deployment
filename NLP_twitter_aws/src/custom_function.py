# Text Pre-processing using "stopwords" from NLTK corpus library
#Tokenization is a term used to describe the normal text strings into a list of tokens or base words
# As a first step, let's write a function that will split a message into its individual words 
# and return a list. We'll also remove very common words, ('the', 'a', etc..). 
# To do this we will take advantage of the NLTK library. It's pretty much the standard library 
# in Python for processing text and has a lot of useful features. 
# We'll only use some of the basic ones here.
#We will also remove prefix and suffix using PorterStemmer
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def text_process(message):
    """
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove all stopwords using nltk stopwords
    3. Remove prefix and suffix using PorterStemmer
    4. Returns a list of the cleaned text
    """
    newstring_list = []
    newstring = ""
    ans = newstring
    # Check characters to see if they are in punctuation or numbers
    for j in message:
        if j.isalpha():
            newstring_list.append(j)
        elif j in string.punctuation:
            newstring_list.append(" ") 
        else:
            newstring_list.append(" ")
    # Join the characters again to form the string.        
    newstring = "".join(newstring_list)
    #print(newstring)
    ans = newstring
    newstring = ""
    
    #We'll  remove very common words, ('the', 'a', etc..) using stopwords
    STOPWORDS = stopwords.words('english') + ['http', 'www', '', 'u', 'ü', 'ur', '4', '2', 'im', 'dont', 'doin', 'ure']
    ps = PorterStemmer()
    
    for word in ans.split(): 
        #print(word, len(word))
        if (word.lower() not in STOPWORDS) and  ( len(word)!=1):
            if (len(ps.stem(word)) < 15):
                newstring = newstring + str( ps.stem(word) + " ") 
    ans = newstring
    newstring = ""
    #print(ans)
    
    return ans

