# Meta-Cache

## Description

Meta-Cache is a simple Python-based microservices designed to provide caching mechanisms for hashed SHA256 strings. It aims to enhance the performance of distributed systems by reducing data retrieval times and improving resource utilization.

## Usage

### Docker
To start using Meta-Cache, you can either execute the main script with Python or use the Docker image available at `mattzh/meta-cache`:

```bash
docker run -d -p 9150:9150 mattzh/meta-cache
```

## API Endpoints

### POST /check-hash
- **Description**: Checks if a given file hash exists in the store.
- **Request Body**: JSON object with a key `file_hash`.
- **Responses**:
  - `200 OK`: Returns `{"exists": true}` if the hash exists, otherwise `{"exists": false}`.
  - `400 Bad Request`: Returns `{"error": "No file hash provided"}` if the `file_hash` is missing.
  - `500 Internal Server Error`: Returns `{"error": "error message"}` if an exception occurs.

### POST /add-hash
- **Description**: Adds a new file hash to the store.
- **Request Body**: JSON object with a key `file_hash`.
- **Responses**:
  - `201 Created`: Returns `{"added": true}` if the hash is successfully added.
  - `200 OK`: Returns `{"added": false, "reason": "File hash already exists"}` if the hash already exists.
  - `400 Bad Request`: Returns `{"error": "No file hash provided"}` if the `file_hash` is missing.
  - `500 Internal Server Error`: Returns `{"error": "error message"}` if an exception occurs.

### POST /remove-hash
- **Description**: Removes an existing file hash from the store.
- **Request Body**: JSON object with a key `file_hash`.
- **Responses**:
  - `200 OK`: Returns `{"removed": true}` if the hash is successfully removed.
  - `200 OK`: Returns `{"removed": false, "reason": "File hash does not exist"}` if the hash does not exist.
  - `400 Bad Request`: Returns `{"error": "No file hash provided"}` if the `file_hash` is missing.
  - `500 Internal Server Error`: Returns `{"error": "error message"}` if an exception occurs.

## License

This project is licensed under the terms of the LICENSE file.
