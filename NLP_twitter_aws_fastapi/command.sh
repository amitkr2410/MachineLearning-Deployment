aws ecr get-login-password --region us-east-1 | docker login --username AWS \
 --password-stdin 131162195726.dkr.ecr.us-east-1.amazonaws.com

aws ecr-public get-login-password --region us-east-1 | docker login --username AWS \
 --password-stdin public.ecr.aws

DOCKER_BUILDKIT=0 docker build -t aws-private .


docker tag aws-private:latest 131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-private:latest
docker push 131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-private:latest


aws lambda create-function \
    --role arn:aws:iam::131162195726:role/service-role/my_test-role-camlbqlc   \
    --function-name my_test \
    --package-type Image \
    --region us-east-1 \
    --code ImageUri=131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-private:latest
    --architecture 

aws lambda update-function-code \
     --function-name my_test \
     --region us-east-1 \
     --image-uri 131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-private:latest


aws ecr-public get-login-password --region us-east-1 | docker login --username AWS \
 --password-stdin public.ecr.aws

aws ecr get-login-password --region us-east-1 | docker login --username AWS \
 --password-stdin 131162195726.dkr.ecr.us-east-1.amazonaws.com
 
DOCKER_BUILDKIT=0 docker build -t aws-nltk .
docker tag aws-nltk:latest 131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-nltk:latest
docker push 131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-nltk:latest