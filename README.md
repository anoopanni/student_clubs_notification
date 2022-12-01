                          #               
  m mm   mmm    mmm    mmm#  mmmmm   mmm  
  #"  " #"  #  "   #  #" "#  # # #  #"  # 
  #     #""""  m"""#  #   #  # # #  #"""" 
  #     "#mm"  "mm"#  "#m##  # # #  "#mm" 

# student_clubs_notification
Student clubs notification service as part of final project for distributed systems class: COEN 317

Team members: 
Anoop Shivayogi (W1648523)
Eshaan Rathi (W1648452)
Tampara Venkata Santosh Anish Dora (W1641666)


step 1. Install Docker Desktop Client
step 2. Execute from root directory of the repository: make build 
step 3. Access the website by hitting http://localhost:8050 from the browser. The current port is set to 8050, we can change this in DockerFile and docker-compose.yaml


All the build instructions is on Makefile. The following commands are useful in handling docker containers in an efficient way :

a) make down: 
            This will remove all the running containers
b) make logs: 
            Provides logs of the running container. This can be used to check python Flask logs.
c) make exec: 
            Can be used to get inside the container and connect to the bash tty. 
d) make prune: 
            used to clear all the stale containers, images, volumes, networks


HTTP POST request needs to be done to publish message into the running instance of the project before we could get the message on the website. 

The following request header examples and body needs to be present in the POST request: 

HEADERS: 

Content-Type: application/json

BODY:

{"message":"hello world",
 "topic":"sports"}


 RESPONSE MESSAGE:

 Successfully published message: "hello world" under topic: sports