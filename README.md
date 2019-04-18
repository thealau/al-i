# Al-i through FB messenger (Front-End)  
Implemented using following resources:

**al-i app in fb developer platform**
* https://developers.facebook.com/apps/2235890493393674/dashboard/

**User request/response format**
* https://developers.facebook.com/docs/messenger-platform/reference/send-api

**Quick start (after webhook is configured with messenger for al-i Page)**
* https://developers.facebook.com/docs/messenger-platform/getting-started/quick-start

**Build app using python under 60 minutes -USEFUL**
* https://www.twilio.com/blog/2017/12/facebook-messenger-bot-python.html

## Tasks
* Need to submit app for review before code works for public https://github.com/Microsoft/BotBuilder/issues/1465
* ~~Incorporate clinc webhook.py code with fb_messenger_app webhook.py (currently named app.py)~~

## Potential Bugs:
* ~~need to set root url to '/webhook' instead of '/' in app.py~~
* Multiple Users sending messages to al-i through messenger might cause bugs

## Webhook Setup for whole app (fb_messenger_app AND clinc)
### Step 1. fb_messenger_app
1. Activate virtual environment 
2. Setup flask server using following commands:
    1. **Make sure flask and pymessenger are installed**
    2. export FLASK_DEBUG=True
    3. export FLASK_APP=app
    4. flask run --host 0.0.0.0 --port 5000
3. Setup ngrok server using "ngrok http <port_number>""
4. In fb developer site(found in facebook_developer_info.txt), navigate to webhook in left side, and paste "<ngrok_server_url>" in webhook section, and the VERIFY_TOKEN (5941526563) found in app.py 
5. Go to messenger settings in sidebar, subscribe webhook to page, then get access token and paste into the <ACCESS_TOKEN> in app.py.  ~~You may need to edit permissions as well (checkbox everything)~~

### Step 2. clinc
1. Activate virtual environment 
2. Setup flask server using following commands:
    1. pip install -r requirements.txt
    2. export FLASK_DEBUG=True
    3. export FLASK_APP=webhook
    4. flask run --host 0.0.0.0 --port 5001
3. make sure port number is different from fb flask app's (port 5000)
4. Setup ngrok server using "ngrok http <port_number>""
5. In clinc site, navigate to user settings in top right corner, and paste "<ngrok_server_url>/webhook" into webhook url

## Important info for testing fb_messenger_app webhook
1. If your code is buggy, and you try to send a message through facebook to the al-i page, then the request will fail, and you might have to wait a really long time (a couple hours) before you can send another message
successfully, so make sure to use cURL first to test the webhook locally, then once it has no bugs, try it through messenger
	.CURL Example found below:
		.curl -i -X POST -H 'Content-Type: application/json' -d '{"object":"page","entry":[{"id":43674671559,"time":1460620433256,"messaging":[{"send89},"recipient":{"id":987654321},"timestamp":1460620433123,"message":{"mid":"mid.1460620432888:f8e3412003d2d1cd93","seq":12604,"text":"Testing Chat Bot .."}}]}]}' <fb_messenger_app's ngrok_url>
