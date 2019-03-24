import json
import flask
from mindfulness import mindfulness_followup1, mindfulness_followup2, mindfulness_followup3
from get_tone import get_tone

app = flask.Flask(__name__)

overall_sentiment = []

response = "hello world"

# TODO m stands for mode, code breaks if we try to make m not a list for some reason
m = []

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
    req = flask.request.get_json(force=True)

    # print out request
    print(req)

    # print query from request
    print("user said " + req.get('query'))

    utterance = req.get('query')

    # print state request came from
    print("coming from state" + req.get('state'))

    response = "hello world - dy"
    #response = "Hmm I see. I know something that might help if you are upset."

    if req.get('state') == 'sentiment_gathering' and len(m) == 0:

        # get sentiment and record it
        sentiment, _ = get_tone(utterance)
        overall_sentiment.append(sentiment)

        # do action based on sentiment
        if sentiment == 'joy':

            response = '''Of course, let's chat! Tell me, how are you doing today?'''

        elif sentiment == 'neutral':
            response = '''I'm all ears. What's been going on?'''

        else:
            if "feel" not in utterance:
                response = '''I'm sorry to hear that. How are you feeling right now?'''
            else:
                response = '''I'm sorry to hear that. What's been going on?'''

        # set mode
        m.append(1)

    elif req.get('state') == 'sentiment_gathering' and len(m) == 1:

        # get sentiment and record it
        sentiment, _ = get_tone(utterance)
        overall_sentiment.append(sentiment)


        # do action based on sentiment
        if sentiment == 'joy':

            response = "That's great to hear!"

        elif sentiment == 'anger' or sentiment == 'anxiety':

            # transition to breathing state
            req['state'] = "breathing"
            response = " This is a breathing exercise"

        elif sentiment == 'disgust' or sentiment == 'sadness':

            # transition to mindfulness exercise
            req['state'] = 'mindfulness'

        else:

            # I don't know what to say when given neutral response
            response = "I see. Tell me more about what's going on"

            m.append(1)

        # set mode
        m.pop()

    elif req.get('state') == 'introduction':

        response = '''My name is Al-i, and I am just that,
        your ally! My purpose is to be here for you without judgement.
        I've been trained to identify exactly how you're feeling, and to
        provide for you, and guide you through, a select set of targeted
        exercises to better equip you for the challenges life brings. Go ahead and tell me how you are feeling!'''

    # MINDFULNESS EXERCISE
    elif req.get('state') == 'mindfulness':
        response = '''Let's try an observation exercise. It can be hard to be present in the moment, \
        especially when we're feeling anxious or overwhelmed with emotions. Let's try and get \
        back to the present and tackle the issues causing our anxiety later. Can you tell me \
        about the environment around you? Describe it in depth, even as far as telling me \
        the colors of the walls, and the physical sensations that you're feeling in the moment.'''

    elif req.get('state') == 'mindfulness_followup1' and not neutral_tone_mindfulness[0]:
        response, neutral_tone_mindfulness[0] = mindfulness_followup1(req)

    elif req.get('state') == 'mindfulness_followup2' and not neutral_tone_mindfulness[0]:
        response, neutral_tone_mindfulness[0] = mindfulness_followup2(req)

    elif req.get('state') == 'mindfulness_followup3' and not neutral_tone_mindfulness[0]:
        response, neutral_tone_mindfulness[0] = mindfulness_followup3(req)


    # check state
    req['slots']['_TEST_'] = {"type": "string", "values": []}

    req['slots']['_TEST_']['values'].append({"tokens": "test", "resolved": 1, "value": response})


    print(req)
    print("webhook successful")



    return req
    

def check_output_context(result, output_context):
    output_contexts = req.get('outputContexts')
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
