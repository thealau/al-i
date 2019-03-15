import json
import flask
from mindfulness import mindfulness_followup1, mindfulness_followup2, mindfulness_followup3
from get_tone import get_tone

app = flask.Flask(__name__)

overall_sentiment = []
# TODO: change this solution  
neutral_tone_mindfulness = [False]

# default route
@app.route('/')
def index():
    return 'Hello World!'

# function for responses
def results():
    print(neutral_tone_mindfulness)
    print(overall_sentiment)
    # build a request object
    result = flask.request.get_json(force=True)
    # print(json.dumps(req, indent=4, sort_keys=True))
    print(result)

    # fetch action from json
    req = result.get('query')
    print(result)

    # if result.get('intent').get('displayName') == 'Default Welcome Intent':
    print(result.get('state'))
    if result.get('state') == 'IntroExplanation':
        if result.get('parameters').get('response') == 'yes':
            return {'query': '''My name is Al-i, and I am just that,
            your ally! My purpose is to be here for you without judgement.
            I've been trained to identify exactly how you're feeling, and to
            provide for you, and guide you through, a select set of targeted
            exercises to better equip you for the challenges life brings. Let's get started! Tell me, how are you doing today'''}
        else:
            return{'query':'''Okay, let's get started! Tell me, how are you doing today?'''}

    elif result.get('state') == "IntroExplanation - How Are You?":
        text = result.get('parameters')
        
        sentiment, _ = get_tone(text['anything'])
        overall_sentiment.append(sentiment)
        print("Overall Sent: ", overall_sentiment[0])

        if sentiment == 'joy':

            return {'query': ''' I'm glad to hear that! What has been good about your day? '''}
        elif sentiment == 'neutral':

            return {'query': ''' Thanks for sharing! '''}

        else:
            return {'query': ''' I'm sorry to hear that, would you like to talk about what's going on? '''}
    
    elif result.get('state') == "IntroExplanation - How Are You? - followup":
        if result.get('parameters').get('response') == 'yes':

            return{'query': ''' Thanks for being open with me! I'm all ears. '''}
        
        elif overall_sentiment[0] == 'anger' or overall_sentiment[0] == 'sadness' or overall_sentiment[0] == 'disgust':
            
            return{'query': ''' I understand! Let's see how I can help. I know of a breathing exercise that can help reduce anxiety. If you would like to try it, say breathe. '''}

        else:
            # TODO, initiate other exercises
            return{'query': ''' Hmm let me think of some exercises I can help you out with '''}

    # MINDFULNESS EXERCISE
    elif result.get('state') == 'mindfulness':
        print('hello')
        return{'query': '''Let’s try an observation exercise. It can be hard to be present in the moment, \
        especially when we’re feeling anxious or overwhelmed with emotions. Let’s try and get \
        back to the present and tackle the issues causing our anxiety later. Can you tell me \
        about the environment around you? Describe it in depth, even as far as telling me \
        the colors of the walls, and the physical sensations that you’re feeling in the moment.'''}

    elif result.get('state') == 'mindfulness_followup1' and not neutral_tone_mindfulness[0]:
        query, neutral_tone_mindfulness[0] = mindfulness_followup1(req)
        return query

    elif result.get('state') == 'mindfulness_followup2' and not neutral_tone_mindfulness[0]:
        query, neutral_tone_mindfulness[0] = mindfulness_followup2(req)
        return query

    elif result.get('state') == 'mindfulness_followup3' and not neutral_tone_mindfulness[0]:
        query, neutral_tone_mindfulness[0] = mindfulness_followup3(req)
        return query

    # return a fulfillment response
    return {'query': '''Okay, that's all for today. It was great talking to you and hearing about how you are doing!'''}

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
