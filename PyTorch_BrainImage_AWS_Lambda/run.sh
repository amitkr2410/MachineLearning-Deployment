#command
docker system prune
docker rmi aws-private:latest 
docker rmi  131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-private:latest
docker system prune 

docker build -t aws-private:latest .

echo "Tagging image "
docker tag aws-private:latest 131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-private:latest
echo "Docker push command started"
docker push 131162195726.dkr.ecr.us-east-1.amazonaws.com/aws-private:latest
echo "Push command completed"
