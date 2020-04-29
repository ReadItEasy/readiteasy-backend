import os


class PathHandler:
    def __init__(self, BASE_DIR):
        self.BASE_DIR = BASE_DIR

    def corpus_statistics(self, language):
        return os.path.join(self.BASE_DIR, 'data', 'languages', language, 'statistics', 'corpus_rank_freqs.txt')

    def extended_dict(self):
        return os.path.join(self.BASE_DIR, 'data', 'languages', 'mandarin', 'dict', 'extended_dict.u8')

    def mandarin_neighboors_words(self):
        return os.path.join(self.BASE_DIR, 'data', 'languages', 'mandarin', 'embeddings', 'chinese_embeddings_552books_neighbors.tsv')

    def languages(self):
        return os.path.join(self.BASE_DIR, 'data', 'languages')

    # def language(self, language):
    #     return os.path.join(self.BASE_DIR, 'data', 'languages', language)

    def books(self, language):
        return os.path.join(self.BASE_DIR, 'data', 'languages', language, 'books')

    def book(self, language, book):
        return os.path.join(self.BASE_DIR, 'data', 'languages', language, 'books', book)

    def book_statistics(self, language, book):
        return os.path.join(self.BASE_DIR, 'data', 'languages', language, 'books', 
                              book, 'statistics', book + '_statistics.txt')

