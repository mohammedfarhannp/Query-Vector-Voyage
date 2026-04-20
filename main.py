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

def TF_IDF_Vector(tf, idf):
    tfidf = {}
    for term, tf_value in tf.items():
        if term in idf:
            tfidf[term] += tf_value * idf[term]
    return tfidf

def COSINE_Similarity(vector_1, vector_2):
    all_terms = set(vector_1.keys()) | set(vector_2.keys())
    
    v1 = [vector_1.get(term, 0) for term in all_terms]
    v2 = [vector_2.get(term, 0) for term in all_terms]
    
    dot_product = sum(a * b for a, b in zip(v1, v2))
    
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    return dot_product / (mag1 * mag2)
    

def Process_Query(query, all_tfidf_vectors, idf):
    query_tokens = Tokenizer(query)
    query_tf = TF(query_tokens)
    query_tfidf = TF_IDF_Vector(TF, idf)
    
    similarities = {}
    for doc_id, doc_vector in all_tfidf_vectors.items():
        similarity = COSINE_Similarity(query_tfidf, doc_vector)
        similarities[doc_id] = similarity

    return similarities

def Rank(similarities):
    ranked = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    return ranked

def Display_Results(similarities, ranked_docs, documents):
    print("\n" + "="*60)
    print("COSINE SIMILARITY SCORES")
    print("="*60)
    for doc_id, score in similarities.items():
        print(f"Document {doc_id}: {score:.4f}")
    
    print("\n" + "="*60)
    print("RANKED DOCUMENTS (Most Relevant First)")
    print("="*60)
    for rank, (doc_id, score) in enumerate(ranked_docs, 1):
        # Show first 100 characters of document as preview
        preview = documents[doc_id][:100].replace('\n', ' ') + "..."
        print(f"{rank}. Document {doc_id} (Score: {score:.4f})")
        print(f"   Preview: {preview}\n")

def main():
    Collection = Load_Documents()
    Tokens_For_Each = {key:Tokenizer(value) for key,value in Collection.items()}
    idf = IDF(Tokens_For_Each)
    

if __name__ == "__main__":
    main()