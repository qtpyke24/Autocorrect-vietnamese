from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from utils import correct_spelling, suggest_next_words
import json

app = FastAPI()

# Mount static files cho frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Welcome to Vietnamese Autocomplete & Autocorrect"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            input_data = json.loads(data)
            input_text = input_data.get("input", "")
            action = input_data.get("action", "")  # "correct" hoặc "suggest"

            if action == "correct":
                # Chỉ xử lý autocorrect
                corrected = correct_spelling(input_text)
                response = {"corrected": corrected, "suggestions": []}
            elif action == "suggest":
                # Chỉ xử lý autocomplete
                corrected = correct_spelling(input_text)  # Vẫn sửa lỗi để đảm bảo prefix đúng
                suggestions = suggest_next_words(corrected, top_n=3)
                suggestions_list = [{"word": word, "score": score} for word, score in suggestions]
                response = {"corrected": corrected, "suggestions": suggestions_list}
            else:
                response = {"error": "Invalid action"}

            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        print("Client disconnected")