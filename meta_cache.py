from flask import Flask, request, jsonify
import aiofiles
import os

app = Flask(__name__)

# In-memory store of file hashes
file_hashes = set()

# File to store file hashes
FILE_NAME = 'file_hashes.txt'


def load_hashes():
    """Load hashes from file into a set."""
    if not os.path.exists(FILE_NAME):
        return set()
    
    with open(FILE_NAME, mode='r') as file:
        content = file.read()
        return set(content.splitlines())


def save_hash(file_hash):
    """Append a hash to file."""
    with open(FILE_NAME, mode='a') as file:
        file.write(f"{file_hash}\n")


@app.route('/check-hash', methods=['POST'])
def check_hash():
    try:
        data = request.get_json()
        file_hash = data.get('file_hash', None)

        if file_hash is None:
            return jsonify({"error": "No file hash provided"}), 400

        file_hashes = load_hashes()
        if file_hash in file_hashes:
            return jsonify({"exists": True}), 200
        else:
            return jsonify({"exists": False}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/add-hash', methods=['POST'])
def add_hash():
    try:
        data = request.get_json()
        file_hash = data.get('file_hash', None)

        if file_hash is None:
            return jsonify({"error": "No file hash provided"}), 400

        file_hashes = load_hashes()
        if file_hash in file_hashes:
            return jsonify({"added": False, "reason": "File hash already exists"}), 200
        
        # Add the hash to the set and save it
        file_hashes.add(file_hash)
        save_hash(file_hash)
        return jsonify({"added": True}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=9150)
