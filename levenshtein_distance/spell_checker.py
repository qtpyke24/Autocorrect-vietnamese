def levenshtein_distance(s1, s2):
    # Tính khoảng cách chỉnh sửa giữa 2 từ
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def correct_sentence(sentence, dictionary):
    # Load từ điển
    with open(dictionary, 'r', encoding='utf-8') as f:
        word_list = [line.strip() for line in f]
    
    # Tách câu thành từ
    words = sentence.lower().split()
    corrected_words = []
    
    for word in words:
        if word in word_list:
            corrected_words.append(word)  # Đúng rồi, giữ nguyên
        else:
            # Tìm từ gần nhất trong từ điển (khoảng cách <= 2)
            min_distance = float('inf')
            closest_word = word
            for dict_word in word_list:
                dist = levenshtein_distance(word, dict_word)
                if dist < min_distance:
                    min_distance = dist
                    closest_word = dict_word
            if min_distance <= 2:  # Ngưỡng sửa lỗi (có thể điều chỉnh)
                corrected_words.append(closest_word)
            else:
                corrected_words.append(word)  # Không sửa nếu quá xa
    
    return ' '.join(corrected_words).capitalize() + '.'