from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)
PORT = 5003
OLLAMA_URL = "http://localhost:11434/api/generate"

@app.route('/')
def health():
    return jsonify({"status": "online", "service": "COMET Vision Server", "port": PORT})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    image_b64 = data.get('image')  # base64 da imagem
    prompt = data.get('prompt', 'Descreva esta imagem em detalhes')
    
    response = requests.post(OLLAMA_URL, json={
        "model": "llava",
        "prompt": prompt,
        "images": [image_b64],
        "stream": False
    })
    
    return jsonify({"success": True, "analysis": response.json().get('response', '')})

if __name__ == '__main__':
    print(f"COMET Vision Server rodando na porta {PORT}")
    app.run(host='0.0.0.0', port=PORT)

