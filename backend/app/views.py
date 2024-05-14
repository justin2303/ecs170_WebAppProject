from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/example', methods=['GET'])
def example():
    if request.method == 'GET':
        # Your logic for GET request here
        return 'This is a GET request!'
    else:
        return 'Method not allowed', 405

if __name__ == '__main__':
    app.run(debug=True)
