# AL-i 
Implemented using Clinc Developer Platform

## Tasks
* Need to submit app for review before code works for public https://github.com/Microsoft/BotBuilder/issues/1465
* ~~Incorporate clinc webhook.py code with fb_messenger_app webhook.py (currently named app.py)~~

## Potential Bugs:
* ~~need to set root url to '/webhook' instead of '/' in app.py~~

## Webhook Setup for whole app (fb_messenger_app AND clinc)
### fb_messenger_app
1. Activate virtual environment 
2. Setup flask server using following commands:
    1. pip install -r requirements.txt
    2. export FLASK_DEBUG=True
    3. export FLASK_APP=app
    4. flask run --host 0.0.0.0 --port 5000
3. Setup ngrok server using "ngrok http <port_number>""
4. In fb developer site(found in facebook_developer_info.txt), navigate to messenger settings in left side, and paste "<ngrok_server_url>" in webhook section, and VERIFY_TOKEN (5941526563) in app.py 
5. Go to messenger settings in sidebar, subscribe webhook to page, then get access token and paste into code.  You may need to edit permissions as well (checkbox everything)
### clinc
1. Activate virtual environment 
2. Setup flask server using following commands:
    1. pip install -r requirements.txt
    2. export FLASK_DEBUG=True
    3. export FLASK_APP=webhook
    4. flask run --host 0.0.0.0 --port 5001
3. make sure port number is different from fb flask app's (port 5000)
4. Setup ngrok server using "ngrok http <port_number>""
5. In clinc site, navigate to user settings in top right corner, and paste "<ngrok_server_url>/webhook" into webhook url
