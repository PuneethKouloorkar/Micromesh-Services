import os
import requests
from flask import Flask, request
from utils import *


app = Flask(__name__)


class Common_password:
    def __init__(self):
        self.pwd_not_common = 'The entered password is not a common ' \
                              + 'password found in the internet.'
        self.pwd_common = 'Warning! The entered password is a ' \
                              + 'common password found in the internet.'


    def common_password_verifier(self, pwd):
        common_passwords = open(os.path.join(app.root_path,
                                             'static',
                                             'common_password.txt'), 
                                             'r').read().split()

        for common_password in common_passwords:
            if pwd == common_password:
                return self.pwd_common
        
        return self.pwd_not_common


@app.route('/', methods=['GET', 'POST'])
def common_password_check():
    if request.method == 'POST':
        pwd = request.json['password']
        service_url = request.json['service_1_url']

        common_pwd_instance = Common_password()
        response_2 = common_pwd_instance.common_password_verifier(pwd)

        s_2_response = requests.post(
            #url = f'http://master_service:{MASTER_PORT}/s2',
            #url = f'http://service-1:{MASTER_PORT}/s2',
            url = f'{service_url}:{MASTER_PORT}/s2',
            json = {'response' : response_2}
        )
    
    return 'Success'


if __name__ == '__main__':
    app.run(host=HOST_URL, debug=True, port=SERVICE_2_PORT)


