#!/usr/bin/env python3
""" Final Project - unigram_word_by_document.py"""
__author__="John Kim"

import re
import os
import sys
import math
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


document_folder = ''

word_by_document_dictionary = {}
word_by_document_dictionaries = {}
word_by_document_array = []


#### Creates a list of text files contained in directory/folder
def get_files_list ():
   
   files_list = []
   
   # change directory from current working directory (where .py file is) to
   # subdirectory "Documents" contains all text files (corpus)
   os.chdir(document_folder)
   os.getcwd()
   
   # creates a list of file names contained in subdirectory "Documents"
   for file in os.listdir():
      if file.endswith(".txt"):
         files_list.append(file)
         
   # Changes directory one level up to where this .py file is contained
   os.chdir('..')
   os.getcwd()
   
   # returns a list with the files names in separate indices      
   return files_list
   

#### Opens every text file in subfolder one by one to create a unigram dictionary
def read_files (file_name):
   
   # change directory from current working directory (where .py file is) to
   # subdirectory "Documents" contains all text files (corpus)
   os.chdir(document_folder)
   os.getcwd()
   
   with open(file_name, 'r') as text_file:
      text = text_file.read()
   text_file.close()
      
   # call function to remove all non-alphabet characters and change to lower case
   # return as a list of single words
   word_list = clean_text(text)
      
   # Changes directory one level up to where this .py file is contained
   os.chdir('..')
   os.getcwd()
   
   return word_list
      
#### Function that cleans up and splits text into list of single words     
def clean_text (text):

   # removes: punctuations, numbers, urls, any non-alphabet characters
   # changes all characters to lower case 
   text = re.sub(r'\S*@\S*\s?', '', text)
   text = re.sub(r'[^a-zA-Z\s]+', ' ', text).lower()
   
   # using NLTK corpus, all stop words (i.e. the, a, is) removed
   stop_words = set(stopwords.words('english')) 
   word_tokens = word_tokenize(text)
   real_words = set(nltk.corpus.words.words())
  
   word_list = [word for word in word_tokens if not word in stop_words] 
   word_list = []
  
   for word in word_tokens:
      if word not in stop_words:
         word_list.append(word)

   word_list = [word for word in word_tokens if word in real_words]
   word_list = []

   for word in word_tokens:
      if word in real_words:
         word_list.append(word)


   
   return word_list 

#### Function to get the frequency of words for each document: a dictionary will be created for
#### each document and added into a nested dictionary (dictionary of dictionaries)  
def create_word_by_document_dictionaries ():

   global word_by_document_dictionaries
   # Call function to create a list of text files (corpus) contained in "Documents" directory
   files_list = get_files_list()
   
   # to keep track of number of documents
   number_of_files = len(files_list)
   
   # To keep track of document number throughout each loop
   # Will be used as key to identify each dictionary in nested dictionary
   file_number = 0
   
   # read through each document and create a dictionary of words and its frequency
   # dictionary added into nested dictionary
   for file_name in files_list:
      temp_dict = {}
      word_list = read_files(file_name)
      for word in word_list:
         if word in temp_dict:
            temp_dict[word] += 1
         else:
            temp_dict[word] = 1
      word_by_document_dictionaries[file_number] = temp_dict
      # will increment by one at the end of each loop to keep track of next document number
      file_number += 1


# Create one single dictionary
# Each key word will have as a value: list with the number of documents as the length - initialized to 0's      
def create_word_by_document_dictionary():

   global word_by_document_dictionary
   
   files_list = get_files_list()
   number_of_files = len(files_list)
   
   document_number = 0
   
   for document in word_by_document_dictionaries:
      temp = word_by_document_dictionaries[document_number]
      for word in temp:
         if word in word_by_document_dictionary:
            word_by_document_dictionary[word][document_number] += temp[word]
         else:
            word_by_document_dictionary[word] = [0] * number_of_files
            word_by_document_dictionary[word][document_number] += temp[word]        
      document_number += 1

         
# Creates a Word by Document array using dictionary of word:[document no.]   
def create_word_by_document_array():
   
   global word_by_document_dictionary
   global word_by_document_array
   
   for key in word_by_document_dictionary:
      word_by_document_array.append(word_by_document_dictionary[key])


def folder_with_documents():

   global document_folder

   print('Please type in name of the folder with all the documents to be used as the corpus')
   print('Leaving blank will use "Documents" by default')
   print('WARNING: The name is case sensitive')
   document_folder = input()
   if document_folder == '':
      document_folder = 'Documents'

def check_if_folder_exists():

   if os.path.isdir(document_folder) is False:
      print ('Folder "' + document_folder + '" missing! Please create folder with documents to use for corpus, then retry.')
      print('Closing program now')
      sys.exit()
   
    
# Function to write out unigram dictionary to an output file
def write_file ():
   
   # Creates a writeable .dat file to export unigram dictionary and word by document array
   word_by_document_dictionary_to_text = open('word_by_document_dictionary.dat',"w")
   word_by_document_array_to_text = open('word_by_document_array.dat', "w")
   
   # iterates through unigram dictionary and writes the unigram and count onto a file
   for key, value in word_by_document_dictionary.items():
      unigram_string = '{}\t{}\n'.format(key, value)
      word_by_document_dictionary_to_text.write(unigram_string)
   
   # Writes word document matrix to a text file   
   word_by_document_array_to_text.writelines([str(x) + "\n" for x in word_by_document_array])
   
   # Closes outgoing file
   word_by_document_dictionary_to_text.close()
   word_by_document_array_to_text.close()
      
    
# Main function to call other functions
def main ():

   folder_with_documents()
   check_if_folder_exists()
   create_word_by_document_dictionaries ()
   create_word_by_document_dictionary()
   create_word_by_document_array()
   write_file()
 
if __name__== "__main__":
    main()

if __name__== "unigram_word_by_document":
    main()