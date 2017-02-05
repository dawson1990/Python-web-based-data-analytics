# Web-based-Data-Analysis
The ea-thesaurus-lower.json word associations file (discussed in class) contains a
dictionary of word associations for 8,210 individual words (as a single JSON file). When a word in
the word associations dictionary is looked up, the associations are returned as a list of individual
dictionaries which themselves associate another word with a score.
You are to build a webapp which allows its users to upload any file of textual data for analysis.
There are two analyses to perform: basic and advanced.
## Basic Analysis
Upon receiving the text file, your webapp processes the file as follows:
* The text in the file is converted to lowercase.
* Each individual word (i.e., token) in the text is looked-up in the word associations file.
* For each unique word found, the top three scoring associations are to be remembered.
* If a word is not found in the word associations file, this fact is to be remembered, too.
* For every word found (or not found), a frequency count for the word is to be provided.

## Advanced Analysis
You are further asked to “score” each unique word appearing in the uploaded text file based on it
appearing in the word associations file. Specifically, your user wants to be able to process the body
of text and score (i.e., rank) each of the unique words as follows:
* A frequency count for each word is to be determined (freq).
* Each unique word in the text is to looked-up in the word associations file, and either the
first, second, or third word association and score is to be retrieved, with which one to use
controlled by a user-configurable setting (association_score).
* The freq and association_score values are to be multiplied together (rank)
Once the analyses are complete, your webapp needs to provide a mechanism which allows a user to
look up any previous results. It is not enough to provide the results of the most-recent analysis: you
must provide a lookup mechanism which allows the user of your webapp to lookup the results of
any previous analysis. Additionally, your system is to only preform an analysis on a text file when
required: if a text file has already been processed by your webapp, its remembered results are to be
looked-up and displayed (i.e., the analysis is not to be repeated needlessly).
# Python-web-based-data-analytics
