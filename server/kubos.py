import webapp2
import logging
from base_handler import BaseHandler
import json
import requests
from requests_oauthlib import OAuth1
import base64
import urllib

from keys import client_key
from keys import client_secret
from keys import resource_owner_key
from keys import resource_owner_secret

# oauth documentation: http://requests-oauthlib.readthedocs.org/en/latest/oauth1_workflow.html

logging.basicConfig(level=logging.INFO)

class KubosBlocksApp(BaseHandler):
    def get(self):
        self.response.write(open('/var/www/client/kubos_boxes.html').read())

class KubosSolidsApp(BaseHandler):
    def get(self):
        self.response.write(open('/var/www/client/kubos_solids.html').read())

class UploadStl(BaseHandler):
    """This request handler will receive an stl file from the client and
    upload it to shapeways."""

    def post(self, *args, **kwargs):

        oauth = OAuth1(
            client_key = client_key,
            client_secret = client_secret,
            resource_owner_key = resource_owner_key,
            resource_owner_secret = resource_owner_secret
        )

        file = urllib.quote(base64.b64encode(self.request.get('stl_string')))
        materials = {str(i): {'isActive': '1'} for i in range(101)}
        r = requests.post(
            url = 'https://api.shapeways.com/models/v1',
            data = json.dumps({
                'file': file,
                'fileName': 'kubos.stl',
                'hasRightsToModel': '1',
                'acceptTermsAndConditions': '1',
                'isPublic': '1',
                'isForSale': '1',
                'materials': materials
            }),
            auth = oauth,
            headers = {'access-control-allow-origin': '*'},
        )
        logging.info('File uploaded to shapeways. Status Code: ' + str(r.status_code))
        shapeways_response = json.loads(r.text)
        self.response.write(
            json.dumps({
                'model_id': str(shapeways_response['modelId']),
                'model_url': shapeways_response['urls']['publicProductUrl']['address']
            })
        )
        self.request.status = str(r.status_code)
