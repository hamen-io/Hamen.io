from flask import (Flask,request,jsonify)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/htaccess-getter")
def htaccess_getter():
    return 

@app.route("/htaccess-setter", methods=["POST"])
def htaccess_setter():
    data = jsonify(request.get_data())
    return ""

if __name__ == '__main__':
    app.run(debug=True)
