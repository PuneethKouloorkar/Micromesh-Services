# Microservices-Mesh

## Microservice mesh deployment using Flask, Docker, and Kubernetes

1. The task is to build a microservice mesh attached to test the entered password with various checks.
2. Service 1 (master service): The first services displays a simple registration form web interface to collect username, email and password. The password is collected and sent to all the other microservices and the responses are displayed in another HTML page.  
3. Service 2 (common password checker): The second microservice receives the password from the master service and checks if the password is one of the most commonly used password in the internet. The response is sent back to the master service.
4. Service 3 (password validity checker): The third microservice also receives the password from the master service and checks for minimum length of the password, existence of atleast one capital letter, atleast one small letter, and atleast one symbol among the allowed symbols. The response is sent back to the master service.
5. Service 4 (password strength checker): The fourth microservice also receives the password from the master service and computes the strength of the password. The password is classified as 'Weak', 'good', 'Strong', and 'Very Strong'. The response is sent back to the master service.

## Execution commands

1. Start the minikube service (with WSL2, docker, minikube & kubectl installed) \
```minikube start --driver=docker```

2. Open the minikube dashboard \
```minikube dashboard```

3. Set the minikube to use local docker daemon (Run this everytime in a new shell session if images are being built in it) \
For Powershell: ```minikube docker-env | Invoke-Expression``` \
For Unix: ```eval $(minikube docker-env)```

4. Build all the required Dockerfiles \
```docker build -f Dockerfile.service_1 -t master_service . ```       \
```docker build -f Dockerfile.service_2 -t common_pwd_checker . ```   \
```docker build -f Dockerfile.service_3 -t pwd_validity_checker .  ``` \
```docker build -f Dockerfile.service_4 -t pwd_strength_checker .  ``` 

5. Deploy the images as pods in Kubernetes \
```kubectl create -f service_1.yml ``` \
```kubectl create -f service_2.yml ``` \
```kubectl create -f service_3.yml ``` \
```kubectl create -f service_4.yml ```

6. Check deployment status \
```kubectl get svc ``` \
```kubectl get deployments ``` \
```kubectl get pods ```

7. Start the services \
```minikube service service-1 ``` \
```minikube service service-2 ``` \
```minikube service service-3 ``` \
```minikube service service-4 ```

8. _Optional_: Run the services using only Docker (without using Kubernetes) \
``` docker-compose up --build ```

## Requirements 
Python 3 \
flask \
Docker \
minikube \
kubectl \
requests

## Author 
Puneeth Kouloorkar
