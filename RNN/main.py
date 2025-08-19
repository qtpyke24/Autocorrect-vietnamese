from data_processor import build_dictionary, training_data
from spell_checker import correct_sentence, train_rnn_model

with open('vietnamese_dict.txt', 'r', encoding='utf-8') as f:
    word_list = [line.strip() for line in f]
word_to_idx = {word: idx for idx, word in enumerate(word_list)}

# Nhập câu và sửa lỗi
input_sentence = input("Nhập câu tiếng Việt có lỗi chính tả: ")
corrected = correct_sentence(input_sentence, 'vietnamese_dict.txt', 'spell_checker_model.pth', word_to_idx)
print("Câu đã sửa: ", corrected)