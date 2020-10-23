# Markov-NameGen
Fantasy Name Generator - Python CLI Script
==========================================

CLI Script for generating fantasy names from one or many text files.


Current Available commands:
---------------------------
 markov.py                   to display the help message
 markov.py <n> <modifiers>  to display <n> new words with <modifiers>
Available modifiers
 markov.py -f=<filename>    to use a different file than the default one
 markov.py -t=<charlen>     to change the length of the tokens
 markov.py -l=<n>           to change the maximum word length
 markov.py -u               to append changes to the config-file
 markov.py -d               to restore config file to its initial values

The code has been inspired by https://towardsdatascience.com/generating-startup-names-with-markov-chains-2a33030a4ac0, and inserted into a class for better portability.
The txt sample name files are from https://www.scrapmaker.com/.

