# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 20:01:36 2018

@author: Nicolai
"""

import csv

def subtitleCleaner(filename):
    
    """
    This function removes timestamps and font and music markings from youtube subtitles.
    INPUT: txt file of youtube subtitles
    OUTPUT: string consisting of text from subtitles
    """
    
    file = open(filename, 'r')
    text = file.read()
    
    # Remove font and music
    text = text.replace('<font color="#CCCCCC">','')
    text = text.replace('<font color="#E5E5E5">','')
    text = text.replace('</font>','')
    text = text.replace('[Music]','')
    
    # Remove timestamps
    while '>' in text:
        text_index = text.index('>')
        text = text[:text_index - 17] + text[text_index + 13:]
    
    # Split by lines
    lines = text.split('\n')
    lines = [line for line in lines if line != '']
    
    # Removes lines that consists only of numbers
    cleanlines = lines
    for i, line in enumerate(lines):
        if line.isdigit():
            del(cleanlines[i])
    
    cleantext = ' '.join(cleanlines)
    
    return cleantext

def deleteSpecChars(text, specialChars):
    """
    This function removes special characters from a string and returns a new string
    INPUT: 
    text: string
    specialChars: List of characters to be removed
    
    
    OUTPUT:
    newTextList: type <list>  Each element in list is a string
    """
    for char in specialChars:
        text = text.replace(char, '') 
    return text

def wordCount(cleantext):
    
    """
    This function counts words from a text and returns a dictionary. 
    Does not fix for punctuation and special characters, so for example 'why' and 'why?' will be counted as two different words. This doesn't matter in the case of youtube subtitles.
    
    INPUT: string
    OUTPUT: dictionary where keys are words, and the values are counts.
    """
    
    words = cleantext.split()
    
    #Counting words and saving count in dictionary
    count = {}
    for word in words:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1
    
    return count

def dict_2_csv(dictionary, csv_file):
    """
    This function writes a dictionary into a csv file, with keys in first column and corresponding values in the second column.
    
    INPUT: 
    dictionary: dictionary
    csv_file: .csv file which the dictionary will be written into
    OUTPUT .csv file
    """
    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in dictionary.items():
            writer.writerow(row)
    return            


def getMostFrequent(counts, exclWordList, topNumber):
    """
    This function takes a dictionary of word counts and returns the most 
    frequent ones. The user defines how many of the most frequent words are 
    returned.
    
    INPUT: 
    counts: Dictionary with word counts.
    A list of words to be excluded from consideration
    topNumber: Number of top freqent words to be extracted.
    OUTPUT:
    topFreqWords: Dictionary of top words where keys represent words and values represent number of time a word has been counted.
    """
    sort_words = sorted(counts, key=counts.__getitem__, reverse=True) # Sort words by count
    sort_count = sorted(counts.values(), reverse=True) # Sort counts
    
    
    sort_words = sort_words[:topNumber] # Removing everything except the top words
    sort_count = sort_count[:topNumber]
    
    topCount = {}
    
    for i in range(len(sort_words)):
        topCount[sort_words[i]] = sort_count[i] # Creating dictionary with the top words
    
    return topCount



if __name__ == '__main__':
    
    cleantext = subtitleCleaner('uglysubtitles.txt')
    
    count = wordCount(cleantext)
    
    dict_2_csv(count, 'csvcount.csv')