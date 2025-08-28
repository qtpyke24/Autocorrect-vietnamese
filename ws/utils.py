from pyvi import ViTokenizer
from nltk.metrics.distance import edit_distance
from models import dictionary, trie
import random

def correct_spelling(text):
    tokenized = ViTokenizer.tokenize(text).split()
    corrected = []
    for word in tokenized:
        if word in dictionary:
            corrected.append(word)
        else:
            distances = [(w, edit_distance(word, w)) for w in dictionary]
            distances.sort(key=lambda x: x[1])
            if distances and distances[0][1] < 3:  # Ngưỡng khoảng cách
                corrected.append(distances[0][0])
            else:
                corrected.append(word)
    return " ".join(corrected)

def suggest_next_words(prefix, top_n=3):
    if not prefix.strip():
        return []
    tokenized_prefix = ViTokenizer.tokenize(prefix).split()
    if not tokenized_prefix:
        return []
    last_word = tokenized_prefix[-1]  # Lấy từ cuối cùng làm prefix
    suggestions = trie.search_prefix(last_word, top_n)
    # Trả về danh sách gợi ý (ngẫu nhiên hoặc sắp xếp theo độ dài)
    random.shuffle(suggestions)  # Thay thế cho score của kenlm
    return [(word, 0.0) for word in suggestions[:top_n]]  # Giữ format