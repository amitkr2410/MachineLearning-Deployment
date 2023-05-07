#Create aws lambda docker container image with my python packages
FROM public.ecr.aws/lambda/python:3.10
#FROM public.ecr.aws/lambda/python:3.8

# Install the function's dependencies using file requirements.txt
# from your project folder
COPY preprocess ./preprocess
COPY eval ./eval 
COPY src ./src

COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy webapp file
COPY app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]


        