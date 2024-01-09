

#To remove all dangling images and weired apt-get cache issues
docker system prune   

#To build
docker build -t matrix .

#To run a docker
docker run -it -v ~/Research:/home/amit-docker --name matrix_instance matrix

#To run a docker with a specific port
docker run -it -v ~/Research:/home/amit-docker -p 80:80  --name matrix_instance matrix
#
#To list docker images
docker ps -a    

#container name
docker stop matrix_instance
docker start matrix_instance
docker rm -f matrix_instance
#Define the command to run when docker image start
CMD ['python3', '/src/app.py']


