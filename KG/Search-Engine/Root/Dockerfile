# set base image (host OS)
FROM python:3.6
MAINTAINER Shivika Prasanna "spn8y@umsystem.edu"

# set the working directory in the container
WORKDIR /website
ADD website/blazegraph.jar blazegraph.jar

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN apt-get update && apt-get install -y python3-opencv
RUN pip3 install opencv-python
RUN pip install -r requirements.txt
RUN apt-get install -y openjdk-11-jdk
RUN apt-get install -y sendmail mutt vim
RUN pip install art

# copy the content of the local src directory to the working directory
COPY website/ .

COPY /subTurtles /data
COPY /subImages /images

RUN chmod +x run.sh
EXPOSE 9999
EXPOSE 5001

CMD [ "./run.sh" ] 
