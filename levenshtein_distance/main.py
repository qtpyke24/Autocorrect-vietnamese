from data_processor import build_dictionary
from spell_checker import correct_sentence

input_sentence = input("Nhập câu cần kiểm tra chính tả: ")
corrected = correct_sentence(input_sentence, 'vietnamese_dict.txt')
print("Câu đã được sửa:", corrected)