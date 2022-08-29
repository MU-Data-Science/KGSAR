#!/bin/sh
python3 message.py "Loading.."
java -Xmx4g -cp /website/blazegraph.jar com.bigdata.rdf.store.DataLoader -namespace kb /website/RWStore.properties /data
python3 message.py "Starting Blazegraph"
java -Djetty.start.timeout=60 -server -Xmx4g -jar -Djetty.host=0.0.0.0 /website/blazegraph.jar &
python3 message.py "Ready"
python ./kgsar.py -t /data -r /images