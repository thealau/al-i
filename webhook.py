import json
import flask
from mindfulness import mindfulness_followup1, mindfulness_followup2, mindfulness_followup3
from student_issue import student_issue_followup1, student_issue_followup2, student_issue_followup3, student_issue_homework, student_issue_homework_math, student_issue_homework_science, student_issue_homework_eecs, student_issue_homework_webwork, student_issue_unknown, student_issue_homework_fear, student_issue_grades
from panic_advice import *
from general_convo import *
from get_tone import get_tone, get_complex_tone

app = flask.Flask(__name__)

overall_sentiment = []


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
    print('this is the incoming request')
    print(req)

    # print query from request
    print("user said " + req.get('query'))

    utterance = req.get('query')

    info = get_complex_tone(utterance)
    print(info)

    # print state request came from
    print("coming from state " + req.get('state'))

    response = "Thanks for sharing."

    if req.get('state') == 'panic_affirm':
        response = handle_panic_advice(req)
    
    elif req.get('state') == 'general_convo':
        response = handle_general_convo(req, info)
        req['state'] = 'positive_followup'

    elif req.get('state') == 'student_issue':

        if '_EXAM_' in req['slots']:
            req['state'] = 'student_issue_exam'
            response = student_issue_followup1(req)

        elif '_HOMEWORK_' in req['slots']:
            new_state = 'student_issue_homework'
            if 'fear' in info:
                response = student_issue_homework_fear(req)

            elif req['slots']['_HOMEWORK_']['values'][0]['tokens'] == 'webwork':
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

        elif '_GRADES_' in req['slots']:
            req['state'] = 'student_issue_grades'
            response = student_issue_grades(req)

        else:
            response = "Classes can definitely be challenging and stressful, but I might have some advice to help out! Is it homework, an exam, grades, or anything of the like concerning you?"

    elif req.get('state') == 'student_issue_exam':

        response = student_issue_followup1(req)

    elif req.get('state') == 'student_issue_study_buddy':
        if '_STUDENT_NAME_' in req['slots']:
            response = student_issue_followup2(req)
        else:
            response = student_issue_followup3(req)

    elif req.get('state') == 'student_issue_homework':
        if 'fear' in info:
            response = student_issue_homework_fear(req)
        elif req['slots']['_HOMEWORK_']['values'][0]['tokens'] == 'webwork':
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

    elif req.get('state') == "student_issue_grades":
        response = student_issue_grades(req)

    # Set response
    req['slots']['_TEST_'] = {"type": "string", "values": []}

    req['slots']['_TEST_']['values'].append({"tokens": "test", "resolved": 1, "value": response})
    
    print('this is the outgoing req')
    print(req)

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
