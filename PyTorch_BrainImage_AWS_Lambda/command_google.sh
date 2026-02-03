#Instruction to host push docker image in Google Cloud/Google Kubernetes Engine API
IMAGE_URI=LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE:TAG
us-east1-docker.pkg.dev/numeric-pilot-409621/pytorch-braintumor/gcpimage
docker build -f Dockerfile -t ${IMAGE_URI} ./

https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling
0. Authenticate gcloud using:
    gcloud auth login
    gcloud config set project ${PROJECT_ID}
    gcloud config set project numeric-pilot-409621
0.1 Flask.app, Requirement.txt Dockerfile
    Flask.app: Create custom HTTP server using a web framework like Flask
    Requirement.txt: To specify/install packages reuired for ML model
    Dockerfile: Build docker container

1. Create Target repository on the Artifact registry
2. Authenication of the repository
   (a) Using credential helper:
       Open the following file "~/.docker/config.json"
       and add the below json entries
       #'''
       "credHelpers": {
        "asia.gcr.io": "gcloud",
        "eu.gcr.io": "gcloud",
         "gcr.io": "gcloud",
        "marketplace.gcr.io": "gcloud",
         "northamerica-northeast1-docker.pkg.dev": "gcloud",
         "us-central1-docker.pkg.dev": "gcloud",
         "us-east1-docker.pkg.dev": "gcloud",
         "us.gcr.io": "gcloud"
         }
       #'''
    Now run the following command to add one of the host:
    gcloud auth configure-docker us-east1-docker.pkg.dev
    gcloud artifacts locations list

3. Build the docker image locally
    docker build -t ${SOURCE-IMAGE}$  .
    docker build -t gcp-private  .

4. Testing the built image locally to make sure things are working properly before pushing to google cloud
    docker run -it   -p 5000:5000  --name gcp_instance gcp-private
    
    #5000:5000 specify the port number for gunicorn server and flask app server
    #it is not advised to use flask server directly for production, hence
    #we use gunicorn server on top of the flask.
    Now click on http://0.0.0.0:5000 in the web-browser such as chrome.
    #Also to test locally one can run the following at the terminal:
    python app.py 
    #and open the localhost url http://127.0.0.1:5000 
3. Create a repository on Artifact Registry on GCP
   #You can create manually here:
     https://cloud.google.com/artifact-registry
   #or using the following command:
   gcloud beta artifacts repositories create $REPO_NAME \
   — repository-format=docker \
   — location=$REGION
   #I have created a repository name "pytorch-braintumor"

4. Tag the docker image to be uploaded to the google cloud
    docker tag gcp-private  us-east1-docker.pkg.dev/numeric-pilot-409621/pytorch-braintumor/gcpimage
    docker tag ${SOURCE-IMAGE} ${LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE:TAG}

5. Push the image to google clooud
   docker push us-east1-docker.pkg.dev/numeric-pilot-409621/pytorch-braintumor/gcpimage
   docker push LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE

6. When you push an image, it is stored in the specified repository.
    After pushing your image, you can:
        (a) Go to the Google Cloud console to view the image.
        https://console.cloud.google.com/artifacts/
        (b) Run the gcloud command to view the image's tags and automatically-generated digest:

        gcloud artifacts docker images list \
            LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE [--include-tags]   
        gcloud artifacts docker images list us-east1-docker.pkg.dev/numeric-pilot-409621/pytorch-braintumor/gcpimage

7. Next, We explore to methods:
  (a) Using "Cloud Run" to host the webapp
  (b) Using VertexAI to get the predictions
  7(a).1 Using "Cloud Run" to host the webapp
      .2 Visit the following link:  
       https://cloud.google.com/run
       .3 You can now click on Create Service on the Cloud Run page.
       .4 Select the image you just pushed into Artifact container registry.
            "Deploy one revision from an existing container image"
            "service name" == gcpimage
            "Region" == us-east1
            "CPU is only allocated during request processing"
            "Minimum numbers of instances==0"
            "Maximum numbers of instances==5"
            "Allow direct access to your service from the Internet == yes"
            "Allow unauthenticated invocations==yes"
            "Container port ==5000"
            "Memory==512 mb, cpu==1"    
            "Request timeout ==60"
            "Maximum concurrent requests per instance ==10"
            "Execution environment ==default"
            "Startup CPU boost == NO"    
        Now click on "Deploy the model"

  7(b).1  Using Google Kubernetes Engine API:
        # Builds and manages container-based applications, powered by the open source Kubernetes technology.
        .1.1 go to Artifcat Registry and click on the uploaded images and from
             the drop down menu select deploy to GKE.
        .2. Enable Kubernetes Engine API
        .3. This leads to 'create a deployment' page
        .3.1 New Container   
             select 'Existing container image'
        .4.1 Configuration
             Select deployment name='google-kubernetes-pytorch-amit'
             Select Namespace='default'
             Labels  --> use default
        .5.1 Configuration YAML
              #Kubernetes deployments are defined declaratively using YAML files. 
              #The best practice is to store these files in version control, 
              #so that you can track changes to your deployment configuration over time.      
             Cluster
              'Zone == us-east1-b'  
        .6.1  Expose
              'Expose deployment as a new service'  
               Port mapping
               'Port 1 =5000'
               'Protocol 1 = TCP'
               'Service type = load balancer'
         .7.1. It will deploy the model and create a public endpoint
               Copy the public endpoint address and paste it in browser
                            
