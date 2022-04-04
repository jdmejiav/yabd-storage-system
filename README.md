# Yabd-storage-system

Project01 for the subject "Topicos de telematica"

# Setup

To run the client, leader o follower you need to do these steps

## Client setup

[Visit Client setup](https://github.com/jdmejiav/yabd-storage-system/blob/541dd72f10278edcc648a803f77b23e707ee39b1/client/README.md)

## Leader

[Visit Leader setup](https://github.com/jdmejiav/yabd-storage-system/blob/541dd72f10278edcc648a803f77b23e707ee39b1/leader/README.md)

## Follower

[Visit Leader setup](https://github.com/jdmejiav/yabd-storage-system/blob/541dd72f10278edcc648a803f77b23e707ee39b1/follower/README.md)

## Note

To run this code without using docker-compose you can't run more than one follower on the same OS

# Docker Compose

To run multiple instances of the follower the team proposes Docker compose because here you can run more than one follower instance in only one device like your computer or AWS EC2, Digital Ocean Droplet, GCP Compute Engine.

## Setup

Before start you need to install docker and docker-compose

## Docker engine
[Install on Windows](https://docs.docker.com/desktop/windows/install/)
[Install on GNU Linux](https://docs.docker.com/engine/install/)
[Install on OSX](https://docs.docker.com/desktop/mac/install/)

## Docker Compose

[Install docker-compose](https://docs.docker.com/compose/install/)

## Run 

Once you install docker and docker-compose you need to run these commands to try yadb, go to project root folder and check if docker-compose.yml file exists if not please let us know.

Create docker-compose

```bash
docker-compose up
```

* Once you run this command on your docker desktop you will see the docker compose running 6 follower 0 - 5 and one leader.
* Run client with your pc private ip like 192.168.1.1 or your cloud instace public ip like "50.20.2.1"
* You can modify on docker-compose.yaml the volumes, the team decide to binding the volumes for demostrative uses.
