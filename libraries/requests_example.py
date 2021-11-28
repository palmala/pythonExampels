import requests
from requests.auth import HTTPDigestAuth


username = "theuser"
password = "thepass"
response = requests.get("https://httpbin.org/status/200", timeout=1.0) # 404

# raise exception if status code is not 200
response.raise_for_status()
print(response.encoding)

# basic authentication
response = requests.get("https://httpbin.org/basic-auth/theuser/thepass", auth=(username, password))
print(response.status_code, response.text)

# digest auth
response = requests.get("https://httpbin.org/digest-auth/auth/theuser/thepass", auth=HTTPDigestAuth(username, password))
print(response.status_code, response.text)

# timeout
response = requests.get("https://httpbin.org/delay/2.5", timeout=1.0) # 404

# redirect
response = requests.get("http://github.com")
print(response.url)
print(response.history)

# session
session = requests.Session()
session.get("https://httpbin.org/cookies/set/sample/123456")
response = session.get("https://httpbin.org/cookies")

