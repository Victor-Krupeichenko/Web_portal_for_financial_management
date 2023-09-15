FROM python:3.10.12
RUN mkdir /web_portal
WORKDIR web_portal
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod a+x docker_start/*.sh