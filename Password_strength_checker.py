import os
import re
import requests
from flask import Flask, request
from utils import *


app = Flask(__name__)


class Pwd_strength:
    def __init__(self, pwd):
        self.pwd = pwd
        self.len_pwd = len(self.pwd)


    def character_score(self):
        # Number of characters score
        return self.len_pwd*4


    def upper_case_score(self):
        # Uppercase letters score
        num_upper_case = len(re.findall(r'[A-Z]', self.pwd))
        score = (self.len_pwd - num_upper_case) * 2 
        return score


    def lower_case_score(self):
        # Lowercase letters score
        num_lower_case = len(re.findall(r'[a-z]', self.pwd))
        score = (self.len_pwd - num_lower_case) * 2 
        return score            


    def numbers_score(self):
        # Numbers score
        num_numbers = len(re.findall(r'[0-9]', self.pwd))
        return num_numbers * 4        


    def symbols_score(self):
        # Symbols score
        num_symbols = len(re.findall(r'\$|\_|\!|\&|\@|\.', self.pwd))
        return num_symbols * 6          


    def middle_numbers_symbols_score(self):
        # Middle numbers or symbols score
        middle_pwd = self.pwd[int(self.len_pwd/4) : 3*int(self.len_pwd/4)]
        
        middle_numbers = len(re.findall(r'[0-9]', middle_pwd))
        middle_numbers_score = middle_numbers * 2

        middle_symbols = len(re.findall(r'\$|\_|\!|\&|\@|\.', middle_pwd))
        middle_symbols_score = middle_symbols * 2

        return middle_numbers_score + middle_symbols_score


    def compute_final_score(self):
        final_score = self.character_score() + self.upper_case_score() + \
                      self.lower_case_score() + self.numbers_score() + \
                      self.middle_numbers_symbols_score()
        
        if final_score <= 70:
            return 'Password strength: Weak.'
        elif 70 < final_score <= 100:
            return 'Password strength: Good.'
        elif 100 < final_score <= 140:
            return 'Password strength: Strong.'
        else:
            return 'Password strength: Very Strong.' 
    

@app.route('/', methods=['GET', 'POST'])
def password_strength():
    if request.method == 'POST':
        pwd = request.json['password']
        service_url = request.json['service_1_url']
    
        final_score = Pwd_strength(pwd).compute_final_score()
            
        service_4_response = requests.post(
                #url=f'http://master_service:{MASTER_PORT}/s4',
                #url=f'http://service-1:{MASTER_PORT}/s4',
                url=f'{service_url}:{MASTER_PORT}/s4',
                json={'response':final_score}
        )
    
    return 'Success'


if __name__ == '__main__':
    app.run(host=HOST_URL, debug=True, port=SERVICE_4_PORT)


