import os


class PathHandler:
    def __init__(self, BASE_DIR):
        self.BASE_DIR = BASE_DIR

    def corpus_statistics(self, language):
        return os.path.join(self.BASE_DIR, 'data', 'languages', language, 'statistics', 'corpus_rank_freqs.txt')
