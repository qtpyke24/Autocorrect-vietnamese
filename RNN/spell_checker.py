from time import time
import torch
import torch.nn as nn
import torch.optim as optim
from collections import defaultdict
import random

class SpellCheckerRNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim=50, hidden_dim=100):
        super(SpellCheckerRNN, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.rnn = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)
    
    def forward(self, x):
        x = self.embedding(x)
        _, (hidden, _) = self.rnn(x)
        out = self.fc(hidden[-1])
        return out

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

def train_rnn_model(training_data_file, dictionary_file, model_path, epochs=1):
    start_time = time.time()
    print("Bắt đầu huấn luyện mô hình...")

    # Load từ điển
    print("Đang đọc từ điển...")
    with open(dictionary_file, 'r', encoding='utf-8') as f:
        word_list = [line.strip() for line in f]
    word_to_idx = {word: idx for idx, word in enumerate(word_list)}
    vocab_size = len(word_list)
    print(f"Từ điển có {vocab_size} từ.")

    # Load dữ liệu huấn luyện
    print("Đang đọc dữ liệu huấn luyện...")
    training_data = []
    with open(training_data_file, 'r', encoding='utf-8') as f:
        for line in f:
            context, target = line.strip().split(' | ')
            context = context.split()
            if all(c in word_to_idx for c in context) and target in word_to_idx:
                training_data.append((context, target))
    print(f"Tìm thấy {len(training_data)} cặp context-target.")

    # Khởi tạo mô hình
    print("Khởi tạo mô hình RNN...")
    model = SpellCheckerRNN(vocab_size)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Sử dụng thiết bị: {device}")
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Huấn luyện
    print("Bắt đầu vòng lặp huấn luyện...")
    for epoch in range(epochs):
        total_loss = 0
        random.shuffle(training_data)
        for i, (context, target) in enumerate(training_data):
            context_indices = torch.tensor([word_to_idx[c] for c in context], dtype=torch.long).unsqueeze(0).to(device)
            target_idx = torch.tensor([word_to_idx[target]], dtype=torch.long).to(device)

            optimizer.zero_grad()
            output = model(context_indices)
            loss = criterion(output, target_idx)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

            # In tiến trình mỗi 1000 mẫu
            if (i + 1) % 1000 == 0:
                print(f"Epoch {epoch+1}, Mẫu {i+1}/{len(training_data)}, Loss: {loss.item():.4f}")

        print(f"Epoch {epoch+1}, Loss trung bình: {total_loss / len(training_data):.4f}")

    # Lưu mô hình
    torch.save(model.state_dict(), model_path)
    print(f"Mô hình đã được lưu tại {model_path}")
    print(f"Thời gian huấn luyện: {time.time() - start_time:.2f} giây")
    return model, word_to_idx

def correct_sentence(sentence, dictionary_file, model_path, word_to_idx):
    # Load từ điển
    with open(dictionary_file, 'r', encoding='utf-8') as f:
        word_list = [line.strip() for line in f]
    
    # Load mô hình
    vocab_size = len(word_list)
    model = SpellCheckerRNN(vocab_size)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    
    # Tách câu
    words = sentence.lower().split()
    corrected_words = []
    
    for i, word in enumerate(words):
        if word in word_list:
            corrected_words.append(word)
        else:
            # Sử dụng Levenshtein distance
            min_distance = float('inf')
            closest_word = word
            for dict_word in word_list:
                dist = levenshtein_distance(word, dict_word)
                if dist < min_distance:
                    min_distance = dist
                    closest_word = dict_word
            
            # Sử dụng RNN để dự đoán từ dựa trên ngữ cảnh
            if i >= 2:  # Cần ít nhất 2 từ trước làm ngữ cảnh
                context = words[i-2:i]
                if all(c in word_to_idx for c in context):
                    context_indices = torch.tensor([word_to_idx[c] for c in context], dtype=torch.long).unsqueeze(0)
                    with torch.no_grad():
                        output = model(context_indices)
                        predicted_idx = torch.argmax(output, dim=1).item()
                        predicted_word = word_list[predicted_idx]
                        # So sánh với Levenshtein
                        if min_distance <= 2 and levenshtein_distance(word, predicted_word) <= 2:
                            corrected_words.append(predicted_word)
                        else:
                            corrected_words.append(closest_word)
                    continue
            if min_distance <= 2:
                corrected_words.append(closest_word)
            else:
                corrected_words.append(word)
    
    return ' '.join(corrected_words).capitalize() + '.'
# model, word_to_idx = train_rnn_model('training_data.txt','vietnamese_dict.txt','spell_checker_model.pth',epochs=n)