import random
from flask import Flask, request
from pymessenger.bot import Bot


app = Flask(__name__)
ACCESS_TOKEN = 'EAAfxh9KdiwoBAGXge1UL7yCNW8p02w1eglDBciLZCE57oG7pTc9A2Umx4ZAO4jkMpTrCOBDW6HbY21oYNba28KmN1pIjaP3m6jKgFlaLhJaTRJ0QG2eJfZCyhMPjJRWwo4LoyGFASn7XKEZChSRRAxpbS2W28pU5SvSkhYnNlQZDZD'
VERIFY_TOKEN = '5941526563'
bot = Bot(ACCESS_TOKEN)

_overall_sentiment = []
_state = ['']
# TODO m stands for mode, code breaks if we try to make m not a list for some reason
_m = [0]


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error 
    # print(token_sent)
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)


def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


@app.route('/', methods=['GET', 'POST'])
def receive_message():
    # Receive Verification token from facebook
    if request.method == 'GET':
        # Before allowing people to message your bot, Facebook has implemented a verify token
        # that confirms all requests that your bot receives came from Facebook. 
        token_sent = request.args.get("hub.verify_token")
        # print('hello')
        return verify_fb_token(token_sent)
    else:
        # ****TODO: INPUT AL-I WEBHOOK.PY CODE HERE****
        # get whatever message a user sent the bot
        output = request.get_json()
        print(output)
        # result = results(output)
        for event in output['entry']:
            messaging = event['messaging']
            # print(messaging)
            for message in messaging:
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    # If user passes in text
                    if message['message'].get('text'):
                        # response_sent_text = get_message()
                        response_sent_text = get_results(message)
                        send_message(recipient_id, response_sent_text)
                    #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        # response_sent_nontext = get_message()
                        response_sent_nontext = get_results()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

