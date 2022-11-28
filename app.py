from flask import Flask, render_template, request, Response, json
from collections import defaultdict
from pubsub import PubSub
import os


app = Flask(__name__, static_url_path='/static')
communicator = PubSub()
# {"1": {"sports":obj1, "basketball":obj2}}
subscriber_map = defaultdict(dict)
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
        if (subscriber_id in subscriber_map) and (topic in subscriber_map[subscriber_id]):
            return Response(status=400, response="Subscriber is already subscribed to the topic") 
        subscriber_map[subscriber_id][topic] = sub_obj
        return Response(status=200, response="Subscribed to the topic {}".format(topic))
    except Exception as e:
        print("GET route /subscribe error: {}".format(e))
        return Response(status=400)


@app.route('/unsubscribe', methods=["GET"])
def unsubscribe():
    try:
        subscriber_id = int(request.args.get('subscriber_id'))
        topic = str(request.args.get('topic'))
        if (subscriber_id in subscriber_map) and (topic in subscriber_map[subscriber_id]):
            communicator.unsubscribe(topic, subscriber_map[subscriber_id][topic])
            del subscriber_map[subscriber_id][topic]
            return Response(status=200, response="Successfully unsubscribed from the topic: {}".format(topic))
        else:
            return Response(status=400, response="Subscriber does not exist or haven't subscribed to: {}".format(topic))
    except Exception as e:
        print("GET route /unsubscribe error: {}".format(e))
        return Response(status=400)

@app.route('/get_all_messages', methods=["GET"])
def get_all_messages():
    try:
        subscriber_id = int(request.args.get('subscriber_id'))
        topic = str(request.args.get('topic'))
        data = {}
        if (subscriber_id in subscriber_map) and (topic in subscriber_map[subscriber_id]):
            for message in subscriber_map[subscriber_id][topic].listen():
                data["result"].append(message)
        return Response(status_code=201, response=json.dumps(data))
    except Exception as e:
        print("GET route /get_all_messages error:".format(e))
        return Response(status=400)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8050)
