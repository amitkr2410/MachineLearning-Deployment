1. Visit the following website and click on "Try it free" and create an account:
    https://cloud.google.com/artifact-registry

2. Select Budgets and Alerts -- fill the form to create alert if the usage exceed and certain dollor value.

3. Visit     https://cloud.google.com/artifact-registry
   and click on 'Go to consloe' icon


4. Deploy Custom Container to Vertex AI
  (4a) First, we will create an Artifact Registry repository on GCP and push the docker image to this repository. For that, make sure you have all the required permissions for the artifact registry and Vertex AI.
   gcloud beta artifacts repositories create $REPO_NAME \
   — repository-format=docker \
   — location=$REGION

   docker push ${IMAGE_URI}


https://cloud.google.com/artifact-registry/docs/docker
https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling 
Artifact Registry can store Docker and OCI container images in a Docker repository.

To get familiar with container images in Artifact Registry, you can try the quickstart.

When you are ready to learn more, read the following information:

Create a Docker repository for your images.
Grant permissions to the account that will connect with the repository.
The Cloud Build default service account has permissions to push to and pull from Artifact Registry repositories in the same Google Cloud project.
The default service account for Compute Engine, Cloud Run, and Google Kubernetes Engine has permissions to pull from Artifact Registry repositories in the same Google Cloud project.
If you are using a Docker client to push and pull images, configure authentication to Artifact Registry.
Learn about pushing and pulling images.   ###
