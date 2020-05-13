import os

import JapaneseTokenizer


def make_chapter_from_english_book(path_book_folder, book_name):
    path_book_chapters = os.path.join(path_book_folder, "chapters")

    if not os.path.isdir(path_book_chapters):
        os.mkdir(path_book_chapters)

    if not len(os.listdir(path_book_chapters)):
        path_book_raw = os.path.join(path_book_folder, "raw", "{}.txt".format(book_name))
        chapters = []
        with open(path_book_raw, "r", encoding="utf-8") as infile:
            chapter = ""
            for n, line in enumerate(infile):
                chapter += line
                if (n + 1) % 100 == 0:
                    chapters.append(chapter)
                    chapter = ""
        for n, chapter in enumerate(chapters):
            path_chapter = os.path.join(path_book_chapters, "{}.txt".format(n + 1))
            with open(path_chapter, "w", encoding="utf-8") as outfile:
                outfile.write(chapter)


def japanese_tokenize(japanese_text):
    mecab_wrapper = JapaneseTokenizer.MecabWrapper(dictType='ipadic')
    tokenized_text = mecab_wrapper.tokenize(japanese_text).convert_list_object()
    return tokenized_text
