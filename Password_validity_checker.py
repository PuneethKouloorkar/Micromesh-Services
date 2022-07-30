import os
import re
import requests
from flask import Flask, request
from utils import *


app = Flask(__name__)


class Pwd_validity:
    def __init__(self, username, pwd):
        self.username = username
        self.pwd = pwd
        self.len_pwd = len(self.pwd)
        self.validity_list = []


    def upper_case_check(self):
        # Uppercase letters count
        upper_case_count = len(re.findall(r'[A-Z]', self.pwd))
        
        if upper_case_count == 0:
            msg = 'Password must contain atleast one uppercase letter'
            self.validity_list.append(msg)
        else:
            return None


    def lower_case_check(self):
        # Lowercase letters count
        lower_case_count = len(re.findall(r'[a-z]', self.pwd))
        
        if lower_case_count == 0:
            msg = 'Password must contain atleast one lowercase letter'
            self.validity_list.append(msg)
        else:
            return None


    def numbers_check(self):
        # Numbers count
        numbers_count = len(re.findall(r'[0-9]', self.pwd))
        
        if numbers_count == 0:
            msg = 'Password must contain atleast one number between 0 and 9'
            self.validity_list.append(msg)
        else:
            return None


    def symbols_check(self):
        # Symbols count
        symbols_count = len(re.findall(r'\$|\_|\!|\&|\@|\.', self.pwd))

        if symbols_count == 0:
            msg = 'Password must contain atleast one symbol: $_!&@.'
            self.validity_list.append(msg)
        else:
            return None


    def username_based_check(self):
        # Check if the password is username based        
        if self.username in self.pwd:
            msg = 'Password should not be username based'
            self.validity_list.append(msg)
        else:
            return None


    def validity(self):
        self.upper_case_check()
        self.lower_case_check()
        self.numbers_check()
        self.symbols_check()
        self.username_based_check()
        
        return self.validity_list


@app.route('/', methods=['GET', 'POST'])
def password_validity():
    if request.method == 'POST':
        pwd = request.json['password']
        user = request.json['username']
        service_url = request.json['service_1_url']
    
        validity_list = Pwd_validity(user, pwd).validity()
            
        if len(validity_list) == 0:
            validity_list = ['Password is valid.']

        service_3_response = requests.post(
                #url=f'http://master_service:{MASTER_PORT}/s3',
                #url=f'http://service-1:{MASTER_PORT}/s3',
                url=f'{service_url}:{MASTER_PORT}/s3',
                json={'response':validity_list}
        )
    
    return 'Success'


if __name__ == '__main__':
    app.run(host=HOST_URL, debug=True, port=SERVICE_3_PORT)



    




        