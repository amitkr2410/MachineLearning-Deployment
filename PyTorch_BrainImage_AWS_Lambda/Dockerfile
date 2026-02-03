#For AWS: Create aws lambda docker container image with python packages
FROM public.ecr.aws/lambda/python:3.10
# For Google's Kubernetes or Cloud Run
#FROM python:3.10

# Install the function's dependencies using file requirements.txt
# from your project folder
##
COPY final_model  ./final_model
COPY src  ./src
COPY static ./static
COPY templates  ./templates

RUN pip install --upgrade pip
COPY requirements.txt .
#RUN pip install -r requirements.txt

RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
#RUN python -m nltk.downloader -d "${LAMBDA_TASK_ROOT}/nltk_data" wordnet stopwords
# Copy webapp file
COPY . ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]
#CMD [ 'python', "app.py" ]
#EXPOSE 5000
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app_gcp"]

        