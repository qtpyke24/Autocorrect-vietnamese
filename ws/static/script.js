const ws = new WebSocket("ws://localhost:8000/ws");

const input = document.getElementById("inputText");
const correctedDiv = document.getElementById("corrected");
const suggestionsDiv = document.getElementById("suggestions");

let lastInput = "";
let lastAction = "";

input.addEventListener("input", () => {
    lastInput = input.value;
});

input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        lastAction = "correct";
        sendInput();
    } else if (event.key === "Tab") {
        event.preventDefault();
        lastAction = "suggest";
        sendInput();
    }
});

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.error) {
        console.error(data.error);
        return;
    }

    if (lastAction === "correct") {
        correctedDiv.innerHTML = `<strong>Văn bản đã sửa:</strong> ${data.corrected}`;
        input.value = data.corrected;  // Thay thế input
        suggestionsDiv.innerHTML = "";
    } else if (lastAction === "suggest") {
        let suggestionsHtml = "<strong>Gợi ý từ tiếp theo:</strong><ul>";
        data.suggestions.forEach(sug => {
            suggestionsHtml += `<li>${sug.word}</li>`;  // Không hiển thị score
        });
        suggestionsHtml += "</ul>";
        suggestionsDiv.innerHTML = suggestionsHtml;
        correctedDiv.innerHTML = `<strong>Văn bản đã sửa:</strong> ${data.corrected}`;
        // Tùy chọn: Nhấn Tab lần nữa để thêm từ đầu tiên
        if (data.suggestions.length > 0 && event.repeat) {
            input.value = data.corrected + " " + data.suggestions[0].word;
        }
    }
};

function sendInput() {
    if (lastInput.trim()) {
        ws.send(JSON.stringify({ input: lastInput, action: lastAction }));
    }
}

ws.onopen = () => console.log("WebSocket connected");
ws.onclose = () => console.log("WebSocket disconnected");
