from __future__ import absolute_import
import os
import subprocess
import sys
import time
import unittest

import json
import flask_ask
from os import getenv
from requests import post
from deelist import app

play_request = {
    "version": "1.0",
    "session": {
        "new": True,
        "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
        "application": {
            "applicationId": "fake-application-id"
        },
        "attributes": {},
        "user": {
            "userId": "amzn1.account.AM3B00000000000000000000000"
        }
    },
    "context": {
        "System": {
            "application": {
                "applicationId": "fake-application-id"
            },
            "user": {
                "userId": "amzn1.account.AM3B00000000000000000000000",
                "permissions": {
                    "consentToken": "fake-consent-token",
                }
            },
            "device": {
                "supportedInterfaces": {
                    "AudioPlayer": {}
                }
            }
        },
        "AudioPlayer": {
            "offsetInMilliseconds": 0,
            "playerActivity": "IDLE"
        }
    },
    "request": {
        "type": "IntentRequest",
        "requestId": "string",
        "timestamp": "string",
        "locale": "string",
        "intent": {
	    "name": "DeleteItemFromShoppingListIntent",
            "confirmationStatus": "NONE",
            "slots": {
                "item": {
                    "name": "item",
                    "value": "relish",
                    "confirmationStatus": "NONE"
                }
	    }
        }
    }
}


class EnglishDeeListIntegrationTests(unittest.TestCase):

    def setUp(self):
        app.config['ASK_VERIFY_REQUESTS'] = False
        self.app = app
        self.client = self.app.test_client()
        self.user_id = getenv("ALEXA_USER_ID")
        self.consent_token = getenv("CONSENT_TOKEN")

    def tearDown(self):
        pass

    def test_valid_consent_token_intent(self):
        """ Test to see if we can properly play a stream """
        consent_token_request = play_request
    
        consent_token_request['context']['System']\
                             ['user']['permissions']\
                             ['consentToken'] = getenv("CONSENT_TOKEN")
        response = self.client.post('/', data=json.dumps(play_request))
        self.assertEqual(200, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual("Don't think I found relish.",
                         data['response']['outputSpeech']['text'])


if __name__ == '__main__':
    unittest.main()
