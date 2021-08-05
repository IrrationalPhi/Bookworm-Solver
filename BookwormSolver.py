#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 16:04:29 2021
"""

from collections import defaultdict

def defaultdict_from_list(li):
    """
    Parameters
    ----------
    li : list of strings
        Creates a defaultdict that contains every string in the list as key,
        with the respective number of occurences as the value.

    Returns
    -------
    res : defaultdict
        defaultdict of string occurrences.

    """
    res = defaultdict(int)
    for elem in li:
        res[elem] += 1
    return res

class TrieNode:
    """ 
    TrieNode class to be used in Trie data structure. Will be used as a node
    in a tree-like Trie data structure.
    
    Properties
    ----------
    char: character/string represented by node.
    isEnd: signifies existence of word that ends at node.
    children: all possible continutations of current word path,
            stored as a dictionary with (key, value) pair (char, TrieNode)
    """
    
    def __init__(self, ch = ""):
        self.char = ch
        self.isEnd = False
        self.children = {}

    def set_end(self):
        """
        Sets a node as the end of a word.

        Returns
        -------
        None.

        """
        self.isEnd = True

    def add_child(self, ch):
        """
        Adds a TrieNode child to current node if does not exist.

        Parameters
        ----------
        ch : char/string

        Returns
        -------
        None.

        """
        # if not yet registered, add a new trie
        if ch not in self.children:
            childTrieNode = TrieNode(ch)
            self.children[ch] = childTrieNode
            
class Trie:     
    """
    Trie class to store all possible words in text list. Used for quick
    searching of possible words. Implemented as a tree-like structure in 
    which each node is a TrieNode.
    
    Properties
    ----------
    root: TrieNode
        dummy TrieNode for traversing Trie.
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def add_word(self, word):
        """
        Adds a word to the current Trie.

        Parameters
        ----------
        word : string
            A word in the word list to be added to the trie.

        Returns
        -------
        None.
        
        """
        
        currNode = self.root
        
        # traverse through the characters in the word
        for currIdx in range(len(word)):
            # add the letter to children of current trie
            # and iterate currNode
            currNode.add_child(word[currIdx])
            currNode = currNode.children[word[currIdx]]
            
        # mark as the end of a word
        currNode.set_end()
        
    def add_words(self, words):
        """
        Adds a list of words to the trie.

        Parameters
        ----------
        words : list of strings
            List of strings to be added to trie.

        Returns
        -------
        None.

        """
        
        for word in words:
            self.add_word(word)
            
    def add_from_text(self, file):
        """
        Adds list of words to be read from a file.

        Parameters
        ----------
        file : txt file
            Text file to be read, where words are added into trie.

        Returns
        -------
        None.

        """
        
        with open(file, 'r') as wordList:
            for line in wordList:
                for word in line.split():
                    self.add_word(word)
            
    # something wrong here
    def search_possible_words(self, letters):
        """
        Searches all valid words in trie given a 
        list of letters, with duplicates

        Parameters
        ----------
        letters : list of chars
            List of characters (possibly with duplicates) that can be 
            used to form words. Maximum number of times a character can
            be used is the number of times it appears in the list.

        Returns
        -------
        None.
        
        """
        
        possibleWords = defaultdict(set)
        maxLen = len(letters)
        letters = defaultdict_from_list(letters)
        
        def dfs(currList, currNode):
            # when we leave, we add
            for letter in currNode.children:
                if letter in letters:
                    currList.append(letter)
                    letters[letter] -= 1
                    
                    # if already a word, we add
                    if currNode.children[letter].isEnd:
                        currString = "".join(currList)
                        possibleWords[len(currString)].add(currString)
                    
                    if letters[letter] == 0:
                        del letters[letter]

                    # recurse for dfs
                    dfs(currList, currNode.children[letter])
                    # backtrack
                    letters[letter] += 1
                    currList.pop()
                    
        dfs([], self.root)
        
        # display the words, partitioned by length
        print("Possible words below: ")
        print()
        for length in range(maxLen, 2, -1):
            if length in possibleWords:
                print("------------------------------------------")
                print(f"{length} LETTER WORDS: ")
                print(*possibleWords[length], sep=', ')
                
                print()

def main():
    trie = Trie()
    trie.add_from_text('wordList.txt')
    letters = input("Enter list of characters: ")
    print()
    letters = list(letters)
    
    findWords = True
    
    while findWords:
        trie.search_possible_words(letters)
        
        willContinue = input("Continue (y/n)? ")
        
        if willContinue != "y":
            findWords = False
        else:
            letters = input("Enter list of characters: ")
            print()
            letters = list(letters)
    

if __name__ == "__main__":
    main()