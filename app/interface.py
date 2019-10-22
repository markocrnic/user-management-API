from flask import Flask, request
from flask_cors import CORS
import implementation as implementation


app = Flask(__name__)
CORS(app)


@app.route('/usermanagement/login/', methods=['POST'])
def login():
    return implementation.checkLogin(request, False)


@app.route('/usermanagement/adminlogin/', methods=['POST'])
def admin_login():
    return implementation.checkLoginAdmin(request, True)


@app.route('/usermanagement/register/', methods=['POST'])
def register():
    return implementation.checkRegister(request)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
