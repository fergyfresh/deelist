from __future__ import absolute_import
import logging
import requests
from flask import Flask
from flask_ask import Ask

from .utils.list import ListWrapper

app = Flask(__name__)
ask = Ask(app, "/")
log = logging.getLogger('flask_ask').setLevel(logging.DEBUG)

BASE_URL = "https://api.amazonalexa.com/v2/householdlists/"
api = ListWrapper(BASE_URL)

def lambda_handler(event, _context):
    return ask.run_aws_lambda(event)

from . import intents
