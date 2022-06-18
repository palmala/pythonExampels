from flask import Flask, request, jsonify
import random
import time

app = Flask(__name__)


@app.route("/", methods=['GET'])
def main():
    time.sleep(1)
    if request.method == 'GET':
        data = {
            "value": str(random.randint(1, 20))
        }
        return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
