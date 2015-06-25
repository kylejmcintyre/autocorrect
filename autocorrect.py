#!/usr/bin/env python

import sys, Queue

# Expect dictionary file as first arg, list of words to auto-correct as second argument
dictionary = [line.strip().lower() for line in open(sys.argv[1])]
candidates = [line.strip().lower() for line in open(sys.argv[2])]

max_tries = int(sys.argv[3]) if len(sys.argv) > 3 else 2500

alphabet = "abcdefghijklmnopqrstufwxyz"

def suggest(word, max_tries):

    pq = Queue.PriorityQueue()
    pq.put((0, word))

    tried = set()

    while pq.qsize() > 0 and len(tried) < max_tries:
        mods, word = pq.get()

        tried.add(word)

        if word in dictionary:
            return word

        # No need to generate more of the search space that we won't use
        if pq.qsize() > max_tries - len(tried):
            continue

        neighbors = []

        # Heuristic: Try swaps first since they're common
        for i, c in enumerate(word):
            if i + 1 < len(word):
                neighbors.append(word[:i] + word[i + 1] + word[i] + word[i+2:])

        for neighbor in neighbors:
            if neighbor not in tried:
                pq.put((mods + .5, neighbor))

        neighbors = []

        # Now do a principled single-edit neighbor enumeration
        for i, c in enumerate(word):
            for a in alphabet:
                # Won't you be my (character changed) neighbor
                neighbors.append(word[:i] + a + word[i+1:])
                # Won't you be my (character added) neighbor
                neighbors.append(word[:i] + a + word[i:])

            # Won't you be my (character deleted) neighbor
            neighbors.append(word[:i] + word[i+1:])

        # Neighbors for adding a character at the end
        for a in alphabet:
            neighbors.append(word + a)

        for neighbor in neighbors:
            if neighbor not in tried:
                pq.put((mods + 1, neighbor))

    return "UNKNOWN"

for candidate in candidates:
    print(suggest(candidate, max_tries))
