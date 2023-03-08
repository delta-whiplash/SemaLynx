from flask import Flask, render_template, jsonify, request
import ping3
import subprocess

liste_semabox = ["semabox1", "semabox2", "semabox3"]
app = Flask(__name__)
# default page
@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)