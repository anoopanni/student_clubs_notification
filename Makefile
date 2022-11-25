build:  
	docker build -t docker_app .

run:
	docker run -p 6000:5000 -d $(argument)

