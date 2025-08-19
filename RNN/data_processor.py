import re
from collections import Counter
import torch

def build_dictionary(input_text_file, output_dict_file):
    with open(input_text_file, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    
    # Trích xuất từ tiếng Việt (giữ dấu)
    words = re.findall(r'\b[\wàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]+\b', text)
    unique_words = sorted(set(words))
    
    # Lưu từ điển
    with open(output_dict_file, 'w', encoding='utf-8') as f:
        for word in unique_words:
            f.write(word + '\n')
    
    print(f"Từ điển đã được xây dựng với {len(unique_words)} từ.")
    return unique_words

def training_data(input_text_file, output_dict_file):
    with open(input_text_file, 'r', encoding='utf-8') as f:
        text = f.read().lower()  # Chuẩn hóa chữ thường

    sentences = re.split(r'(?<=[.!?]) +', text)  # Tách câu dựa trên dấu chấm, hỏi, cảm thán
    sentences = [s.strip() for s in sentences if s.strip()]  # Loại bỏ câu rỗng
    word_seq = [re.findall(r'\b[\wàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]+\b', s) for s in sentences]

    training_data = []
    for seq in word_seq:
        for i in range(1,len(seq)):
            context = seq[max(0, i-2):i]  # Lấy từ trước từ hiện tại
            target = seq[i]  # Từ hiện tại
            training_data.append((context, target))

    training_data = training_data[:100000] 
    
    with open(output_dict_file, 'w', encoding='utf-8') as f:
        for context, target in training_data:
            f.write(f"{' '.join(context)} | {target}\n")
     
    print(f"Dữ liệu huấn luyện đã được tạo với {len(training_data)} mẫu.")      
    return training_data

# Chạy để build (thay 'data200k.vi.txt' bằng path file thực của bạn)
# build_dictionary('data200k.vi.txt', 'vietnamese_dict.txt')
# training_data('data200k.vi.txt', 'training_data.txt')