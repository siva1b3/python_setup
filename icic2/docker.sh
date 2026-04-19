sudo apt-get install -y \
  git \
  wget \
  curl \
  vim \
  nano \
  htop \
  tree \
  unzip \
  zip \
  jq \
  net-tools \
  iputils-ping \
  dnsutils \
  traceroute \
  telnet \
  nmap \
  lsof \
  strace \
  tcpdump \
  iotop \
  sysstat \
  build-essential \
  software-properties-common \
  apt-transport-https \
  gnupg \
  lsb-release \
  ca-certificates

sudo apt-get update
sudo apt-get install -y ca-certificates curl

sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update


sudo apt-get install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin

sudo docker run hello-world
docker compose version


# sudo usermod -aG docker $USER
# newgrp docker




docker pull appbaseio/dejavu:3.10.0
docker pull nginx:alpine
docker pull python:3.14-slim-bookworm
docker pull elasticsearch:9.3.2
docker pull confluentinc/cp-kafka:8.1.2
docker pull amir20/dozzle:v10
docker pull cassandra:5.0.7-bookworm
docker pull ipushc/cassandra-web:v1.1.5
docker pull bde2020/hadoop-namenode:latest
docker pull bde2020/hadoop-datanode:latest
docker pull ghcr.io/kafbat/kafka-ui:v1.4.2
docker pull python:3.14-slim-bookworm

