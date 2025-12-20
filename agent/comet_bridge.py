from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)
API_KEY = "heDuf3s4Y_EXwISRm2q2O1UPgi0zWbskf4_suT3cdus"

def require_auth(f):
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if auth.startswith('Bearer ') and auth[7:] == API_KEY:
            return f(*args, **kwargs)
        return jsonify({'error': 'Nao autorizado'}), 401
    decorated.__name__ = f.__name__
    return decorated

@app.route('/')
def root():
    return jsonify({'status': 'online', 'service': 'COMET Bridge'})

@app.route('/exec', methods=['POST'])
@require_auth
def execute():
    data = request.get_json()
    cmd = data.get('command', '')
    try:
        r = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True, timeout=120)
        return jsonify({'success': True, 'output': r.stdout, 'error': r.stderr})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print('COMET Bridge rodando na porta 5000')
    app.run(host='0.0.0.0', port=5000)
