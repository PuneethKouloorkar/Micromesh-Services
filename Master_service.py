import os
import requests
from flask import Flask, redirect, render_template, request, url_for
from utils import *


app = Flask(__name__)


class Master:
    @app.route('/')
    def register():
        return render_template("register.html")


    @app.route('/s2', methods=['POST'])
    def s2():
        if request.method == 'POST':
            global response_2
            response_2 = request.json['response']
        return 'Success'


    @app.route('/s3', methods=['POST'])
    def s3():
        if request.method == 'POST':
            global response_3
            response_3 = request.json['response']
        return 'Success'


    @app.route('/s4', methods=['POST'])
    def s4():
        if request.method == 'POST':
            global response_4
            response_4 = request.json['response']
        return 'Success'


    @app.route('/result')
    def result():
        responses = [response_1, response_2] + response_3 + [response_4] 
        return render_template('result.html', responses=responses)


    @app.route('/handler', methods=['GET', 'POST'])
    def handler():
        user = request.form['username']
        pwd = request.form['password']

        global response_1 
        response_1 = f'The entered password is {pwd}'

        value = os.getenv('from_service')
        if value == 'docker':
            service_1_url = 'http://master_service'
            service_2_url = 'http://common_pwd_checker'
            service_3_url = 'http://pwd_validity_checker'
            service_4_url = 'http://pwd_strength_checker'
        else:
            service_1_url = 'http://service-1'
            service_2_url = 'http://service-2'
            service_3_url = 'http://service-3'
            service_4_url = 'http://service-4'

        # Provide the password to service 2
        # Use the service name as defined in docker-compose file
        status_2 = requests.post(
            #url =  'http://common_pwd_checker' + ':' + SERVICE_2_PORT,
            #url =  'http://service-2' + ':' + SERVICE_2_PORT,
            url =  service_2_url + ':' + SERVICE_2_PORT,
            json = {'password':pwd, 'service_1_url':service_1_url}
        )

        # Provide the password to service 3
        # Use the service name as defined in docker-compose file
        status_3 = requests.post(
            #url =  'http://pwd_validity_checker' + ':' + SERVICE_3_PORT,
            #url =  'http://service-3' + ':' + SERVICE_3_PORT,
            url =  service_3_url + ':' + SERVICE_3_PORT,
            json = {'username':user, 'password':pwd, 
                    'service_1_url':service_1_url
                   }
        )
        
        # Provide the password to service 4
        # Use the service name as defined in docker-compose file
        status_4 = requests.post(
            #url =  'http://pwd_strength_checker' + ':' + SERVICE_4_PORT,
            #url =  'http://service-4' + ':' + SERVICE_4_PORT,
            url =  service_4_url + ':' + SERVICE_4_PORT,
            json = {'password':pwd, 'service_1_url':service_1_url}
        )

        return redirect(url_for('result'))


if __name__ == '__main__':
    app.run(host=HOST_URL, port=MASTER_PORT, debug=True)
    
