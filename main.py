# Modules
import math
import os
import re

from collections import Counter

# Functions
def Load_Documents():
    Docs = {}
    Counter = 1
    for File in os.listdir("Docs"):
        with open("Docs/" + File, 'rb') as File_Obj:
            Data = File_Obj.read()
        Docs[Counter] = Data.decode()
        Counter += 1

    return Docs

def Tokenizer(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = text.split()
    return tokens

def TF(tokens):
    tf = Counter(tokens)
    total_terms = len(tokens)
    for term in tf:
        tf[term] = tf[term] / total_terms
    return tf

def IDF(all_document_tokens):
    num_of_docs = len(all_document_tokens)
    
    doc_freq = Counter()
    
    for tokens in all_document_tokens.values():
        unique_terms = set(tokens)
        for term in unique_terms:
            doc_freq[term] += 1
        
        idf = {}
        for term, freq in doc_freq.items():
            idf[term] = math.log(num_of_docs / freq)
        
        return idf

def main():
    Collection = Load_Documents()
    Tokens_For_Each = {key:Tokenizer(value) for key,value in Collection.items()}

if __name__ == "__main__":
    main()