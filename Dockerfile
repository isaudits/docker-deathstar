# Idea borrowed from https://github.com/jthorpe6/DockerFiles/tree/master/InstantDomainAdmin

# docker run -it --rm -p 8443:8443 -p 80:80 -p 443:443 deathstar

FROM debian:stable

WORKDIR /root/

ENV LC_ALL C.UTF-8
ENV STAGING_KEY=RANDOM
ENV DEBIAN_FRONTEND noninteractive

ENV EMPIRE_USER='empireadmin'
ENV EMPIRE_PASS='Password123!'

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    git \
    tmux \
    curl \
    wget \
    sudo \
    locales \
    lsb-release \
    python-pip \
    python-dev \
    python3-pip \
    #python3-dev \
    python-m2crypto \
    apt-transport-https && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install impacket && \
    pip install libtmux

RUN git clone --depth=1 https://github.com/lgandx/Responder /opt/Responder && \
    sed -i "s/SMB = On/SMB = Off/g" /opt/Responder/Responder.conf && \
    sed -i "s/HTTP = On/HTTP = Off/g" /opt/Responder/Responder.conf && \
    sed -i "s/HTTPS = On/HTTPS = Off/g" /opt/Responder/Responder.conf

RUN git clone --recursive --depth=1 https://github.com/byt3bl33d3r/CrackMapExec /opt/CrackMapExec && \
    cd /opt/CrackMapExec && \
    rm -rf .git && \
    python setup.py install && \
    #run cme just to initialize it
    cme --help

# From https://github.com/EmpireProject/Empire/blob/master/Dockerfile
# NOTE - pip install of urllbb3 due to error with version 1.24 and can likely be removed if Empire updates requirements.txt:
# https://github.com/EmpireProject/Empire/issues/1266
RUN git clone --depth=1 -b dev https://github.com/EmpireProject/Empire.git /opt/Empire && \
    cd /opt/Empire/ && \
    rm -rf .git && \
    cd /opt/Empire/setup/ && \
    pip install urllib3==1.22 && \
    ./install.sh && \
    # installer grabs some more stuff from repo - clean it up!
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN git clone --depth=1 https://github.com/byt3bl33d3r/DeathStar /opt/DeathStar && \
    cd /opt/DeathStar && \
    rm -rf .git && \
    pip3 install -r ./requirements.txt

COPY entrypoint.py /opt/entrypoint.py
COPY tmux.conf /root/.tmux.conf
ENTRYPOINT ["python", "/opt/entrypoint.py"]

