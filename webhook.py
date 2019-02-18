# import flask dependencies
import json
# from df_response_lib import response_format as rf
import flask
from mindfulness import mindfulness_followup1, mindfulness_followup2, mindfulness_followup3
from get_tone import get_tone

app = flask.Flask(__name__)

overall_sentiment = []
neutral_tone_mindfulness = False

# default route
@app.route('/')
def index():
    return 'Hello World!'

# function for responses
def results():
    print(neutral_tone_mindfulness)
    # build a request object
    req = flask.request.get_json(force=True)
    # print(json.dumps(req, indent=4, sort_keys=True))

    # fetch action from json
    result = req.get('queryResult')
    print(result)

    # if result.get('intent').get('displayName') == 'Default Welcome Intent':

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
        
        sentiment, _ = get_tone(text['anything'])
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

    # Mindfullness Exercise
    # Check if outputContext list contains target Context (TODO: What if this list is empty)
    # elif result.get('intent').get('displayName') == 'MindfulnessExercise': # and check_output_context(result, 'mindfulnessexercise-followup1'):
    #     return mindfulness(req)

    # print(result.get('intent').get('displayName'))
    elif result.get('intent').get('displayName') == 'MindfulnessExercise - followup' and not neutral_tone_mindfulness:#and check_output_context(result, 'mindfulnessexercise-followup2'):
        return mindfulness_followup1(req, neutral_tone_mindfulness)

    elif result.get('intent').get('displayName') == 'MindfulnessExercise - followup2' and not neutral_tone_mindfulness:#and check_output_context(result, 'mindfulnessexercise-followup2'):
        return mindfulness_followup2(req, neutral_tone_mindfulness)

    elif result.get('intent').get('displayName') == 'MindfulnessExercise - followup3' and not neutral_tone_mindfulness:#and check_output_context(result, 'mindfulnessexercise-followup2'):
       return mindfulness_followup3(req, neutral_tone_mindfulness)

    # elif result.get('intent').get('displayName') == 'MindfulnessExercise - fallback':
    #     return mindfulness_first(req)

    # return a fulfillment response
    return {'fulfillmentText': '''Ok, that's all for today. It was great talking to you and hearing about how you are doing!'''}

def check_output_context(result, output_context):
    output_contexts = result.get('outputContexts')
    # loop through dicts to find target output context
    for output_context_dict in output_contexts:
        if output_context in output_context_dict['name']:
            return True
    return False


# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return flask.make_response(flask.jsonify(results()))

# run the app
if __name__ == '__main__':
   webhook.app.run()
