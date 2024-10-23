import unittest
import json
from meta_cache import app

class MetaCacheTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.app = app.test_client()
        self.app.testing = True

        # Clean up the file hash store
        self.clean_file_hashes()

    def tearDown(self):
        # Clean up after tests
        self.clean_file_hashes()

    def clean_file_hashes(self):
        """Helper function to clean the file hash store."""
        try:
            open('file_hashes.txt', 'w').close()
        except FileNotFoundError:
            pass

    def test_add_hash(self):
        # Test adding a new file hash
        response = self.app.post('/add-hash', 
                                 data=json.dumps({"file_hash": "123456"}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("added", response.json)
        self.assertEqual(response.json['added'], True)

    def test_add_existing_hash(self):
        # First, add the hash
        self.app.post('/add-hash', 
                      data=json.dumps({"file_hash": "654321"}),
                      content_type='application/json')

        # Try adding the same hash again
        response = self.app.post('/add-hash', 
                                 data=json.dumps({"file_hash": "654321"}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("added", response.json)
        self.assertEqual(response.json['added'], False)
        self.assertIn("reason", response.json)

    def test_check_existing_hash(self):
        # First, add the hash
        self.app.post('/add-hash', 
                      data=json.dumps({"file_hash": "abcdef"}),
                      content_type='application/json')

        # Now check if the hash exists
        response = self.app.post('/check-hash', 
                                 data=json.dumps({"file_hash": "abcdef"}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("exists", response.json)
        self.assertEqual(response.json['exists'], True)

    def test_check_nonexistent_hash(self):
        # Check for a hash that hasn't been added
        response = self.app.post('/check-hash', 
                                 data=json.dumps({"file_hash": "zyxwvu"}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("exists", response.json)
        self.assertEqual(response.json['exists'], False)

    def test_no_file_hash_provided(self):
        # Test what happens if no file hash is provided
        response = self.app.post('/add-hash',
                                 data=json.dumps({}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

        response = self.app.post('/check-hash',
                                 data=json.dumps({}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

if __name__ == '__main__':
    unittest.main()
