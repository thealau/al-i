# import flask dependencies
import json
# from df_response_lib import response_format as rf
import flask
from mindfulness import mindfulness,mindfulness_first
from get_tone import get_tone

app = flask.Flask(__name__)

overall_sentiment = []

# default route
@app.route('/')
def index():
    return 'Hello World!'

# function for responses
def results():
    # build a request object
    req = flask.request.get_json(force=True)
    # print(json.dumps(req, indent=4, sort_keys=True))

    # fetch action from json
    result = req.get('queryResult')

    if result.get('intent').get('displayName') == 'IntroExplanation':
        if result.get('parameters').get('response') == 'yes':
            return {'fulfillmentText': '''My name is Al-i, and I am just that,
            your ally! My purpose is to be here for you without judgement.
            I've been trained to identify exactly how you're feeling, and to
            provide for you, and guide you through, a select set of targeted
            exercises to better equip you for the challenges life brings. Let's get started! Tell me, how are you doing today'''}
        else:
            return{'fulfillmentText':'''Okay, let's get started! Tell me, how are you doing today?'''}

    elif result.get('intent').get('displayName') == "IntroExplanation - How Are You?":
        text = result.get('parameters')
        
        sentiment = get_tone(text['anything'])
        overall_sentiment.append(sentiment)
        print("Overall Sent: ", overall_sentiment[0])

        if sentiment == 'joy':

            return {'fulfillmentText': ''' I'm glad to hear that! What has been good about your day? '''}
        elif sentiment == 'neutral':

            return {'fulfillmentText': ''' Thanks for sharing! '''}

        else:
            return {'fulfillmentText': ''' I'm sorry to hear that, would you like to talk about what's going on? '''}
    
    elif result.get('intent').get('displayName') == "IntroExplanation - How Are You? - followup":
        if result.get('parameters').get('response') == 'yes':

            return{'fulfillmentText': ''' Thanks for being open with me! I'm all ears. '''}
        
        elif overall_sentiment[0] == 'anger' or overall_sentiment[0] == 'sadness' or overall_sentiment[0] == 'disgust':
            
            return{'fulfillmentText': ''' I understand! Let's see how I can help. I know of a breathing exercise that can help reduce anxiety. If you would like to try it, say breathe. '''}

        else:
            # TODO, initiate other exercises
            return{'fulfillmentText': ''' Hmm let me think of some exercises I can help you out with '''}


    elif result.get('intent').get('displayName') == 'MindfulnessExercise':
        return mindfulness(req)

    elif result.get('intent').get('displayName') == 'MindfulnessExercise - fallback':
        return mindfulness_first(req)


    # return a fulfillment response
    return {'fulfillmentText': '''Hello, I'm Al-i! I'm so happy to meet you! My mission is to support you in your journey towards adopting mindfulness and a more positive outlook for better overall mental well being. Before we begin, would you like to know how I work, and how I can help?'''}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return flask.make_response(flask.jsonify(results()))

# run the app
if __name__ == '__main__':
   webhook.app.run()
