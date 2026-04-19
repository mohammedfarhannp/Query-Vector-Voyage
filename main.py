# Modules
import math
import os
import re

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

def main():
    Collection = Load_Documents()
    print(Tokenizer(Collection[1]))

if __name__ == "__main__":
    main()