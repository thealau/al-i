# import flask dependencies
import json
from df_response_lib import response_format as rf
import flask

app = flask.Flask(__name__)

# default route
@app.route('/')
def index():
    return 'Hello World!'

# function for responses
def results():
    # build a request object
    req = flask.request.get_json(force=True)
    print(json.dumps(req, indent=4, sort_keys=True))

    # fetch action from json
    result = req.get('queryResult')

    if result.get('intent').get('displayName') == 'IntroExplanation':
        if result.get('parameters').get('response') == 'yes':
            return {'fulfillmentText': '''My name is Al-i, and I am just that,
            your ally! My purpose is to be here for you without judgement.
            I've been trained to identify exactly how you're feeling, and to
            provide for you, and guide you through, a select set of targeted
            exercises to better equip you for the challenges life brings.'''}
        else:
            return{'fulfillmentText':'response sent from webhook'}


    # return a fulfillment response
    return {'fulfillmentText': '''Hello, I'm Al-i! I’m so happy to meet you, $name.
    My mission is to support you in your journey towards adopting mindfulness and a
    more positive outlook for better overall mental well being. Before we begin, 
    would you like to know how I work, and how I can help?'''}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return flask.make_response(flask.jsonify(results()))

# run the app
if __name__ == '__main__':
   webhook.app.run()