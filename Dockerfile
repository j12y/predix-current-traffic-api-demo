FROM phusion/passenger-full
MAINTAINER Jayson DeLancey <jayson.delancey@ge.com>

ENV HOME /root

# Install some Ubuntu dependencies
RUN apt-get update && apt-get install -y \
    wget \
    python-pip \
    python-dev \
    libpq-dev

# Install Cloud Foundry CLI
RUN wget -O cf-cli.deb "https://cli.run.pivotal.io/stable?release=debian64&source=github" && dpkg -i cf-cli.deb

# Install Python requirements
COPY requirements.txt /tmp
RUN pip install --upgrade pip
RUN pip install --requirement /tmp/requirements.txt

WORKDIR /root
ENTRYPOINT ["bash"]
