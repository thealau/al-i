def handle_panic_advice(req):
    health_trigger = ['headache', 'stomach', 'stomach ache', 'sick', 'pain']
    fight_trigger = ['fight', 'argument', 'disagreement', 'fighting']
    print('PANIC ADVICE')
    print()

    response = 'EMPTY'

    if '_TRIGGER_' in req['slots']:
        print('found trigger')
        print(req['slots']['_TRIGGER_'])
        print()

        trigger = req['slots']['_TRIGGER_']
        trigger_split = trigger[0].split()
        trigger_type = ""
        for word in trigger_split:
            print(word)
            if word in health_trigger:
                trigger_type = 'health'
            elif word in fight_trigger:
                trigger_type = 'fight'

        if '_LOCATION_' in req['slots']:
            print('found location')
            loc = req['slots']['_LOCATION_'][0]
            if loc == 'home':
                if trigger_type == 'health':
                    response = panic_advice_home_health(req)
                elif trigger_type == 'fight':
                    response = panic_advice_home_fight(req)
                else:
                    response = "ERROR IN LOCATION"
            elif loc == 'work':
                if trigger_type == 'health':
                    response = panic_advice_work_health(req)
                elif trigger_type == 'fight':
                    response = panic_advice_work_fight(req)
                else:
                    response = "ERROR IN LOCATION"

            elif loc == 'school':
                if trigger_type == 'health':
                    response = panic_advice_school_health(req)
                elif trigger_type == 'fight':
                    response = panic_advice_school_fight(req)
                else:
                    response = "ERROR IN LOCATION"

            else:
                response = "ERROR IN LOCATION"
        else:
            if trigger_type == "":
                response = panic_advice_unknown(req)
            elif trigger_type == 'health':
                response = panic_advice_health(req)
            elif trigger_type == 'fight':
                response = panic_advice_fight(req)
            else:
                response = "ERROR" 
    print("RESPONSE IS: ", response)
    return response   

def panic_advice_school_fight(req):
    output = '''school_fight: Working with other students can be hard. \
        Many schools have mental health support available should you decide that's necessary. \
        There may also be faculty available if you're having problems working with others students. \
        Be kind to yourself, and make sure you're reaching out for help with friends and students when you need it! \
        How are you feeling now? Are you feeling better, or would you like to talk more?'''
    return output

def panic_advice_work_fight(req):
    output = '''work_fight: Professional relationships can be confusing to navigate. \
        If your work has a human resources department, you can reach out to them for support. \
        If not, make sure to reach out to your friends and family for support when work gets tough. \
        Many people want to "leave work at work," which can be healthy, but we need to make sure to reach out for support when \
            work gets really tough. \
        How are you feeling now? Are you feeling better, or would you like to talk more?'''
    return output

def panic_advice_home_fight(req):
    output = '''home_fight: Family problems can be difficult to navigate, especially if they're very personal. \
        How are you feeling now? Are you feeling better, or would you like to talk more?'''
    return output

def panic_advice_school_health(req):
    output = '''school_health: Having a health problem at school can be really scary, but is one of the safer places you can be should something happen. \
        Make sure you've told someone about this health issue if it's recurring, especially if it's actually scaring you. \
        Having someone to support you can help a lot and take away a little bit of that fear and feeling of helplessness. \
        How are you feeling now? Are you feeling better, or would you like to talk more?'''
    return output

def panic_advice_work_health(req):
    output = '''work_health: \
        How are you feeling now? Are you feeling better, or would you like to talk more?'''
    return output

def panic_advice_home_health(req):
    output = '''home_health: \
        How are you feeling now? Are you feeling better, or would you like to talk more?'''
    return output

def panic_advice_health(req):
    output = '''just health: \
        How are you feeling now? Are you feeling better, or would you like to talk more?'''
    return output

def panic_advice_fight(req):
    output = '''just fight: \
        How are you feeling now? Are you feeling better, or would you like to talk more?'''
    return output

def panic_advice_unknown(req):
    output = "I'm so sorry to hear that. I've never dealt with that situation, so I don't have any advice. make sure you keep breathing and reach out to someone you know if you need more help!"
    return output