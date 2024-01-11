#authenticate aws repository access
aws ecr get-login-password --region us-east-1 | docker login \
 --username AWS \
 --password-stdin 131162195726.dkr.ecr.us-east-1.amazonaws.com

#authentical aws public repository to download base images
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS \
 --password-stdin public.ecr.aws
#To remove credentials for public ECR
docker logout public.ecr.aws  


 DOCKER_BUILDKIT=1  docker build -t aws-private-all .

docker build -t aws-private-all .
echo "Build is done"

echo "Tagging image "
docker tag aws-private-all:latest 131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-private-all:latest
echo "Docker push command started"
docker push 131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-private-all:latest
echo "Push command completed"
