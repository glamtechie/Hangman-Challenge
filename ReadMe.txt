The given code is in Python and runs on Python 2.7

Download the folder from the link
To run type this in the terminal:
    cd Hangman-Challenge
    python play.py


Output: Printing the hangman characters and finally, the total error. Right now, the total number of runs is set to 100. To change it, just change the input to the function in play.py

Program logic:

1. I downloaded 2 files online- Probabilities of occurence of alphabets in English ie. letters.txt (source:Pavel Micka) and  1/3 million most frequent words with counts ie.count_1w.txt (source: Peter Norvig)

2. To predict the next alphabet I used a simple but powerful concept used extensively in AI- Bayes rule and probability rules.

Here is what I did:
High level: Split the sentence into words. Predicted the most probable letter for each word. Then chose the most probable letter out of all the letters we predicted.

For every letter in a word:
P(letter|previous predictions)= sum over all words in vocabulary(P(word,letter|guessed))
                              = sum over all words in the vocabulary(P(letter|words)*P(guessed|words)*P(words)/normalizing_constant)

The denominator will be a normalizing constant which we can ignore since we are comparing letters.
P(letter|words) will either be 0 or 1 considering a letter can either be in a word or not. P(guessed|words) also follows similar logic. P(words) is calculated by us from the data we have.

Finally, here is what we choose:
= max_probability_letter(max_probability_letter_for_each_word(probability of every letter occuring in the word given guesses))

Thus, for every word in the phrase, we are calculating the letter that has the highest occurence based on all the words in vocabulary of the same length. Once we get this letter and its probability, we add it to a list along with all our predictions for the other words.
We then select the best of these predictions.

