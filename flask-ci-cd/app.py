from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Hello from Flask CI/CD Pipeline!")

@app.route('/health')
def health():
    return jsonify(status="healthy")

@app.route('/db-test')
def db_test():
    return jsonify(db="connected")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
