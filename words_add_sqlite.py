import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ReadItEasy.settings')

import django
django.setup()

from apiWords.models import MandarinWord
from utils.path_utils import PathHandler

# fetch the root project and other paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
paths = PathHandler(BASE_DIR)
path_ce_dict = paths.extended_dict()
path_neighbors_words = paths.mandarin_neighboors_words()

dict_similar_words = {}
with open(path_neighbors_words, 'r', encoding='utf-8') as infile:
    for line in infile:
        word, *neighbors = line.split('\t')
        dict_similar_words[word] = neighbors

# delete all object in the database for avoiding duplicates
MandarinWord.objects.all().delete()
#
#
# iterate through our dict
list_words = []
with open(path_ce_dict, 'r', encoding='utf-8') as f:
    headline = f.readline()
    print(headline)
    for n, line in enumerate(f):
        line_splitted = line.rstrip('\n').split('\t')
        traditional = line_splitted[0]
        simplified = line_splitted[1]
        pronunciation_num = line_splitted[2]
        pronunciation = line_splitted[3]
        hsk = line_splitted[4]
        definitions = line_splitted[5]
        similar_words = dict_similar_words.get(simplified, [])
        similar_words = '/'.join(similar_words)
        #
        # print(line_splitted)
        # print("traditional", traditional)
        # print("simplified", simplified)
        # print("pronunciation_num", pronunciation_num)
        # print("pronunciation", pronunciation)
        # print("hsk", hsk)
        # print("definitions", definitions)
        # print("similar_words", similar_words)
        # input("input")

        new_word = MandarinWord(simplified=simplified,
                                traditional=traditional,
                                pronunciation=pronunciation,
                                pronunciation_num=pronunciation_num,
                                hsk=hsk,
                                definitions=definitions,
                                similar_words=similar_words,
                                )
        list_words.append(new_word)
        if n % 1000==0:
            print(n)

MandarinWord.objects.bulk_create(list_words)
print("done")
