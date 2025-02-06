"""
From
https://old.reddit.com/r/dailyprogrammer/comments/onfehl/20210719_challenge_399_easy_letter_value_sum/

Assign every lowercase letter a value, from 1 for a to 26 for z. Given a string
of lowercase letters, find the sum of the values of the letters in the string.

lettersum("") => 0
lettersum("a") => 1
lettersum("z") => 26
lettersum("cab") => 6
lettersum("excellent") => 100
lettersum("microspectrophotometries") => 317

Use enable1 word list
(https://raw.githubusercontent.com/dolph/dictionary/master/enable1.txt)
for the optional bonus challenges.
Optional bonus challenges:
1. microspectrophotometries is the only word with a letter sum of 317. 
   Find the only word with a letter sum of 319.
2. How many words have an odd letter sum?
3. There are 1921 words with a letter sum of 100, making it the second most common
   letter sum. What letter sum is most common, and how many words have it?
4. zyzzyva and biodegradabilities have the same letter sum as each other (151),
   and their lengths differ by 11 letters. Find the other pair of words with the
   same letter sum whose lengths differ by 11 letters.
5. cytotoxicity and unreservedness have the same letter sum as each other (188),
   and they have no letters in common. Find a pair of words that have no letters
   in common, and that have the same letter sum, which is larger than 188. (There
   are two such pairs, and one word appears in both pairs.)
6. The list of word { geographically, eavesdropper, woodworker, oxymorons } contains
   4 words. Each word in the list has both a different number of letters, and a
   different letter sum. The list is sorted both in descending order of word length,
   and ascending order of letter sum. What's the longest such list you can find?
"""

from collections import defaultdict
from typing import Dict, List, Tuple


class LetterSum:
    @staticmethod
    def calculate(string: str) -> int:
        """
        Calculate the sum of the alphabetical values of the letters in a given string.

        Each letter's value is determined by its position in the alphabet:
        'a' = 1, 'b' = 2, ..., 'z' = 26.

        Non-alphabetical characters are ignored.

        Parameters:
        string (str): The input string to calculate the letter sum for.

        Returns:
        int: The sum of the alphabetical values of the letters in the input string.
        """
        return sum(ord(i) - 96 for i in string.lower() if i.isalpha())


