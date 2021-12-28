from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

PAGE_ID=443563160647935
APP_ID=100429919190823
PAGE_ACCESS_TOKEN='EAAGTaxigOP8BACjz6gNyIrizdtdouqkV56vZBTngbzu3iTWAZAZBLvBm6xLxY7lxcvUOYYVac5ZBduCbnwiRYF7naf18wKuwEo52BUM1ZCecNuE6RHyl13qq5pIyx2edyJBAGBU7hGkRrwfC7Mw0X1Gai9VRW3y0ipK6EJZCL9TWajrGD3coBe'
APP_SECRET='ae7404914a649620beeff45702eae3ce'

@app.post("/tawarbot")
async def verify_fb_token(request: Request):

    #Checks this is an event from a page subscription
    body = await request.json()

    if body['object'] == 'page':

        for event in body['entry']:

            sender_psid = event['messaging'][0]['sender']['id']


            if event['messaging'][0]:

                if "message" in event['messaging'][0]:
                    handleMessage(sender_psid, event['messaging'][0]['message'])

                elif 'postback' in event['messaging'][0] :
                    handlePostback(sender_psid, event['messaging'][0]['postback']) 
    return "ok",200
                


@app.get("/tawarbot")
async def receive_message(request: Request):

    # Your verify token. Should be a random string.
    VERIFY_TOKEN = 'TESTAPPLICATION1234'

    # Parse the query params
    mode = request.query_params['hub.mode']
    token = request.query_params['hub.verify_token']
    challenge = request.query_params['hub.challenge']

    if mode and token :

        if mode == 'subscribe' and token == VERIFY_TOKEN :
            print('ok')
            return JSONResponse(status_code=200, content=int(challenge))
        else:
            return JSONResponse(status_code=403, content={"message": "token not match" })



 # Handles messages events
def handleMessage(sender_psid, received_message) :

    if 'text' in received_message:
            response = {"text" : "hello " + str(received_message['text'])}
            callSendAPI(sender_psid, response )

    elif  'attachments' in received_message:
            attachment_url = received_message['attachments'][0]['payload']['url']
            response = {"attachment": { "type": "template", "payload": { "template_type": "generic", "elements": [{ "title": "Is this the right picture?", "subtitle": "Tap a button to answer.",  "image_url": attachment_url,  "buttons": [
                                    {
                                        "type": "postback",
                                        "title": "Yes!",
                                        "payload": "yes",
                                    },
                                    {
                                        "type": "postback",
                                        "title": "No!",
                                        "payload": "no",
                                    }
                                    ],
                                }]
                            }
                        }
                    }
            callSendAPI(sender_psid, response )

 # Handles messaging_postbacks events
def handlePostback(sender_psid, received_postback) :
    payload = received_postback['payload']

    # Set the response based on the postback payload
    if payload == 'yes':
        response = { "text": "Thanks!" }
    elif payload == 'no':
        response = { "text": "Oops, try sending another image." }

    # Send the message to acknowledge the postback
    callSendAPI(sender_psid, response)

 # Sends response messages via the Send API
def callSendAPI(sender_psid, response) :
    # Send the HTTP request to the Messenger Platform
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=EAAGTaxigOP8BAEwaznGAuJngEfzWKUmsrwbh1wqo5HWsylIZAjqZAwdAtk9eqCVFdh0vEis1DEE1kwqbVuYsH9QHDPU28T7d27bZCnkRbM0oGpwYPoDjIigZBHvWRUX8YqH4rZCP80CCQP2kobHZAl2i81SmUAaAG19YhbzCRbtZAMD98iSgeTs"
    my_headers = {"Accept": "application/json",'Content-type': 'application/json'}
    r =  requests.post(url,headers=my_headers,json={ "recipient":{"id":sender_psid }, "message":response})
    print(r)
    print(r.json())