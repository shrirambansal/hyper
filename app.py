from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Logistic map function to generate chaotic sequences
def logistic_map(size, key):
    x = float(key)
    seq = []
    for _ in range(size):
        x = 4.0 * x * (1 - x)
        seq.append(int((x * 10**6) % 256))  # Normalize to byte range (0-255)
    return seq

# Encryption function
def encrypt_message(message, key):
    seq = logistic_map(len(message), float(key))
    return ''.join(chr(ord(char) ^ seq[i]) for i, char in enumerate(message))

# Decryption function (same as encryption for XOR)
def decrypt_message(encrypted_message, key):
    seq = logistic_map(len(encrypted_message), float(key))
    return ''.join(chr(ord(char) ^ seq[i]) for i, char in enumerate(encrypted_message))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    action = request.form['action']
    message = request.form['message']
    key = request.form['key']

    if not message or not key:
        return jsonify({'error': 'Message and Key cannot be empty!'})

    try:
        key_float = float(key)
        if not (0 < key_float < 1):
            raise ValueError
    except ValueError:
        return jsonify({'error': 'Key must be a float between 0 and 1!'})

    if action == 'encrypt':
        result = encrypt_message(message, key)
    elif action == 'decrypt':
        result = decrypt_message(message, key)
    else:
        result = 'Invalid action!'

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
