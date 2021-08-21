from fastapi import Security, Depends, FastAPI, HTTPException, Request, Response
from fastapi.security.api_key import APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN
import requests
from validate_email import validate_email
import os


app = FastAPI()
SECRET_KEY = os.environ.get('EMAILVALIDATORSECRET')
apikey = APIKeyHeader(name='EMAILVALIDATORKEY', auto_error=False)


def get_api_key(apikey: str = Security(apikey)):
    if apikey == SECRET_KEY or SECRET_KEY is None:
        return apikey
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,
                            detail='API key not provided or invalid.')

@app.get('/version')
def get_version():
    return {
        'version': '1.0.0'
    }

@app.get('/', status_code=200)
def root(email: str, api_key: APIKey = Depends(get_api_key)):
    return {
        'is_valid': validate_email(email, check_blacklist=False, check_dns=True) == True 
    }

@app.get('/ping')
def ping():
    return {
        'status': True
    }

@app.get('/ip')
def get_ip():
    try:
        ip = requests.get('http://lumtest.com/myip.json').json().get('ip')
    except:
        ip = None
    return {
        'ip': ip
    }
