import re
import os
from git import Repo

# --- Configuration ---
REPO_PATH = './'  
WORDLIST_FILE = 'santali_words.txt'
NUMBERS_FILE = 'santali_numbers.txt'
INPUT_FILE = 'articles_input.txt' 

# REGEX EXPLAINED:
# Letters only: \u1C5A to \u1C7F (Ol Chiki alphabets)
# Numbers only: \u1C50 to \u1C59 (Ol Chiki digits)
OL_LETTERS_RE = r'[\u1C5A-\u1C7F]+'
OL_NUMBERS_RE = r'[\u1C50-\u1C59]+'

def process_text():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Place your text in {INPUT_FILE} first.")
        return

    # 1. Load existing data to ensure uniqueness
    words_set = set()
    if os.path.exists(WORDLIST_FILE):
        with open(WORDLIST_FILE, 'r', encoding='utf-8') as f:
            words_set = set(line.strip() for line in f if line.strip())

    nums_set = set()
    if os.path.exists(NUMBERS_FILE):
        with open(NUMBERS_FILE, 'r', encoding='utf-8') as f:
            nums_set = set(line.strip() for line in f if line.strip())

    # 2. Read new articles
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 3. Extract Pure Words and Numbers separately
    new_words = re.findall(OL_LETTERS_RE, content)
    new_numbers = re.findall(OL_NUMBERS_RE, content)

    # 4. Update sets (Deduplication)
    added_w = 0
    for w in new_words:
        if w not in words_set:
            words_set.add(w)
            added_w += 1

    added_n = 0
    for n in new_numbers:
        if n not in nums_set:
            nums_set.add(n)
            added_n += 1

    # 5. Save sorted "Pure Words" list
    with open(WORDLIST_FILE, 'w', encoding='utf-8') as f:
        for word in sorted(list(words_set)):
            f.write(word + '\n')

    # 6. Save sorted Numbers list
    with open(NUMBERS_FILE, 'w', encoding='utf-8') as f:
        for num in sorted(list(nums_set)):
            f.write(num + '\n')

    print(f"Process Complete: {added_w} new words, {added_n} new numbers.")
    
    # 7. Push to GitHub if there is new data
    if added_w > 0 or added_n > 0:
        sync_github()

def sync_github():
    try:
        repo = Repo(REPO_PATH)
        repo.git.add(WORDLIST_FILE, NUMBERS_FILE)
        repo.index.commit("Automated Update: Added pure Ol Chiki words and numbers")
        origin = repo.remote(name='origin')
        origin.push()
        print("Successfully synced to GitHub.")
    except Exception as e:
        print(f"GitHub Sync failed: {e}")

if __name__ == "__main__":
    process_text()