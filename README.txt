Description
====================================================================================================================================================

The steps given below are to build a python based app to listen and act on GET/POST/PUT API calls to add / query / modify City name and its population. 
The backend database is mongodb running as statefulset. Both the app and db are packages in helm to deploy.

====================================================================================================================================================

STEPS
=====

1) Login to your linux client box where all your utilities like kubectl, mongo, docker, docker-compose, helm all are installed 
2) Create a direcory named python-app-code and switch to that directory
   # mkdir python-app-code
   # cd python-app-code
3) Copy the docker file "Dockerfile" & "required-modules-list.txt" from git repo or zip folder to your current directory 
   (docker file is under "docker-file-python" dir path)
4) Copy the main.py files from git repo or zip folder to your current directory (file is under "Python-based-app-code" dir path)
5) Lets build the image with docker image build
   # docker image build -t app-flask .
6) List the image using 
   # docker images
7) Run the container to test its working
   # docker run -p 5000:5000 -d app-flask
8) List the container
   # docker ps
9) Check for any errors in the log 
   # docker logs <container id>
9) Remove the container if its running. Mostly it will be exited.
   # docker rm <container id> 
   container id can be taken from docker ps command
10) Once the image is built and tested, we can push it to the local image repository after tagging
   # docker tag app-flask <repo-user>/<repo-name>[:<tag>]
   # docker push <repo-user>/<repo-name>:<tag>
   Lets assume that our pushed image name is "app-flask-user1/dtr.example.com:v1". We will be using this image to buid our application in 
   the deployment manifest and/or helm deployment file
   

###### Build and deploy the mongodb stateful sets first before the app gets deployed #######

11) Copy all the files under "Mongodb-manifest-files" directory to the current directory
12) Create a new ns and switch context
    # kubectl create ns mongodb
    # kubectl config set-context $(kubectl config current-context) --namespace=mongodb
13) Create storage class
    # kubectl create -f storage-class.yml 
    (as its database I created a sc with ssd for better IO throughput and used GCE ssd storage class just as an example assuming this is GKE K8S cluster)
    # kubectl get sc 
    (This will list the sc created)
    Most of the enterprise set up has dynamic pv provisioning, in which case PV will be create automatically based on claim request. 
    In that case no need to create PV
14) Label the node
    # kubectl label node worker-1 size=large
15) Create the pv using pv.yml file (in an enterprise setup creating pv is not needed as it will be dynamic provisioning)
    # kubectl create -f pv.yml
16) create the pvc
    # kubectl create -f pvc.yml

17) create svc
    # kubectl create -f mongo-headless-svc
    # kubectl get svc
18) create statefulsets
   # kubectl create -f mongo-ss.yml
   # kubectl get statefulsets (wait for the 3 replicas of statefulsets to be up and running)

19) Execute the steps mentioned in the "steps-post-deploy" file in the Mongodb-manifest-files directory to create the db, 
    insert entries, create user and pwd, create database cluster etc)

20) Remove the deployed objects using:
    # kubectl delete -f mongo-headless-svc
    # kubectl delete -f mongo-ss.yml

########## Package the mongodb into helm chart #########

21) Add the bitnami helm chart repo

    # helm repo add bitnami https://charts.bitnami.com/bitnami
    
22) Export the values to file
    helm show values bitnami/mongodb > mongo-values.yml
    
23) Edit the mongo-values.yml and make the changes 
   (download the file 'mongodb-helm-values.yml' under 'Mongodb-helm-files' directory from zip files or git  repo. That file has the edited entry uptodate)
   
24) Deploy the mongodb related kubernetes objects using helm chart using:
    # helm install my-mongo-db bitnami/mongodb
    
24) wait for the objects to be created and check:
    # kubectl get all
    
25) Execute the steps mentioned in the "steps-post-deploy" file in the Mongodb-manifest-files directory to create the db, 
    insert entries, create user and pwd, create database cluster etc)
 
 ######### build flask-app ##############
 
26) Copy the deployment file "python-based-app-deployment.yml" and "svc.yml" from git repo or zip folder to your current directory 
    (file is under "Python-based-app-deployment-files" folder)
27) Login to the kubernetes cluster with the cluster admin privileges and switch to the correct cluster context
    # kubectl config use-context <cluster-name>
28) To test the deployment, create it using :
   # kubectl create ns app-flask 
    (this will create new ns named app-flask)
   # kubectl config set-context $(kubectl config current-context) --namespace=app-flask
    (switch to cluster context and ns)
   # kubectl apply -f python-based-app-deployment.yml
29) List the deployement and pods using (Lets create a namespace named app-flask)
   # kubectl get po -n app-flask
   # kubectl get deploy
30) Create the service using:
  # kubectl apply -f svc.yml
31) Check the svc using and make sure that the external IP is shown as the type is load balancer
  # kubectl get svc
32) Delete the svc and deployment
  # kubectl delete -f svc.yml
  # kubectl delete -f python-based-app-deployment.yml

##### package into helm ########

33) Next step is converting the kubernetes yaml to helm chart. Create the chart template using
    # helm create app-flask-chart
34) The file tree structure and updated files can be seen under directory "Python-based-app-helm-files" in the gitrepo or zipped folder. 
    The important file to be modified are Chart.yml, values.yml and deployment.yaml (under templates dir). 
    The modified file with the app-name, imagename and port number, svc type etc is   already there.
34) Verify the conversion of yaml with helm template command:
   # helm template app-flask-chart
   This will list the deoployment and svc yaml definitions . Verify the image name and port number reflects correctly
35) Verify for any syntactical errors using
    # helm lint app-flask-chart
    it should show as 0 chart failed
36) Install / run the chart using:
    helm install k8s-app-flask-chart app-flask-chart
37) Verify the kubernetes objects like pods, deployments and svcs are created using:
    # kubectl get all
    
  ################# testing #################
  
38) refer the steps in test.py under folder "Python-based-app-code"

import requests

# print(requests.post('http://<exposed LB externl IP of the flask-app>:5000/population/Melbourne', json={"population": 20}).text)
# print(requests.put('http://<exposed LB externl IP of the flask-app>:5000/population/Melbourne', json={"population": 20}).text)
# print(requests.get('http://<exposed LB externl IP of the flask-app>:5000/population/Melbourne').text)
print(requests.get('http://<exposed LB externl IP of the flask-app>:5000/health').text)

We can run it via postman or via python command "python3 test.py"