# function for responses
def get_results(user_text):

    utterance = ''

    if user_text['message'].get('text'):
        utterance = user_text['message'].get('text')

    # info = get_complex_tone(utterance)
    # print(info)

    response = "Hmm I see. I know something that might help if you are upset."
    print(_m)

    # if test is in slots, that means this request came from a business logic transition and response should already be correct
    #if '_TEST_' in req['slots']:
    #    print('test detected')
    #    return req

    if req.get('state') == 'sentiment_gathering' and len(_m) == 0:

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
        m[0] = 1

    elif req.get('state') == 'sentiment_gathering' and m[0] == 1:

        # get sentiment and record it
        sentiment, _ = get_tone(utterance)
        overall_sentiment.append(sentiment)

        # do action based on sentiment
        if sentiment == 'joy':

            response = "That's great to hear!"

        elif sentiment == 'anger' or sentiment == 'fear':

            # transition to breathing state
            req['state'] = "breathing"
            response = " This is a breathing exercise"
            m[0] = 0

        elif sentiment == 'sadness':

            # transition to mindfulness exercise
            # **for some reason, setting state in 'req' to mindfulness here messes things up, so weird.
            _state[0] = 'mindfulness'
            # req['state'] = 'mindfulness'
            response = "Hmm I see. I know something that might help if you are upset. It's a mindfulness exercise"
            m[0] = 0
        else:

            # I don't know what to say when given neutral response
            response = "How do you feel specifically about that?"

            m[0] = 1

        # set mode
        # m.pop()

    # MINDFULNESS EXERCISE
    elif req.get('state') == 'mindfulness' and _mindfulness_m[0] == 0:
        response = '''Let's try an observation exercise. It can be hard to be present in the moment, \
        especially when we're feeling anxious or overwhelmed with emotions. Let's try and get \
        back to the present and tackle the issues causing our anxiety later. Can you tell me \
        about the environment around you? Describe it in depth, even as far as telling me \
        the colors of the walls, and the physical sensations that you're feeling in the moment.'''
        _mindfulness_m[0] = 1

    elif req.get('state') == 'mindfulness' and _mindfulness_m[0] == 1:
        response, _neutral_tone_mindfulness[0] = mindfulness_followup1(req)
        if _neutral_tone_mindfulness[0] is False:
            _mindfulness_m[0] = 2
        else:
            _mindfulness_m[0] = 3

    elif req.get('state') == 'mindfulness_followup2' and _mindfulness_m[0] == 2:
        response, _neutral_tone_mindfulness[0] = mindfulness_followup2(req)
        if _neutral_tone_mindfulness[0] is False:
            _mindfulness_m[0] = 3

    elif req.get('state') == 'mindfulness_followup3' and _mindfulness_m[0] == 3:
        response, _neutral_tone_mindfulness[0] = mindfulness_followup3(req)
        # Set mode back to 0 after end of mindfulness exercise
        _mindfulness_m[0] = 0

    elif req.get('state') == 'student_issue':

        if '_EXAM_' in req['slots']:
            req['state'] = 'student_issue_exam'
            response = student_issue_followup1(req)

        elif '_HOMEWORK_' in req['slots']:
            new_state = 'student_issue_homework'

            if req['slots']['_HOMEWORK_']['values'][0]['tokens'] == 'webwork':
                if '_MATH_' in req['slots']:
                    response = student_issue_homework_math(req)
                    new_state = 'student_issue_course'

                elif '_SCIENCE_' in req['slots']:
                    response = student_issue_homework_science(req)
                    new_state = 'student_issue_course'

                elif '_EECS_' in req['slots']:
                    response = student_issue_homework_eecs(req)
                    new_state = 'student_issue_course'

                else:
                    response = student_issue_homework_webwork(req)

            else:
                if '_MATH_' in req['slots']:
                    response = student_issue_homework_math(req)
                    new_state = 'student_issue_course'

                elif '_SCIENCE_' in req['slots']:
                    response = student_issue_homework_science(req)
                    new_state = 'student_issue_course'

                elif '_EECS_' in req['slots']:
                    response = student_issue_homework_eecs(req)
                    new_state = 'student_issue_course'
                    
                else:
                    response = student_issue_homework(req)

            req['state'] = new_state
        else:
            response = "Classes can definitely be challenging and stressful, but I might have some advice to help out! Is it homework, an exam, or anything of the like concerning you?"

    elif req.get('state') == 'student_issue_exam':

        response = student_issue_followup1(req)

    elif req.get('state') == 'student_issue_study_buddy':
        if '_STUDENT_NAME_' in req['slots']:
            response = student_issue_followup2(req)
        else:
            response = student_issue_followup3(req)

    elif req.get('state') == 'student_issue_homework':
        if req['slots']['_HOMEWORK_']['values'][0]['tokens'] == 'webwork':
            if '_MATH_' in req['slots']:
                response = student_issue_homework_math(req)
                req['state'] = 'student_issue_course'

            elif '_SCIENCE_' in req['slots']:
                response = student_issue_homework_science(req)
                req['state'] = 'student_issue_course'

            elif '_EECS_' in req['slots']:
                response = student_issue_homework_eecs(req)
                req['state'] = 'student_issue_course'

            else:
                response = student_issue_homework_webwork(req)

        else:
            if '_MATH_' in req['slots']:
                response = student_issue_homework_math(req)
                req['state'] = 'student_issue_course'

            elif '_SCIENCE_' in req['slots']:
                response = student_issue_homework_science(req)
                req['state'] = 'student_issue_course'

            elif '_EECS_' in req['slots']:
                response = student_issue_homework_eecs(req)
                req['state'] = 'student_issue_course'
                
            else:
                response = student_issue_homework(req)

    elif req.get('state') == 'student_issue_course':
        if '_MATH_' in req['slots']:
            response = student_issue_homework_math(req)
                

        elif '_SCIENCE_' in req['slots']:
            response = student_issue_homework_science(req)
            

        elif '_EECS_' in req['slots']:
            response = student_issue_homework_eecs(req)
            
        else:
            response = student_issue_unknown(req)

    # Set response
    req['slots']['_TEST_'] = {"type": "string", "values": []}

    req['slots']['_TEST_']['values'].append({"tokens": "test", "resolved": 1, "value": response})

    
    print('this is the outgoing req')
    print(req)

    return req

# if __name__ == '__main__':
#     app.run(ssl_context='adhoc')
