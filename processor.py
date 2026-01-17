import re
import os

# --- Configuration ---
WORDLIST_FILE = 'santali_words.txt'
NUMBERS_FILE = 'santali_numbers.txt'
INPUT_FILE = 'articles_input.txt' 

OL_LETTERS_RE = r'[\u1C5A-\u1C7F]+'
OL_NUMBERS_RE = r'[\u1C50-\u1C59]+'

def process_text():
    if not os.path.exists(INPUT_FILE):
        return

    words_set = set()
    if os.path.exists(WORDLIST_FILE):
        with open(WORDLIST_FILE, 'r', encoding='utf-8') as f:
            words_set = set(line.strip() for line in f if line.strip())

    nums_set = set()
    if os.path.exists(NUMBERS_FILE):
        with open(NUMBERS_FILE, 'r', encoding='utf-8') as f:
            nums_set = set(line.strip() for line in f if line.strip())

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    new_words = re.findall(OL_LETTERS_RE, content)
    new_numbers = re.findall(OL_NUMBERS_RE, content)

    for w in new_words: words_set.add(w)
    for n in new_numbers: nums_set.add(n)

    # Save sorted "Pure Words"
    with open(WORDLIST_FILE, 'w', encoding='utf-8') as f:
        for word in sorted(list(words_set)):
            f.write(word + '\n')

    # Save sorted Numbers
    with open(NUMBERS_FILE, 'w', encoding='utf-8') as f:
        for num in sorted(list(nums_set)):
            f.write(num + '\n')

if __name__ == "__main__":
    process_text()