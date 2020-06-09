import argparse
import os
import glob
import re
import time
from timeit import default_timer as timer
import jieba
from collections import Counter

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create the Biaffine Parser model.'
    )

    parser.add_argument('--fsrc', '-s', help='path to root folder containing books', required=True)
    parser.add_argument('--fdest', '-d', help='path to folder to save the data', required=True)
    parser.add_argument('--n_limit', default='0', type=int, 
                                  help='number of book to process (default=all)')

    args = parser.parse_args()

    list_paths_book = glob.glob(args.fsrc + '/**/*.txt', recursive=True)
    if not args.n_limit:
        args.n_limit = len(list_paths_book)

    jieba.enable_parallel(64)
    start = timer()
    list_times = []
    books_freqs = Counter({})
    for n,path in enumerate(list_paths_book[:args.n_limit]):
        t1 = time.time()
        with open(path, 'r', encoding='utf-8') as f:
            txt = f.read().split("------章节内容开始-------")[-1]
            tokens_jieba = jieba.cut(txt, cut_all=False, HMM=True)
            books_freqs += Counter(tokens_jieba)
            
            if n%10==0:
                print('progress :{:.2f}% \t {}/{} \t time elapsed = {:.2f}s'.format(100*n/len(list_paths_book) ,n,len(list_paths_book), timer()-start), end='\r')

        list_times.append(time.time()-t1)
    
    n_books = n+1
    print("\nSentences tokenized !")
    print("{} seconds in total and {} seconds per book".format(sum(list_times),sum(list_times)/n_books))

    books_freqs = rmv_not_chinese(books_freqs)
    n_tokens = sum(books_freqs.values())
    n_types = len(set(books_freqs.keys()))

    print(books_freqs.most_common(10))
    print(n_tokens, n_types)

    with open(args.fdest, "w", encoding="utf-8") as outfile:
        outfile.write("#tokens:\t{}\ttype:\t{}\n".format(n_tokens, n_types))
        for rank, (char, freq) in enumerate(books_freqs.most_common()):
            outfile.write("{}\t{}\t{}\n".format(char, rank+1, freq))

