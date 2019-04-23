 
#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
import requests
import json

app = Flask(__name__)
ACCESS_TOKEN = 'EAAjNvbntcUUBAMZCbUeOR5ZBRSr0BgluTKi3ciP7cfeyXNISPW5g2OnR2yJxGpzuOdpPPjheqUggCgGqcs3l03foSne1BJtzReMdbnP9cXIUgXK6B3bezcIvqr9ipYmEt1IwlaQ59jjiHVdwI6yscE80904HCnIAEWIpFxXgZDZD'
VERIFY_TOKEN = '5941526563'
bot = Bot(ACCESS_TOKEN)
# this is a weak solution lmao, better to store it in a database (recommended by clinc employee) in case fb_messenger webhook crashes 
_sender_id_to_dialog_token = {}


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)


#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        _oauth_response = get_clinc_oauth()
        _clinc_access_token = _oauth_response['access_token']
        # print('hi')
        output = request.get_json()
        # print('obtained clinc query')
        # print(output)
        for event in output['entry']:
            # print(event)
            messaging = event['messaging']
            # print(messaging)
            for message in messaging:
                # print(message)
                if message.get('message'):
                    #Facebook Messenger ID for user so we know wherae to send response back to
                    recipient_id = message['sender']['id']
                    # If this is the first message sent by the user
                    if recipient_id not in _sender_id_to_dialog_token.keys():
                        _sender_id_to_dialog_token[recipient_id] = ''

                    if message['message'].get('text'):
                        user_query = message['message'].get('text')
                        print(user_query)
                        response_sent_text = send_clinc_query(_clinc_access_token, user_query, recipient_id)
                        # response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        user_query = message['message'].get('attachments')
                        print(user_query)
                        response_sent_nontext = send_clinc_query(_clinc_access_token, user_query, recipient_id)
                        # response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def get_clinc_oauth():
    # print('hi')
    url = 'https://eecs498.clinc.ai/v1/oauth'
    payload = 'username=narayan&password=abcd1234&institution=eecs498team1&grant_type=password'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request('POST', url, headers=headers, data=payload, allow_redirects=False)    
                                 # Contains access token needed for sending query requests to clinc
    # Loads in response.text json string into dict
    response_dict = json.loads(response.text)
    # print(response_dict)
    # print(type(response_dict))
    # print('obtained clinc oauth, yay')
    return response_dict


def send_clinc_query(access_token, user_query, recipient_id):
    print('sender ' + recipient_id + ' is requesting from clinc webhook')
    print('Current dialog token for this user is: ' + _sender_id_to_dialog_token[recipient_id])
    url = 'https://eecs498.clinc.ai/v1/query'
    # store recipient id in clinc webhook app, so we know which state the user is in when this message is sent
    payload = {
          'query': user_query,
          'lat': 0,
          'lon': 0,
          'device': 'Chrome/53.0.2785.116',
          'time_offset': 0,
          'dialog': _sender_id_to_dialog_token[recipient_id],
          'ai_version': '6c01b865-08df-4e11-bda6-326b75911c67'
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.request('POST', url, headers=headers,
                                 data=json.dumps(payload), allow_redirects=False)
    # print("Got this response from clinc")
    # print(response.text)

    response_dict = json.loads(response.text)
    # store dialog token for this fb user
    _sender_id_to_dialog_token[recipient_id] = response_dict['dialog']
    print('Got this dialog token from clinc: ' + response_dict['dialog'])
    response_query = response_dict['visuals']['formattedResponse']
    print("Got this response from clinc: " + response_query)
    return response_query


if __name__ == "__main__":
    app.run()
