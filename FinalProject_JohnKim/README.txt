README.txt

The purpose of this program is to find words that are similar to a given word.  There are 3 .py files and 3 .dat files.  To find similar words using the default (provided) latent semantic analysis values, only the cosine_similarity.py program file and the latent_semantic_analysis.dat file are necessary.  All 3 files are listed below with instructions and the libraries needed to run them.

———————————————————————

********************************************************************************************
NOTE: To see the 10 test cases, please type in the following command in the command console:
	
	python/python3 cosine_similarity.py TESTS.txt

For some systems, python will run python.  If this does not work, please use python3.
********************************************************************************************


cosine_similarity.py:
The main file which calculates the cosine similarity of the input word with words from documents to find the most similar word(s).

Special libraries needed:
None needed


WARNING: 
If the latent_semantic_analysis.dat file is not found, cosine_similarity.py program file will automatically run unigram_word_by_document.py and latent_semantic_analysis.py program files to create the required latent_semantic_analysis.dat file.


Directions:
To find similar words use existing LSA values included within the latent_semantic_analysis.dat file, just run the cosine_similarity.py program file.
There are 3 option when running from console:


1. python/python3* cosine_similarity.py TESTS.txt
This command will run the cosine_similarity.py program file with 10 preselected words and print out a random number(s) (between 1-5) of similar words.


2. python/python3* cosine_similarity.py inputword
This command will run the cosine_similarity.py program file with the given word.  Depending on if the documents used to create the latent semantic analysis values contained the word(s) typed in, the program may not be able to use certain input words.  If the word is rejected, the program will ask to either enter a new word or type in "stop now" to terminate.  If the word is accepted, it will ask how many similar words you wish to find and ask to confirm, then it will find the give number of similar words.


3. python/python3* cosine_similarity.py
Like the command above, typing this in command line to run file allowing you to choose the word.  The difference being it will prompt the user for a word after it has loaded the latent semantic analysis value.  Depending on if the documents used to create the latent semantic analysis values contained the word(s) typed in, the program may not be able to use certain input words.  If the word is rejected, the program will ask to either enter a new word or type in "stop now" to terminate.  If the word is accepted, it will ask how many similar words you wish to find and ask to confirm, then it will find the give number of similar words.


At the end of every run, the program file will create and write to a .dat file named latent_semantic_analysis_dictionary_log.dat.  This file will contain the sliced matrix created from the latent semantic analysis (latent_semantic_analysis.py) to allow the user to view the words and LSA values used to do cosine similarity calculations.

*Some systems such as the ones the Macs use may need the user to use python3 in the command line to run the file(s).

———————————————————————

unigram_word_by_document.py and latent_semantic_analysis.py:
Files to create new LSA values using different documents. 

Special libraries needed:
numpy
nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


WARNING:  
These files are used to recreate a word by document matrix.  The program file unigram_word_by_document.py requires that a folder be present in the current working director (where the .py files are located) containing all the documents/text files.  The .py file will prompt the user to type in the folder containing the documents, and if it is not present, will alert the user and terminate.



Directions:
The two files must be run in this order:
unigram_word_by_document.py
latent_semantic_analysis.py:



The unigram_word_by_document.py file:

In the command console, type: python/python3* unigram_word_by_document.py
The unigram_word_by_document.py program file will take the content of all text file(s) and clean the text.  It will then create a unigram dictionary containing all the words and export it to a file named word_by_document_dictionary.dat.  This dictionary will have all the words from every document, with each value being a list the length of the number of documents.  Each index of the list corresponds to the document number and will contain the frequency of the word in that row by column cell.
More importantly, it will also create a word frequency by documents matrix, named word_by_document_array.dat, that will be used by the latent_semantic_analysis.py program file to create an LSA matrix. The rows corresponds to the order of the words in the dictionary and the columns correspond to the document number.  Each row by column cell will have the frequency of the word of each  document in it. 
Running this file will prompt the user to type in the name of the folder to locate the folder containing the text file(s).  It is important that this folder is present in the current working directory (where the .py files are located), or the program will terminate.  If left blank, the default folder name will be "Documents".
If a folder is not found, the program will ask that a folder be created with the text file(s) placed in it and then terminate.




The latent_semantic_analysis.py file:

In the command console, type: python/python3* latent_semantic_analysis.py
The latent_semantic_analysis.py program file will load the file named word_by_document_array.dat and use the array to perform a Latent Semantic Analysis.  The latent_semantic_analysis.dat file created will be used by the program file cosine_similarity.py to perform cosine similarity operations to find similar words for a word input by the user.


WARNING:
In the function:
	def singular_value_decomposition():

The number of columns to slice in the equation:
	up, sp, vp = u[: ,0:100], np.diag(s[0:100]), vt[: ,0:100]

needs to be changed accordingly depending on the number of documents.  In this example, there were 250 documents used.  The number of columns to slice cannot exceed the number of documents (i.e. 250 columns to slice given 3 documents), nor is it helpful to set the number of columns to slice to 0.



