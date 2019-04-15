def handle_panic_advice(req):
    health_trigger = ['headache', 'stomach', 'stomach ache', 'sick', 'pain']
    fight_trigger = ['fight', 'argument', 'disagreement', 'fighting']
    print('PANIC ADVICE')
    print()

    response = 'EMPTY'

    if '_TRIGGER_' in req['slots']:
        print('found trigger')
        trigger = req['slots']['_TRIGGER_']['values'][0]['tokens']
        trigger_split = trigger.split()
        trigger_type = ""
        for word in trigger_split:
            if word in health_trigger:
                trigger_type = 'health'
            elif word in fight_trigger:
                trigger_type = 'fight'

        if '_LOCATION_' in req['slots']:
            print('found location')
            loc = req['slots']['_LOCATION_']['values'][0]['tokens']
            if loc == 'home':
                if trigger_type == 'health':
                    response = panic_advice_home_health(req)
                elif trigger_type == 'fight':
                    response = panic_advice_home_fight(req)
                else:
                    response = '''ERROR IN LOCATION'''
            elif loc == 'work':
                if trigger_type == 'health':
                    response = panic_advice_work_health(req)
                elif trigger_type == 'fight':
                    response = panic_advice_work_fight(req)
                else:
                    response = '''ERROR IN LOCATION'''

            elif loc == 'school':
                if trigger_type == 'health':
                    response = panic_advice_school_health(req)
                elif trigger_type == 'fight':
                    response = panic_advice_school_fight(req)
                else:
                    response = '''ERROR IN LOCATION'''

            else:
                response = '''ERROR IN LOCATION'''
        else:
            if trigger_type == "":
                response = panic_advice_unknown(req)
            elif trigger_type == 'health':
                response = panic_advice_health(req)
            elif trigger_type == 'fight':
                response = panic_advice_fight(req)
            else:
                response = '''ERROR''' 

    return response   

def panic_advice_school_fight(req):
    output = '''school fight'''
    return output

def panic_advice_work_fight(req):
    output = '''work fight'''
    return output

def panic_advice_home_fight(req):
    output = '''home_fight'''
    return output

def panic_advice_school_health(req):
    output = '''school_health'''
    return output

def panic_advice_work_health(req):
    output = '''work_health'''
    return output

def panic_advice_home_health(req):
    output = '''home_health'''
    return output

def panic_advice_health(req):
    output = '''just health'''
    return output

def panic_advice_fight(req):
    output = '''just fight'''
    return output

def panic_advice_unknown(req):
    output = '''I'm so sorry to hear that. I've never dealt with that situation, so I don't have any advice. make sure you keep breathing and reach out to someone you know if you need more help!'''
    return output