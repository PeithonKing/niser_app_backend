import os.path
from random import choice
from niser_app.settings import STATIC_URL

# ROOT = os.path.abspath(os.path.dirname(__file__))
# ASSETS = os.path.join(ROOT, 'assets')
#ADJECTIVES_FILENAMES = ['3la', '4la', 'ma34']
ADJECTIVES_FILENAMES = ['simple-adj']
#NOUNS_FILENAMES = ['3ln', '4ln', 'mm34']
NOUNS_FILENAMES = ['wiki-animals-34']
ADJECTIVES_FILES = map(lambda i: f"{STATIC_URL}arc/assets/{i}", ADJECTIVES_FILENAMES)
NOUNS_FILES = map(lambda i: f"{STATIC_URL}arc/assets/{i}", NOUNS_FILENAMES)

adjectives = []
nouns = []

for i in ADJECTIVES_FILES:
    with open(i) as f:
        adjectives += f.readline().split()
for i in NOUNS_FILES:
    with open(i) as f:
        nouns += f.readline().split()

def genURL():
    adjective_1 = choice(adjectives).title()
    adjective_2 = choice(adjectives).title()
    noun = choice(nouns).title()
    return f"{adjective_1}{adjective_2}{noun}"
