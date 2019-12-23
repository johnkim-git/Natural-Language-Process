#!/usr/bin/env python3
""" Final Project - cosine_similarity.py"""
__author__="John Kim"

import re
import os
import sys
import math
#import numpy
import random
from os import path

word_to_analyze = ''
number_of_words = 0

latent_semantic_analysis_dictionary = {}
cosine_similarity_dictionary = {}
cosine_similarity_log = {}#open('cosine_similarity_log.dat',"w")

# Function to read incoming dictionary (model corpus) text file and copy into content as a string
def open_file(file_name):
   
   
   with open(file_name, 'r') as text_file:
      content = text_file.readlines()
   text_file.close()

   return content


# Function to create unigram(s) dictionary read in from .dat file
def recreate_latent_semantic_analysis_dictionary():

   global latent_semantic_analysis_dictionary

   print()
   print('Building data of words, please wait. Sorry about the wait.\n')

   text_file = open_file('latent_semantic_analysis_dictionary.dat')

   for line in text_file:
      line = re.sub(r'[^a-zA-Z0-9\s\-\.]+', '', line)
      line = re.sub(r'[\s\s]+', ' ', line)
      line = re.sub(r'[\t]+', '', line)
      line = re.sub(r'[\n]+', '', line)
      line_list = line.split(' ')
      line_list = ' '.join(line_list).split()
      if is_number(line_list[0]) == False:
         key = line_list[0]
         line_list.pop(0)
         latent_semantic_analysis_dictionary[key] = []
      line_list = [float(value) for value in line_list]
      for element in line_list:
         latent_semantic_analysis_dictionary[key].append(element)


# Will check if program is capable of analyzing input word (has to be available in dictionary)
# If not, will keep looping until a word typed in is available to analyze using cosine similarity
# to find similar words
def check_word_dict():

   global word_to_analyze
   global number_of_words

   confirmation = 'no'

   if (word_to_analyze == ''):
      while (word_to_analyze == ''):
         print('You have not entered a word.  Please enter a word!')
         word_to_analyze = input().lower()

   while (word_to_analyze not in latent_semantic_analysis_dictionary) or (word_to_analyze == ''):
      if (word_to_analyze == ''):
         while (word_to_analyze == ''):
            print('You have not entered a word.  Please enter a word!')
            word_to_analyze = input().lower()
      if (word_to_analyze not in latent_semantic_analysis_dictionary):
         while (word_to_analyze not in latent_semantic_analysis_dictionary):
            print('Due to limited data, the word: ' + word_to_analyze + ' was not found')
            print('Please reenter a new word or type "stop now" to terminate:')
            word_to_analyze = input().lower()
            if word_to_analyze == 'stop now':
               print('Ending program')
               sys.exit()
            print('Are you certain you want to search the synonyms for: ' + word_to_analyze + ' [yes or no]')
            confirmation = input().lower()
            while confirmation == 'no' or confirmation == 'n':
               print('Please reenter a new word or type "stop now" to terminate:')
               word_to_analyze = input().lower()
               if word_to_analyze == 'stop now':
                  print('Ending program')
                  sys.exit()
               print('Are you certain you want to search the synonyms for: ' + word_to_analyze + ' [yes or no]')
               confirmation = input().lower()


# Ask for number of words
def num_of_synonyms():

   global number_of_words

   confirmation = 'no'

   while confirmation == 'no' or confirmation == 'n':
      print('Enter the number of related words you would like to see (between 1-5)')
      number_of_words = int(input())
      print('Confirm: You would like to see', number_of_words, 'synonyms for ' + word_to_analyze + '? [yes or no]')
      confirmation = input().lower()


# Cosine similarity function to calculate which words are most similar to word input by user
def cosine_similarity():

   global word_to_analyze
   global cosine_similarity_dictionary
   global cosine_similarity_log

   print('Finding word(s) most similar to: ' + word_to_analyze + '.')
   print('Please wait....')

   high_cosine_similarity_value  = 0
   low_cosine_similarity_value = 0

   top_related_words = ['No more words are available'] * number_of_words

   cosine_similarity_value = 0

   for index in range (0, number_of_words - 1):
      low_cosine_similarity_value = 0
      cosine_similarity_log[word_to_analyze] = []
      for key in latent_semantic_analysis_dictionary:
         cosine_similarity_value = 0
         numerator = 0
         denominator = 0
         denominator_first_word = 0
         denominator_second_word = 0
         if key != word_to_analyze:
            for input_word, compare_word in zip(latent_semantic_analysis_dictionary[word_to_analyze], 
                                                latent_semantic_analysis_dictionary[key]):
               numerator += input_word * compare_word
               denominator_first_word  += pow(input_word, 2)
               denominator_second_word += pow(compare_word, 2)
            denominator = math.sqrt(denominator_first_word) * math.sqrt(denominator_second_word)
            if denominator == 0:
               cosine_similarity_value = 0
            else:
               cosine_similarity_value = numerator / denominator
            ##
            cosine_similarity_log[word_to_analyze].append([key, cosine_similarity_value])
         if key in top_related_words:
            continue
         if index == 0:
            if cosine_similarity_value > high_cosine_similarity_value:
               high_cosine_similarity_value = cosine_similarity_value
               top_related_words[index] = key
         else:
            if (cosine_similarity_value < high_cosine_similarity_value) and (cosine_similarity_value > low_cosine_similarity_value):
               low_cosine_similarity_value = cosine_similarity_value
               top_related_words[index] = key
      if index != 0:
         high_cosine_similarity_value = low_cosine_similarity_value

   return top_related_words