class WordAnalyzer:
    def __init__(self, filename: str):
        self.filename = filename
        self.odd_letter_count = 0
        self.most_common_words: Dict[int, List[str]] = defaultdict(list)
        self.word_pairs_length_diff = []
        self.word_pairs_no_common = []
        self.words_length_and_sum = defaultdict(str)
        self.MAXLEN = 0
        self.MAXSUM = 0

    def process_file(self):
        """Reads the file and proccesses each line to populate the word sums and perform checks."""
        with open(self.filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip("\n")
                self._process_line(line)

    def _process_line(self, line: str):
        """
        Processes each line to:
        1. Count words with off letter sums.
        2. Build a dictionary of word grouped by their letter sum.
        3. Print any word with a letter sum of 319.
        """
        ls = LetterSum.calculate(line)
        if ls == 319:
            print(line)

        if ls % 2 != 0:
            self.odd_letter_count += 1

        self.most_common_words[ls].append(line)
        self.words_length_and_sum[(len(line), ls)] = line
        self.MAXLEN = max(self.MAXLEN, len(line))
        self.MAXSUM = max(self.MAXSUM, ls)

    def analyze_word_pais(self, length_diff: int = 11):
        """Finds and stores word pairs for both length differences and disjoint
        letters."""
        self._find_length_diff_pairs(length_diff)
        self._find_no_common_pairs(min_sum=188)

    def _find_length_diff_pairs(self, length_diff: int):
        """
        Finds pairs of words with the same letter sum whose lengths differ by `target_diff`.
        Optimized by only checking relevant word sets (base_length + target_diff).
        Ensures all valid word combinations are considered.
        """
        for _, words in self.most_common_words.items():
            # group words by length
            length_dict = defaultdict(list)
            for word in words:
                length_dict[len(word)].append(word)

            # Only check base_length + target_diff, but ensure all permutations
            # within length groups
            for base_length, base_words in length_dict.items():
                target_length = base_length + length_diff
                if target_length in length_dict:
                    target_words = length_dict[target_length]
                    for w1 in base_words:
                        for w2 in target_words:
                            self.word_pairs_length_diff.append((w1, w2))

    def _find_no_common_pairs(self, min_sum: int):
        """
        Finds pairs of words with the same letter sum that have no letters in common.
        Optimized by only checking relevant word sets (min_sum and above).
        Ensures all valid word combinations are considered.
        """
        for key, values in self.most_common_words.items():
            if key > min_sum:
                num_values = len(values)
                if num_values >= 2:
                    for start in range(num_values - 1):
                        for end in range(start + 1, num_values):
                            if set(values[start]).isdisjoint(set(values[end])):
                                self.word_pairs_no_common.append(
                                    (values[start], values[end])
                                )

    def _find_most_common_word_sum(self) -> Tuple[int, int]:
        """Finds the most common word sum and the number of words with that sum."""
        return max(self.most_common_words.items(), key=lambda x: len(x[1]))

    def find_longest_unique(self) -> List[str]:
        """Find the longest list of words such that:
        1. Each word has a unique length.
        2. Each word has a unique letter sum.

        The list is sorted in:
        1. Descending order of word length.
        2. Ascending order of letter sum.
        """
        chainlist, templist = [], []

        # Iterate over possible word lengths (descending order)
        for length in range(self.MAXLEN, 0, -1):
            for chain in chainlist:
                next_sum = LetterSum.calculate(chain[-1]) + 1  # Ensure increasing sum
                for letter_sum in range(next_sum, self.MAXSUM):
                    if word := self.words_length_and_sum.get((length, letter_sum), ""):
                        if letter_sum == next_sum:
                            chain.append(word)  # Continue the chain
                        else:
                            templist.append(chain + [word])  # Create a new chain
                        break  # Finding a word is enough to build the chain, no need to go through all the words

            chainlist.extend(templist)
            templist.clear()

            # Start new chains if possible
            for letter_sum in range(1, self.MAXSUM):
                if word := self.words_length_and_sum.get((length, letter_sum), ""):
                    chainlist.append([word])
                    break  # Only one word per length is allowed

        return max(chainlist, key=len)

    def print_results(self):
        """Prints the results of the word analysis."""
        most_common_sum, words_in_most_common_sum = self._find_most_common_word_sum()

        print(f"{self.odd_letter_count} words have an odd letter sum")
        print(
            f"{most_common_sum} is the most common letter sum, and {len(words_in_most_common_sum)} words have it"
        )
        print(
            "Pair of words with the same letter sum whose lengths differ by 11 letters"
        )

        for pair in self.word_pairs_length_diff:
            print(pair)

        print("Pair of words with the same letter sum with no letters in common")
        for pair in self.word_pairs_no_common:
            print(pair)

        longest_list = self.find_longest_unique()
        print(f"Longest valid list found: {len(longest_list)} words")
        print("Word Length | Letter Sum | Word")
        print("-" * 30)
        for word in longest_list:
            print(f"{len(word):11} | {LetterSum.calculate(word):10} | {word}")
        print("-" * 30)
        print("Longest list of words with unique lengths and letter sums")


if __name__ == "__main__":
    print(LetterSum.calculate(""))
    print(LetterSum.calculate("a"))
    print(LetterSum.calculate("z"))
    print(LetterSum.calculate("cab"))
    print(LetterSum.calculate("excellent"))
    print(LetterSum.calculate("microspectrophotometries"))

    analyzer = WordAnalyzer("enable1.txt")
    analyzer.process_file()
    analyzer.analyze_word_pais(length_diff=11)
    analyzer.print_results()
