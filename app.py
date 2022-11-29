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
        subscriber_id = request.args.get('subscriber_id')
        topic = request.args.get('topic')
        if not topic or not subscriber_id:
            return Response(status=400, response="Missing subscriber_id or topic")
        subscriber_id = int(subscriber_id)
        topic = str(topic)
        sub_obj = communicator.subscribe(topic)
        if (subscriber_id in subscriber_map) and (topic in subscriber_map[subscriber_id]):
            return Response(status=200, response="Subscriber is already subscribed to the topic") 
        subscriber_map[subscriber_id][topic] = sub_obj
        return Response(status=200, response="Subscribed to the topic {}".format(topic))
    except Exception as e:
        error = "GET route /subscribe error: {}".format(e)
        print(error)
        return Response(status=400, response=error)


@app.route('/unsubscribe', methods=["GET"])
def unsubscribe():
    try:
        subscriber_id = request.args.get('subscriber_id')
        topic = request.args.get('topic')
        if not topic or not subscriber_id:
            return Response(status=400, response="Missing subscriber_id or topic")
        subscriber_id = int(subscriber_id)
        topic = str(topic)
        if (subscriber_id in subscriber_map) and (topic in subscriber_map[subscriber_id]):
            communicator.unsubscribe(topic, subscriber_map[subscriber_id][topic])
            del subscriber_map[subscriber_id][topic]
            return Response(status=200, response="Successfully unsubscribed from the topic: {}".format(topic))
        else:
            return Response(status=200, response="Subscriber does not exist or haven't subscribed to: {}".format(topic))
    except Exception as e:
        error = "GET route /unsubscribe error: {}".format(e)
        print(error)
        return Response(status=400, response=error)

@app.route('/get_all_messages', methods=["GET"])
def get_all_messages():
    try:
        subscriber_id = int(request.args.get('subscriber_id'))
        topic = str(request.args.get('topic'))
        if not topic or not subscriber_id:
            return Response(status=400, response="Missing subscriber_id or topic")
        subscriber_id = int(subscriber_id)
        topic = str(topic)
        data = []
        if (subscriber_id in subscriber_map) and (topic in subscriber_map[subscriber_id]):
            for message in subscriber_map[subscriber_id][topic].listen():
                data.append(message.get("data"))
        return Response(status=200, response=json.dumps({"result":data}))
    except Exception as e:
        error = "GET route /get_all_messages error: {}".format(e)
        print(error)
        return Response(status=400, response=error)

@app.route('/publish', methods=["POST"])
def publish():
    try:
        status_code = 200
        json = request.get_json(force=True)
        if not json:
            status_code = 400
            msg = "problem pasrsing the request body JSON"
        if "topic" not in json:
            status_code = 400
            msg = "topic is missing in the request body JSON"
        if "message" not in json:
            status_code = 400
            msg = "message is missing in the request body JSON"
        communicator.publish(json.get("topic"), json.get("message"))
        msg = "Successfully published message: \"{}\" under topic: {}".format(json.get("message"), json.get("topic"))
        return Response(status=status_code, response=msg)
    except Exception as e:
        error = "POST route /publish error: {}".format(e)
        print(error)
        return Response(status=400, response=error)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8050)
