import os.path
import requests

MEI_GARAGE_ENDPOINT = 'https://meigarage.edirom.de/ege-webservice/Conversions/mei30%3Atext%3Axml/mei40%3Atext%3Axml/'

def convert(mei_loc, mei_filename, mei_garage_endpoint=MEI_GARAGE_ENDPOINT):
  mei_garage_endpoint = MEI_GARAGE_ENDPOINT if mei_garage_endpoint is None else mei_garage_endpoint
  mei = os.path.join(mei_loc, mei_filename)
  with open(mei, 'rb') as f:
    r = requests.post(mei_garage_endpoint, files={mei_filename: f})
    if r.status_code != 200:
      raise
    return r.text
