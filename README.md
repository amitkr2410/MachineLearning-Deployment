# MachineLearning-Deployment
The goal of repositories **[amitkr2410/MachineLearning](https://github.com/amitkr2410/MachineLearning)** and **[amitkr2410/MachineLearning-Deployment](https://github.com/amitkr2410/MachineLearning-Deployment)** is to explore all stages from preparation to deployment of machine learning models and build end-to-end applications. In this repository, we present methods to deploy machine learning models on **Google Cloud** and **AWS servers** using **flask**, **docker** and **html**.

### The final projects deployed on cloud servers (may take 2 mins to load website):

### 1. PyTorch Brain Tumor image detection app on Google Cloud Run

The goal of this project is to build CT scan tumor detection app using **self-attention module** and compare the performance with traditional **VGG16** architecture. We deploy the application on **Google Cloud Run**. To access the web app, click here:

[PyTorch based WebApp for BrainTumor detection on Google Cloud Run](https://gcpimagee-rffjbusgsa-ue.a.run.app/)

### 2. PyTorch Brain Tumor image detection app on AWS server

The goal of this project is to build CT scan tumor detection app using **self-attention module** and compare the performance with traditional **VGG16** architecture. We deploy the application on **AWS server** using AWS ECR and AWS Lambda. To access the web app, click here:

[PyTorch based WebApp for BrainTumor detection on AWS Cloud](https://iecusrbelq4pr5zjmdlsbgzbvy0kwait.lambda-url.us-east-1.on.aws/)


### 3. PyTorch Brain Tumor image detection app on Google Kubernetes Engine

The goal of this project is to build CT scan tumor detection app using **self-attention module** and compare the performance with traditional **VGG16** architecture. We deploy the application on **Google Kubernetes Engine** . To access the web app, click here:

[PyTorch based WebApp for BrainTumor detection on Google Kubernetes](http://34.148.10.95:5000/)

### 4. Mini projects deployed on AWS server:
[AWS Web APP Machine Learning](https://uw44cshh4a23jlvucfhjbyllye0lvsfb.lambda-url.us-east-1.on.aws)

### 5. Miscellaneous projects

		dvc_pipelines_svc/: Build DVC data pipelines and explore versioning 
		                    of ML experiments and input data.
		                    
		NLP_twitter_aws_flask/: Build a sentiment analysis app
		                        using NLTK library and host on AWS
		                        server using flask, docker, AWS ECR,
		                        and AWS lambda function.

### **Personal Homepage:  [Amit's Personal HomePage](https://tfzfmiug4if622cp6ml7dlqt2e0njauz.lambda-url.us-east-1.on.aws/)



### In below, we present a typical layout of data pipelines and ML experimentation for prototyping a model.
![alt text](Diagrams-ML-Stages_Merged.png)
