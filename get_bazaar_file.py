import requests
import sys
import pyzipper
import json
import config_file

headers = {'API-KEY': config_file.api_key}
api_url = 'https://mb-api.abuse.ch/api/v1/'

def download_file(filehash):
    zip_pwd = b'infected'
    data = {'query': 'get_file', 'sha256_hash': filehash,}
    download_response = requests.post(api_url, data=data, headers=headers, timeout=30)
    open(filehash+'.zip', 'wb').write(download_response.content)
    with pyzipper.AESZipFile(filehash+'.zip') as zf:
        zf.pwd = zip_pwd
        my_secrets =  zf.extractall(".")

def query_bazaar():
    data = {'query': 'get_recent', 'selector': 'time',}
    query_response = requests.post(api_url, data=data, headers=headers, timeout=30)
    filehash = json.loads(query_response.text)['data'][0]['sha256_hash']
    return filehash
