from flask import Flask, render_template
import os

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8050)
