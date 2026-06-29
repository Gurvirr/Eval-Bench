FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN pip3 install --break-system-packages \
    numpy==1.26.4 \
    pandas==2.2.3 \
    openpyxl==3.1.5 \
    reportlab==4.2.5

WORKDIR /root
COPY data/build_inputs.py /tmp/build_inputs.py
RUN python3 /tmp/build_inputs.py

COPY skills /root/.gemini/skills
COPY skills /root/.claude/skills
