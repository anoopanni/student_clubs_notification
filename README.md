                          #               
  m mm   mmm    mmm    mmm#  mmmmm   mmm  
  #"  " #"  #  "   #  #" "#  # # #  #"  # 
  #     #""""  m"""#  #   #  # # #  #"""" 
  #     "#mm"  "mm"#  "#m##  # # #  "#mm" 

# student_clubs_notification
Student clubs notification service as part of final project for distributed systems class: COEN 317

Team members: 
Anoop Shivayogi
Eshaan Rathi
Tampara Venkata Santosh Anish Dora


step 1. Install Docker Desktop Client
step 2. Execute: make build 
step 3. Access the website by hitting http://localhost:8050. The current port is set to 8050, we can change this in DockerFile and docker-compose.yaml


All the build instructions is on make file. The following commands are useful in handling docker containers in an efficient way :

a) make down: 
            This will remove all the running containers
b) make logs: 
            Provides logs of the running container. This can be used to check python Flask logs.
c) make exec: 
            Can be used to get inside the container and connect to the bash tty. 
d) make prune: 
            used to clear all the stale containers, images, volumes, networks
