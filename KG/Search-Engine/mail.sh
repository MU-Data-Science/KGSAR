#!/bin/sh
printf "Starting Docker for Mac.";
open -a Docker;
while [[ -z "$(! docker stats --no-stream 2> /dev/null)" ]];
  do printf ".";
  sleep 1
done
echo "";

echo "Docker Engine is now running!"
echo "Logging into the private repository if this message is shown."
echo "Please enter Docker login password."
docker login --username=shivikaprasannamu
echo "Starting SMTP"
echo "Please enter the password you use to log into your machine."
sudo postfix start
echo "Pulling image from Docker"
docker pull shivikaprasannamu/kgsar-private:kgsar
echo "Running container inside image"
docker run -p 5001:5001 -p 9999:9999 shivikaprasannamu/kgsar-private:kgsar
