from flask import Flask, render_template
from pubsub import PubSub
import os


app = Flask(__name__, static_url_path='/static')

subscriber_id = -1

@app.route('/')
def home():
    global subscriber_id
    subscriber_id += 1
    return render_template('index.html', subscriber_id=subscriber_id)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8050)
