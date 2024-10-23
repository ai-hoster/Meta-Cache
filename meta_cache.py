from flask import Flask, request, jsonify
import aiofiles
import os
import atexit
import threading
import time

app = Flask(__name__)

# In-memory store of file hashes
file_hashes = set()
file_hash_lock = threading.Lock()

# File to store file hashes
FILE_NAME = 'file_hashes.txt'
UPDATE_INTERVAL = 60  # Update file every 60 seconds

def load_hashes():
    """Load hashes from file into a set."""
    if not os.path.exists(FILE_NAME):
        return set()
    
    with open(FILE_NAME, mode='r') as file:
        content = file.read()
        return set(content.splitlines())

def save_hashes_to_file():
    """Save all hashes to file."""
    with file_hash_lock:
        with open(FILE_NAME, mode='w') as file:
            for file_hash in file_hashes:
                file.write(f"{file_hash}\n")


def periodic_save():
    """Periodically save hashes to file."""
    while True:
        time.sleep(UPDATE_INTERVAL)
        save_hashes_to_file()

def on_exit():
    """Save hashes to file on exit."""
    save_hashes_to_file()

@app.route('/check-hash', methods=['POST'])
def check_hash():
    try:
        data = request.get_json()
        file_hash = data.get('file_hash', None)

        if file_hash is None:
            return jsonify({"error": "No file hash provided"}), 400

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

        with file_hash_lock:
            if file_hash in file_hashes:
                return jsonify({"added": False, "reason": "File hash already exists"}), 200
            # Add the hash to the set
            file_hashes.add(file_hash)

        return jsonify({"added": True}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/remove-hash', methods=['POST'])
def remove_hash():
    try:
        data = request.get_json()
        file_hash = data.get('file_hash', None)

        if file_hash is None:
            return jsonify({"error": "No file hash provided"}), 400

        with file_hash_lock:
            if file_hash not in file_hashes:
                return jsonify({"removed": False, "reason": "File hash does not exist"}), 200
            
        # Remove the hash from the set
        file_hashes.remove(file_hash)

        return jsonify({"removed": True}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Load hashes into memory at startup
    file_hashes = load_hashes()

    # # Start periodic save thread
    # save_thread = threading.Thread(target=periodic_save, daemon=True)
    # save_thread.start()

    # Register exit handler
    atexit.register(on_exit)

    app.run(debug=True, use_reloader=False, port=9150)
