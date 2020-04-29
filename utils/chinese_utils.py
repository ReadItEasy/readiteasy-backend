import os
import re
from collections import Counter
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


def compute_freqs_dict(chinese_text):
    tokenized_text = chinese_tokenize(chinese_text)
    text_freqs = Counter(tokenized_text)
    text_freqs = rmv_not_chinese(text_freqs)
    n_tokens = sum(text_freqs.values())
    n_types = len(set(text_freqs.keys()))

    return n_tokens, n_types, text_freqs

def write_freqs_dict(path_src, path_dest):
    with open(path_src, 'r', encoding='utf-8') as infile:
        text = infile.read()

    n_tokens, n_types, text_freqs = compute_freqs_dict(text)
    with open(path_dest, "w", encoding="utf-8") as outfile:
        outfile.write("#tokens:\t{}\ttype:\t{}\n".format(n_tokens, n_types))
        for rank, (char, freq) in enumerate(text_freqs.most_common()):
            outfile.write("{}\t{}\t{}\n".format(char, rank+1, freq))


def word_statistics_in_file(word, path_statistics):
    with open(path_statistics, "r", encoding="utf-8") as infile:
        meta = infile.readline()
        _, n_tokens, _, n_types = meta.rstrip("\n").split("\t")
        n_tokens = int(n_tokens)
        n_types = int(n_types)
        target_rank = 0
        target_count = 0
        for line in infile:
            char, rank, count = line.rstrip("\n").split("\t")
            if char == word:
                target_rank = int(rank)
                target_count = int(count)
                break
    
    return target_rank, target_count, n_tokens, n_types

def read_freqs_dict(path):
    book_freqs = {}
    with open(path, 'r', encoding='utf-8') as infile:
        meta = infile.readline()
        _, n_book_tokens, _, n_book_types = meta.rstrip("\n").split("\t")
        n_book_tokens = int(n_book_tokens)
        n_book_types = int(n_book_types)
        count_cum_sum = 0
        book_char_95percentile = ""
        for line in infile:
            char, rank, count = line.rstrip("\n").split("\t")
            book_freqs[char] = int(count)
            count_cum_sum += int(count)
            if (not book_char_95percentile) and (count_cum_sum > int(0.95 * n_book_tokens)):
                book_char_95percentile = char

    return book_freqs, n_book_tokens, n_book_types, book_char_95percentile


def make_statistics_from_chinese_book(path_book_folder, book_name):
    path_folder_statistics = os.path.join(path_book_folder, "statistics")

    if not os.path.isdir(path_folder_statistics):
        os.mkdir(path_folder_statistics)

    path_raw = os.path.join(path_book_folder, 'raw', book_name + '.txt')
    path_book_statistics = path_raw.replace('/raw/', '/statistics/').replace('.txt', '_statistics.txt')
    if not os.path.isdir(path_book_statistics):
        write_freqs_dict(path_raw, path_book_statistics)



path_book = "/home/wran/projects/readiteasy/readiteasy-backend/data/languages/mandarin/books/1984_orwell/raw/1984_orwell.txt"

with open(path_book, 'r', encoding='utf-8') as infile:
    write_freqs_dict(path_book, path_book + 'xxx')

