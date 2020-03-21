import os
import re
import jieba
from .list_utils import argmax_list


jieba.initialize()
HMM = True

def get_chinese(text):
    """process a text to remove all non chinese character"""
    filtrate = re.compile(u'[^\u4E00-\u9FA5]') # non-Chinese unicode range
    text = filtrate.sub(r'', text) # remove all non-Chinese characters
    return text


def rmv_not_chinese(counter):
    """remove non chinese entries in a word frequency counter"""
    for key in counter.copy().keys():
        if get_chinese(key) == '':
            del counter[key]
    return counter


def find_chapter_separator(txt):
    """find the formatting for chapter in a mandarin book
    the format is usually `第*节` or `第*章` or `第*回` with `*` which can
    be a chinese or digit number"""

    # define the different possible separator that can occur (can be extended in the future)
    list_sep = ['节', '章', '回']

    # find the list of chapter separation for all of the separators defined in `list_sep`
    list_count = []
    list_seps = []
    for sep in list_sep:
        seps = re.findall('第[一二三四五六七八九十百零0-9]{1,5}' + sep + '[\n\\s\t　]', txt)
        list_seps.append(seps)
        list_count.append(len(seps))

    # find the index of the longest list
    max_index = argmax_list(list_count)

    # check if there is a non zero lenght list
    if list_count[max_index] == 0:
        max_sep = None
        max_seps = None
    else:
        max_sep = list_sep[max_index]
        max_seps = list_seps[max_index]
    return max_sep, max_seps


def make_chapter_from_chinese_book(path_book_folder, book_name):
    path_book_chapters = os.path.join(path_book_folder, "chapters")

    if not os.path.isdir(path_book_chapters):
        os.mkdir(path_book_chapters)

    if not len(os.listdir(path_book_chapters)):
        path_book_raw = os.path.join(path_book_folder, "raw", "{}.txt".format(book_name))
        with open(path_book_raw, "r", encoding="utf-8") as infile:
            full_text = infile.read()
        chapter_separator, _ = find_chapter_separator(full_text)
        chapters = re.split('第[一二三四五六七八九十百零0-9]{1,5}' + chapter_separator + '[\n\\s\t]',
                               full_text)[1:]
        for n, chapter in enumerate(chapters):
            path_chapter = os.path.join(path_book_chapters, "{}.txt".format(n+1))
            with open(path_chapter, "w", encoding="utf-8") as outfile:
                outfile.write(chapter)


def chinese_tokenize(chinese_text):
    tokenized_text = jieba.cut(chinese_text, HMM=HMM)
    return tokenized_text