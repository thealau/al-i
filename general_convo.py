def handle_general_convo(req, info):
    print('gen convo')
    print()

    response = 'EMPTY'

    if 'fear' in info or 'sadness' in info:
        response = "I'm so sorry to hear that! Sounds tough!"
    elif 'anger' in info:
        response = "That sounds aggravating!"
    elif 'joy' in info:
        response = "What a good day!"
    else:
        response = "That's interesting, thanks for sharing!"

    # trigger = req['slots']['_TRIGGER_']['values'][0]['tokens']

    print("RESPONSE IS: ", response)
    return response 