# Function to check if latent_semantic_analysis log required for cosine similarity is available
# If not available, will run unigram_word_by_dictionary.py to create a word by document array
# required by latent_semantic_analysis.py
# Then it will run latent_semantic_analysis.py to create a latent semantic analysis dictionary of
# word by documents. 
def check_lsa_file_available():
   
   if os.path.isfile('latent_semantic_analysis_dictionary.dat') is False:
      print('Required file latent_semantic_analysis_dictionary.dat is missing! Now creating...')
      import latent_semantic_analysis
      print('Required file latent_semantic_analysis_dictionary.dat created!\n')

# Print the n number of words most similar to word chosen by user - n = number from users choice
def print_words(top_words_list):

   print('The top', number_of_words, 'related words to ' + word_to_analyze + ' are: ')

   count = 1

   for word in top_words_list:
      print(count, ': ' + word)
      count += 1

# Necessary to check if first element of list is word or numbers to correctly recreate a
# dictionary from .dat file.
def is_number(s):
   try:
      float(s)
      return True
   except ValueError:
      pass
 
   try:
      import unicodedata
      unicodedata.numeric(s)
      return True
   except (TypeError, ValueError):
      pass
 
   return False


# Function to write out unigram dictionary to an output file
def write_file():

   global latent_semantic_analysis_dictionary
   cosine_similarity_log

   # Creates a writeable .dat file to export unigram dictionary and word by document array
   latent_semantic_analysis_dictionary_to_text = open('latent_semantic_analysis_dictionary_log.dat', "w")

   # iterates through unigram dictionary and writes the unigram and count onto a file
   for key, value in latent_semantic_analysis_dictionary.items():
      dictionary_string = '{}\t{}\n'.format(key, value)
      latent_semantic_analysis_dictionary_to_text.write(dictionary_string)
      
   # Creates a writeable .dat file to export unigram dictionary and word by document array
   cosine_similarity_log_to_text = open('cosine_similarity_log.dat', "w")

   # iterates through unigram dictionary and writes the unigram and count onto a file
   for key, value in cosine_similarity_log.items():
      dictionary_string = '{}\t{}\n'.format(key, value)
      cosine_similarity_log_to_text.write(dictionary_string)


   # Closes outgoing file
   latent_semantic_analysis_dictionary_to_text.close()
   cosine_similarity_log_to_text.close()

# Created to make testing easier without console
def run_from_console(*args):
   
   global word_to_analyze

   recreate_latent_semantic_analysis_dictionary()

   if len(sys.argv) == 2:
      if sys.argv[1] == 'TESTS.txt':
         auto(sys.argv[1])
      else:
         word_to_analyze = sys.argv[1]
         #recreate_latent_semantic_analysis_dictionary()
         check_word_dict()
   else:
      word_to_analyze = ''
      print('Please enter a word:')
      word_to_analyze = input()
      #recreate_latent_semantic_analysis_dictionary()
      check_word_dict()

def auto(tests_file):

   global word_to_analyze
   global number_of_words

   number_of_words = 5

   tests = open_file(tests_file)
   #print(tests)
   tests_list = tests[0].split(' ')

   #recreate_latent_semantic_analysis_dictionary()

   #auto_words = ['ruins', 'quick', 'self', 'poor', 'important', 'success', 'special', 'final', 'script', 'writing', 'free']

   #if word_to_analyze == '':
   for element in tests_list:
      number_of_words = random.randint(1,5)
      word_to_analyze = element
      top_words_list = cosine_similarity()
      print_words(top_words_list)
      print()
   write_file()
   sys.exit()




# Main function to call other functions
def main():

   check_lsa_file_available()
   #recreate_latent_semantic_analysis_dictionary()
   run_from_console(sys.argv)
   #check_lsa_file_available()
   #recreate_latent_semantic_analysis_dictionary()
   #check_word_dict()
   num_of_synonyms()
   top_words_list = cosine_similarity()
   print_words(top_words_list)
   write_file()


if __name__ == "__main__":
    main()