#!/usr/bin/env python3
from fastapi.testclient import TestClient
from main import app
import unittest

class TestFastApiWebserver(unittest.TestCase):
	client = TestClient(app)
	
	def test_read_main(self):
		response = TestFastApiWebserver.client.get("/")
		print(TestFastApiWebserver.client.__dict__)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {"msg": "Hello-bello"})


if __name__ == '__main__':
	unittest.main()
