#import library
import numpy as np
import math
import pandas as pd
import re
from collections import Counter
import os

def reg_text(Text):
    sentences = Text.str.lower().str.replace('[^\w\s]', '').str.split('.')
    word = []
    for i in range(len(sentences)):
        word.append(''.join(sentences[i]).split())
        word[i].insert(0, '<s>')
        word[i].append('</s>')
    texts = []
    for i in range(len(word)): 
        for j in range (len(word[i])):
            texts.append(word[i][j]) 
    return texts

def buildUnigramModel(Text):
    '''
    BUILD UNIGRAM MODEL
    IS : Diberikan input sebuah data berisi text
    FS : Meng-outputkan hasil dari model unigram yang dibuat dalam bentuk dictionary (key: kata; value: probabilitas kemunculan kata tersebut)
    Note : Lakukan proses cleaning dengan menghapus punctuation dan mengubah teks menjadi lower case.
    '''
    texts = reg_text(Text)
    len_text = len(texts)
    unigram = dict(Counter(texts))
    unigram.update((x, y/len_text) for x, y in unigram.items())
    return unigram
   
def buildBigramModel(Text):
    '''
    BUILD BIGRAM MODEL
    IS : Diberikan input sebuah data berisi text
    FS : Meng-outputkan hasil dari model bigram yang dibuat dalam bentuk dictionary (key: pasangan kata; value: probabilitas kemunculan pasangan kata tersebut)
    Note : Lakukan proses cleaning dengan menghapus punctuation dan mengubah teks menjadi lower case.
    '''
    texts = reg_text(Text)
    counts = dict(Counter(texts))
    bigram = dict(Counter(zip(texts, texts[1:])))
    i = 0
    for x,y in bigram.items():
        bigram[x] = y/counts.get(list(bigram.keys())[i][0])
        i += 1
    return bigram

def nextBestWord(bigramModel, currentWord):
    '''
    MENAMPILKAN NEXT BEST WORD
    IS : Menerima input sebuah kata
    FS : Meng-outputkan kata berikutnya yang memiliki probabilitas tertinggi berdasarkan model bigram
    '''
    list_key = list(bigramModel.keys())
    list_value = list(bigramModel.values())
    list_words_value = []
    list_words_key= []
    i = 0
    for i in range(len(list_key)):
        if (list_key[i][0] == currentWord):
            list_words_value.append(list_value[i])
            list_words_key.append(list_key[i][1])
    return list_words_key[list_words_value.index(max(list_words_value))]

def nextTenBestWords(bigramModel, currentWord):
    '''
    MENYIMPAN TOP 10 NEXT BEST WORD
    IS : Menerima input sebuah kata
    FS : Menghasilkan list berisi 10 kata berikutnya (beserta probabilitasnya) dengan probabilitas tertinggi berdasarkan model bigram. 
    '''
    list_key = list(bigramModel.keys())
    list_value = list(bigramModel.values())
    list_words = []
    i = 0
    for i in range(len(list_key)):
        if (list_key[i][0] == currentWord):
            list_words.append([list_key[i][1], list_value[i]])
    list_words.sort(key=lambda x:x[1],reverse=True)
    return list_words[:10]
    
def generateSentence(bigramModel, length):
    '''
    GENERATE SENTENCE
    IS : Menerima input model bigram dan panjang kalimat yang ingin di-generate
    FS : Mengembalikan kalimat dengan panjang sesuai inputan
    Note : Generate sentence
    '''
    list_words = list(bigramModel.keys())
    kalimat = ''
    kata = nextBestWord(bigramModel,"<s>")
    for i in range(length):
        kalimat = kalimat +" " + kata
        kata = nextBestWord(bigramModel,kata)
    return kalimat
    
if __name__ == '__main__':
    print("TUGAS LANGUAGE MODELING NLP - SFY")
    print("SILAKAN MASUKKAN IDENTITAS ANDA")
    Nama = input("NAMA : ")
    NIM = input("NIM : ")

    os.system("pause")
    os.system("cls")

    #import dataset
    data = pd.read_csv('text.csv')

    print("TUGAS 1. TAMPILKAN 5 BARIS PERTAMA DARI DATASET")
    print()
    print("HASIL : ")
    print(data.head())

    os.system("pause")
    os.system("cls")

    print("TUGAS 2. BUAT MODEL UNIGRAM")
    print()
    print("HASIL : ")
    print(buildUnigramModel(data['text']))

    os.system("pause")
    os.system("cls")

    print("TUGAS 3. BUAT MODEL BIGRAM")
    print()
    print("HASIL : ")
    bigramModel = buildBigramModel(data['text'])
    print(bigramModel)    

    os.system("pause")
    os.system("cls")

    print("TUGAS 4. MENAMPILKAN NEXT BEST WORD")
    print()
    print("HASIL : ")
    print("of -> ",nextBestWord(bigramModel,"of"))
    print("update -> ",nextBestWord(bigramModel,"update"))
    print("hopes -> ",nextBestWord(bigramModel,"hopes"))

    os.system("pause")
    os.system("cls")

    print("TUGAS 5. TOP 10 BEST NEXT WORD")
    print()
    print("HASIL : ")
    print("of -> ",nextTenBestWords(bigramModel,"of"))
    print("update -> ",nextTenBestWords(bigramModel,"update"))
    print("hopes -> ",nextTenBestWords(bigramModel,"hopes"))

    os.system("pause")
    os.system("cls")

    print("TUGAS 6. GENERATE KALIMAT")
    print()
    n = int(input("Panjang Kalimat : "))
    print("HASIL : ")
    print(generateSentence(bigramModel, n))

    os.system("pause")
    os.system("cls")
    print("SELAMAT", Nama ,"ANDA SUDAH MENYELESAIKAN TUGAS LANGUAGE MODELING NLP-SFY")