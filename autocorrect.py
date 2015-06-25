#!/usr/bin/env python

import sys, Queue

# Expect dictionary file as first arg, list of words to auto-correct as second argument
dictionary = [line.strip().lower() for line in open(sys.argv[1])]
candidates = [line.strip().lower() for line in open(sys.argv[2])]

vowels = "aeiou"

def suggest(word, max_tries=1000):

    blank_mask = [False for i in range(len(word))]

    pq = Queue.PriorityQueue()
    pq.put((0, (word, blank_mask)))

    tried = set()

    while pq.qsize() > 0 and len(tried) < max_tries:
        mods, pair = pq.get()
        word, mask = pair

        tried.add(word)

        if word in dictionary:
            return word

        # No need to generate more of the search space that we won't use
        if pq.qsize() > max_tries - len(tried):
            continue

        # Swap vowels
        for i, c in enumerate(word):
            if c in vowels and not mask[i]:
                mask_copy    = mask[:]
                mask_copy[i] = True

                for v in vowels:
                    if v == c:
                        continue

                    mod_word = word[:i] + v + word[i+1:]

                    if mod_word not in tried:
                        pq.put((mods + 1, (mod_word, mask_copy)))

        # Shorten runs of repeated characters:
        start = 0
        last  = word[0]

        for i, char in enumerate(word):
            if char == last and i != len(word) - 1:
                continue
         
            num_repeated = i - start if i < len(word) - 1 else (i - start) + 1
            if num_repeated > 1:
                for j in range(1, num_repeated):
                    mod_word = word[:start] + last * j + "" if i == len(word) - 1 else word[i:]
                    if mod_word not in tried:
                        pq.put((mods + 1, (mod_word, blank_mask)))
            
            start = i
            last  = char

    return "NO SUGGESTION"

for candidate in candidates:
    print(suggest(candidate))
