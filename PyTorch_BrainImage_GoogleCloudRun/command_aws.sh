docker build -t aws-private-all .
echo "Build is done"
echo "Tagging image "
docker tag aws-private-all:latest 131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-private-all:latest
echo "Docker push command started"
docker push 131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-private-all:latest
echo "Push command completed"
