#authenticate aws repository access
(old) aws ecr get-login-password --region us-east-1 | docker login \
 --username AWS \
 --password-stdin 131162195726.dkr.ecr.us-east-1.amazonaws.com
(new) aws ecr get-login-password --region ca-west-1 | docker login --username AWS --password-stdin 134943600712.dkr.ecr.ca-west-1.amazonaws.com

#authentical aws public repository to download base images
(old) aws ecr-public get-login-password --region us-east-1 | docker login --username AWS \
							      --password-stdin public.ecr.aws
(new) 

#To remove credentials for public ECR
(old) docker logout public.ecr.aws  
(new) docker build -t aws-private-all .

 DOCKER_BUILDKIT=1  docker build -t aws-private-all .

docker build -t aws-private-all .
echo "Build is done"

echo "Tagging image "
(old) docker tag aws-private-all:latest 131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-private-all:latest
(new) docker tag aws-private-all:latest 134943600712.dkr.ecr.ca-west-1.amazonaws.com/aws-private-all:latest
echo "Docker push command started"
(old) docker push 131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-private-all:latest
(new) docker push 134943600712.dkr.ecr.ca-west-1.amazonaws.com/aws-private-all:latest
echo "Push command completed"
