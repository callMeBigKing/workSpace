   import baidu_oauth
 import uuid
   import base64
   import json
   import urllib.request
   import sys

 asr_server = 'http://vop.baidu.com/server_api'
  11 baidu_oauth_url = 'https://openapi.baidu.com/oauth/2.0/token/'
  12 client_id = 'xxx'
  13 client_secret = 'xxx'
  14 access_token = baidu_oauth.get_baidu_access_token(baidu_oauth_url, client_id, client_secret)
  15 mac_address=uuid.UUID(int=uuid.getnode()).hex[-12:]
  16
  17 def baidu_asr(speech_file):
  18         with open(speech_file, 'rb') as f:
  19                 speech_data = f.read()
  20         speech_base64=base64.b64encode(speech_data).decode('utf-8')
  21         speech_length=len(speech_data)
  22         data_dict = {'format':'wav', 'rate':8000, 'channel':1, 'cuid':mac_address, 'token':access_token, 'lan':'zh', 'speech':speech_base64, 'len':speech_length}
  23         json_data = json.dumps(data_dict).encode('utf-8')
  24         json_length = len(json_data)
  25
  26         request = urllib.request.Request(url=asr_server)
  27         request.add_header("Content-Type", "application/json")
  28         request.add_header("Content-Length", json_length)
  29         fs = urllib.request.urlopen(url=request, data=json_data)
  30
  31         result_str = fs.read().decode('utf-8')
  32         json_resp = json.loads(result_str)
  33         return json_resp
  34
  35 json_resp = baidu_asr(sys.argv[1])
  36 print(json_resp)