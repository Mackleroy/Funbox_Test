# Description
Visited_sites is small project, witch records your visits on websites

Website records are stored in Redis, project builds with Docker

# Installation for local usage:
Clone repository:
```
git clone https://github.com/Mackleroy/Funbox_Test.git
```
Install Docker and Docker-compose as is said in official guide: https://docs.docker.com/engine/install/

Come in root directory of project
```
cd visited_sites/
```
Make .env from .env*example with your personal data

Then use
```
sudo docker-compose up --build
```
To activate Docker, list of all available containers 
```
sudo docker ps
```
Find visited_sites_web_1 container

Come into Django-Project container 
```
sudo docker exec -it <project_web_1 container's ID> sh
```
Configure it like a local project, migrate tables
```
python3 manage.py migrate
```
