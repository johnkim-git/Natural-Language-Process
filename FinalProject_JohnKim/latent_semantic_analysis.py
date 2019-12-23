#!/usr/bin/env python3
""" Final Project - latent_semantic_analysis.py"""
__author__="John Kim"

import re
import os
import sys
import math
import numpy as np

word_by_document_dictionary = {}
word_by_document_array = []
word_by_document_matrix = None
Ap = None


# Function to read incoming dictionary (model corpus) text file and copy into content as a string
def open_file (file_name):
   
   with open (file_name, 'r') as text_file:  
      content = text_file.readlines()
   text_file.close()
   
   return content


# Function to read in and recreate word document array from .dat file created in unigram_word_by_document.py
def recreate_word_by_document_array():

   global word_by_document_array
   
   text_file = open_file('word_by_document_array.dat')

   for line in text_file:
      word_in_document_list = re.sub(r'[^0-9\s]+', ' ', line).split()
      word_in_document_list = [int(value) for value in word_in_document_list] 
      word_by_document_array.append(word_in_document_list)
      

# Function to create unigram(s) dictionary read in from .dat file
def recreate_word_by_document_dictionary ():
   
   global word_by_document_dictionary
   
   text_file = open_file('word_by_document_dictionary.dat')
   
   for line in text_file:
      line = re.sub(r'[^a-zA-Z0-9\s]+', '', line)
      line = re.sub(r'[\t]+', ' ', line)
      line = re.sub(r'[\n]+', '', line)
      line_list = line.split(' ')
      key = line_list[0]
      line_list.pop(0)
      line_list = [int(value) for value in line_list] 
      word_by_document_dictionary[key] = line_list


# Function to perform Latent Semantic Analyis using the recreated word by document array 
def singular_value_decomposition():

   global word_by_document_array
   global word_by_document_dictionary
   global Ap
  
   
   word_document_matrix = np.matrix(word_by_document_array, dtype = int)
   
   # good explanation on https://technowiki.wordpress.com/2011/08/27/latent-semantic-analysis-lsa-tutorial/
   # u = matrix of coordinates of each word on concept (aka dimensions) space
   # s = matrix of singular values which gives clue as to how many concept (aka dimensions) we need to include
   # u = matrix coordinates of each documment on concept (aka dimensions) space
   
   u, s, vt = np.linalg.svd(word_document_matrix)
   
   up, sp, vp = u[: ,0:100], np.diag(s[0:100]), vt[: ,0:100]
   
   Ap = up*sp*vp.T

   row = 0

   for key in word_by_document_dictionary:
      word_by_document_dictionary[key] = Ap[row]
      row += 1
   

# Function to check if latent_semantic_analysis log required for cosine similarity is available
# If not available, will run unigram_word_by_dictionary.py to create a word by document array
# required by latent_semantic_analysis.py
# Then it will run latent_semantic_analysis.py to create a latent semantic analysis dictionary of
# word by documents. 
def check_word_by_document_available():



   if os.path.isfile('word_by_document_dictionary.dat') is False and os.path.isfile('word_by_document_array.dat') is False:
      print('Required file word_by_document_dictionary.dat is missing!')
      print('Required file word_by_document_array.dat is missing!')
      print('Now creating...')
      import unigram_word_by_document
      print('Required file word_by_document_dictionary.dat created!')
      print('Required file word_by_document_array.dat created!\n')
   if os.path.isfile('word_by_document_dictionary.dat') is False:
      print('Required file word_by_document_dictionary.dat is missing!')
      print('Now creating...')
      import unigram_word_by_document
      print('Required file word_by_document_dictionary.dat created!\n')
   if os.path.isfile('word_by_document_array.dat') is False:
      print('Required file word_by_document_array.dat is missing!')
      print('Now creating...')
      import unigram_word_by_document
      print('Required file word_by_document_array.dat created!\n')


# Function to write out unigram dictionary to an output file
def write_file():

   global word_by_document_dictionary

   # Creates a writeable .dat file to export unigram dictionary and word by document array
   latent_semantic_analysis_dictionary_to_text = open('latent_semantic_analysis_dictionary.dat', "w")

   # iterates through unigram dictionary and writes the unigram and count onto a file
   for key, value in word_by_document_dictionary.items():
      unigram_string = '{}:\t{}\n'.format(key, value)
      latent_semantic_analysis_dictionary_to_text.write(unigram_string)

   # Closes outgoing file
   latent_semantic_analysis_dictionary_to_text.close()

   
# Main function to call other functions
def main ():
   
   check_word_by_document_available()
   recreate_word_by_document_array()
   recreate_word_by_document_dictionary()
   singular_value_decomposition()
   write_file()
 
if __name__== "__main__":
    main()   
    
    
if __name__== "latent_semantic_analysis":
    main()