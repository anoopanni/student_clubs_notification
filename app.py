from flask import Flask, render_template, request, Response
from pubsub import PubSub
import os


app = Flask(__name__, static_url_path='/static')
communicator = PubSub()
subscriber_map = {}
subscriber_id = 0

@app.route('/', methods=["GET"])
def home():
    global subscriber_id
    subscriber_id += 1
    return render_template('index.html', subscriber_id=subscriber_id)

# curl -IX GET http://localhost:8050/subscribe?subscriber_id=123&topic="sports"
# curl -IX GET http://localhost:8050/subscribe\?subscriber_id\=123\&topic\="sports"
@app.route('/subscribe', methods=["GET"])
def subscribe():
    try:
        subscriber_id = int(request.args.get('subscriber_id'))
        topic = str(request.args.get('topic'))
        sub_obj = communicator.subscribe(topic)
        if subscriber_id in subscriber_map and subscriber_map[subscriber_id][1] == topic:
            return Response(status=400, response="subscriber is already subscribed to the topic") 
        subscriber_map[subscriber_id] = (sub_obj, topic)
        return Response(status=201, response="Subscribed to the topic {}".format(topic))
    except Exception as e:
        print("GET route /subscribe error: {}".format(e))


@app.route('/unsubscribe', methods=["GET"])
def unsubscribe():
    try:
        subscriber_id = int(request.args.get('subscriber_id'))
        topic = str(request.args.get('topic'))
        if subscriber_id in subscriber_map and subscriber_map[subscriber_id][1] == topic:
            return Response(status=400, response="subscriber is already subscribed to the topic") 
        return Response(status=201)
    except Exception as e:
        print("GET route /unsubscribe error: {}".format(e))

@app.route('/get_all_messages', methods=["GET"])
def get_all_messages():
    try:
        subscriber_id = int(request.args.get('subscriber_id'))
        topic = str(request.args.get('topic'))


        return Response(status_code=201)

    except Exception as e:
        print("GET route /get_all_messages error:".format(e))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8050)
