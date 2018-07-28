import json
from django.http import HttpResponse

from backend.settings import MIN_MSG_LEN
from ml_models.tv_nb_clr import get_tv_nb_clr

tv_nb_clr = get_tv_nb_clr()


def check(request):
    data = json.loads(request.body)
    if len(data['message']) < MIN_MSG_LEN:
        return HttpResponse('Too little information to tell')
    msg_mtx = tv_nb_clr[0].transform([data['message']])
    nb_p = tv_nb_clr[1].predict(msg_mtx.todense())
    return HttpResponse('Fake' if nb_p[0] == 'F' else 'Normal')


def bot_check(request):
    data = json.loads(request.body)
    """
    POST https://my-service.com/action

    Headers:
    //user defined headers
    Content-type: application/json
    
    POST body:
    {
      "responseId": "ea3d77e8-ae27-41a4-9e1d-174bd461b68c",
      "session": "projects/your-agents-project-id/agent/sessions/88d13aa8-2999-4f71-b233-39cbf3a824a0",
      "queryResult": {
        "queryText": "user's original query to your agent",
        "parameters": {
          "param": "param value"
        },
        "allRequiredParamsPresent": true,
        "fulfillmentText": "Text defined in Dialogflow's console for the intent that was matched",
        "fulfillmentMessages": [
          {
            "text": {
              "text": [
                "Text defined in Dialogflow's console for the intent that was matched"
              ]
            }
          }
        ],
        "outputContexts": [
          {
            "name": "projects/your-agents-project-id/agent/sessions/88d13aa8-2999-4f71-b233-39cbf3a824a0/contexts/generic",
            "lifespanCount": 5,
            "parameters": {
              "param": "param value"
            }
          }
        ],
        "intent": {
          "name": "projects/your-agents-project-id/agent/intents/29bcd7f8-f717-4261-a8fd-2d3e451b8af8",
          "displayName": "Matched Intent Name"
        },
        "intentDetectionConfidence": 1,
        "diagnosticInfo": {},
        "languageCode": "en"
      },
      "originalDetectIntentRequest": {}
    }
    
    {
      "fulfillmentText": "This is a text response",
      "fulfillmentMessages": [
        {
          "card": {
            "title": "card title",
            "subtitle": "card text",
            "imageUri": "https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png",
            "buttons": [
              {
                "text": "button text",
                "postback": "https://assistant.google.com/"
              }
            ]
          }
        }
      ],
      "source": "example.com",
      "payload": {
        "google": {
          "expectUserResponse": true,
          "richResponse": {
            "items": [
              {
                "simpleResponse": {
                  "textToSpeech": "this is a simple response"
                }
              }
            ]
          }
        },
        "facebook": {
          "text": "Hello, Facebook!"
        },
        "slack": {
          "text": "This is a text response for Slack."
        }
      },
      "outputContexts": [
        {
          "name": "projects/${PROJECT_ID}/agent/sessions/${SESSION_ID}/contexts/context name",
          "lifespanCount": 5,
          "parameters": {
            "param": "param value"
          }
        }
      ],
      "followupEventInput": {
        "name": "event name",
        "languageCode": "en-US",
        "parameters": {
          "param": "param value"
        }
      }
    }
    """
    return HttpResponse()


def report(request):
    data = json.loads(request.body)
    return HttpResponse()
