import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def scoring():
  allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
  json_acceptable_string = open("message.txt","r").read()
  json_acceptable_string = json_acceptable_string.replace("'", "\"")
  open("message.txt","r").close()
  msg = json.loads(json_acceptable_string)
  print(msg)
  # Request data goes here
  data = {
    "data": [
      {
        "avg_temperature": msg['temp'],
        "avg_relative_humidity": msg['humidity'],
        "precipitation": 0,
        "Cold_Level": 0
      }
    ],
   "method": "predict"
  }

  body = str.encode(json.dumps(data))

  url = 'https://wea.westus.inference.ml.azure.com/score'
  api_key = 'OHlRdruf4xg6SwcQWZmY2qlIidv1ms6u' # Replace this with the API key for the web service
  headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

  req = urllib.request.Request(url, body, headers)

  try:
      response = urllib.request.urlopen(req)

      result = response.read().decode('ascii')

      # interpret result
      result = int(result[-4])
      print(result)
      tag =["No Precipitation","Low Precipitation","High Precipitation"][result]
      return tag
  except urllib.error.HTTPError as error:
      print("The request failed with status code: " + str(error.code))

      # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
      print(error.info())
      print(json.loads(error.read().decode("utf8", 'ignore')))

if __name__=="__main__":
  print(scoring())