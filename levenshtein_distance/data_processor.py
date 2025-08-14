import re
from collections import Counter

def build_dictionary(input_text_file, output_dict_file):
    # Đọc văn bản từ file đính kèm
    with open(input_text_file, 'r', encoding='utf-8') as f:
        text = f.read().lower()  # Chuẩn hóa chữ thường
    
    # Trích xuất từ: loại bỏ dấu câu, số, và giữ từ tiếng Việt (có dấu)
    words = re.findall(r'\b[\wàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]+\b', text)
    
    # Lấy từ unique và lưu vào file
    unique_words = set(words)
    with open(output_dict_file, 'w', encoding='utf-8') as f:
        for word in sorted(unique_words):
            f.write(word + '\n')
    
    print(f"Từ điển đã được xây dựng với {len(unique_words)} từ.")

# Chạy để build (thay 'data200k.vi.txt' bằng path file thực của bạn)
# build_dictionary('data200k.vi.txt', 'vietnamese_dict.txt')
build_dictionary('data200k.vi.txt', 'vietnamese_dict.txt')