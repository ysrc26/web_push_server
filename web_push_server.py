from Utils import push_manager, mongodb
# from bottle import Bottle, request, response, run, server_names, ServerAdapter
from bottle import *
from bson import json_util
import json

g_mongo_manager_singleton = None

app = Bottle()


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/save_subscription', method=['POST', 'OPTIONS'])
def save_subscription():
    if request.method == 'OPTIONS':
        return json.dumps({})
    else:
        obj = request.json
        subscription = request.json['subscription']
        sub_dict = {
            "site": "site",
            "subscription": subscription}
        db_instance = g_mongo_manager_singleton.get_db_instance()
        subscriptions_collection = db_instance["subscriptions"]
        inserted_id = subscriptions_collection.insert_one(sub_dict)
        if inserted_id:
            return json.dumps(sub_dict, indent=4, sort_keys=False, default=json_util.default)
        else:
            return json.dumps(False)


@app.route('/send_web_push', method=['POST'])
def send_web_push():
    push_result = push_manager.send_web_push(
        request.json['subscription_info'],
        request.json['data'],
        request.json['private_key']
    )
    return json.dumps(push_result)


@app.route('/send_push_to_all', method=['POST'])
def send_push_to_all():
    json_data = request.json['request']
    private_key = "Jg4ehhzcSMqIZA6E8FD0cyz8OK62KAcDKrzwzv8wfYI"
    # private_key = json_data['private_key']
    data = "Push is working!"
    db_instance = g_mongo_manager_singleton.get_db_instance()
    subscriptions_collection = db_instance["subscriptions"]
    for subscription in subscriptions_collection.find({}, {"subscription": 1}):
        push_manager.send_web_push(subscription, data, private_key)

    return json.dumps("Push to all sent!")


@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    response.content_type = 'application/json'


@app.error(500)
def error500(error_msg):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    print str(error_msg.body)
    response.content_type = 'application/json'
    return 'Exception: %s' % str(error_msg.body)


def db_init():
    global g_mongo_manager_singleton
    if not g_mongo_manager_singleton:
        g_mongo_manager_singleton = mongodb.MongoDB("mongodb://34.254.61.254:27017/", "web_push")


db_init()

# class SSLWSGIRefServer(ServerAdapter):
#     def run(self, handler):
#         from wsgiref.simple_server import make_server, WSGIRequestHandler
#         import ssl
#         if self.quiet:
#             class QuietHandler(WSGIRequestHandler):
#                 def log_request(*args, **kw): pass
#
#             self.options['handler_class'] = QuietHandler
#         srv = make_server(self.host, self.port, handler, **self.options)
#         srv.socket = ssl.wrap_socket(
#             srv.socket,
#             certfile='server.pem',  # path to certificate
#             server_side=True)
#         srv.serve_forever()
#
#
# web_push_server = SSLWSGIRefServer(host='0.0.0.0', port='8888')

# app.run(host='0.0.0.0', port=8888)
# run(server=web_push_server)
# run(app=app, host='0.0.0.0', port=8888)

if __name__ == '__main__':
    run(app=app)
