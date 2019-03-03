FROM partlab/ubuntu-golang

RUN mkdir -p /app
COPY . /app
WORKDIR /app

RUN apt-get update
RUN apt-get -y install cmake
RUN apt-get install -y python3-pip
RUN apt-get install -y build-essential libssl-dev libffi-dev python-dev
RUN pip3 install -r requirements.txt

EXPOSE 5001 8082

RUN ["chmod","+x","start.sh"]
ENTRYPOINT ["bash","start.sh"]
