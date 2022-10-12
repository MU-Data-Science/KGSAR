# Running the KGSAR Information Retrieval Tool

# Description of KGSAR

KGSAR stands for Knowledge Graphs for Spanish-American notary Records and is a tool that performs information retrieval, given a search word, and allows users to annotate to add, update, or delete more words while searching. These annotated words are then utilized for further model retraining. 

# Accessing using Docker
To run our tool on your system, you can simply pull our docker image (latest: kgsar_v3) by running the following script in your terminal.

```
    $ ./run-kgsar.sh
```

![Search-Engine-Login](/Screenshots/search-engine-run-successful.png)
![Search-Engine-Blazegraph](/Screenshots/search-engine-run-blazegraph.png)

You will be prompted for the docker login credentials and your system password to enable mailing (this information is not stored anywhere). You will be required to have Docker Desktop installed on your system. The latest docker images contains a subset of 4 rollos and their corresponding knowledge graphs in turtle (.ttl) format.

Please note that kgsar_v3 is a private Docker image and <u>will</u> require you to enter the password to the repository when prompted.

![Search-Engine-Success](/Screenshots/search-engine-run-success.png)

# Accessing the tool locally

The tool can also be run locally on your machine, on a much larger dataset. To do this, please make the following changes:

Step 1:
    Add the local absolute paths (complete directory path) for the images and turtles to [kgsar.py](/Search-Engine/Root/website/kgsar.py).

Step 2:
    Download the images from OneDrive (please request Dr. Praveen Rao for access) and add them to a folder under [Root](/Search-Engine/Root/). <br/> 
    Add the [turtle](/KG/Turtles/) files to another folder under Root.

![Local-Adding-Paths](/Screenshots/local-adding-paths.png)

Step 3:
    In [RWStore.properties](/Search-Engine/Root/website/RWStore.properties), change the path in line 11, to the local path where the Blazegraph jar file is stored. <br />
    <!-- In [run.sh](/Search-Engine/Root/website/run.sh), change the argument paths in line 7 to the local paths set in Step 1. -->

![Local-RWStoreProperties](/Screenshots/local-RWStoreProperties.png)

Step 4:
    Run the blazegraph jar in one Terminal window followed by [kgsar.py](/Search-Engine/Root/website/kgsar.py) in another Terminal window. Please remember to run the following steps inside a Conda enviroment, especially if using a MacOS with an M1 chip (packages like OpenCV cannot be installed directly on M1 chip as of 2022).

        $ java -server -Xmx4g -jar /path/to/blazegraph.jar

![Local-Blazegraph](/Screenshots/local-run-blazegraph.png)

        $ python3 /website/kgsar.py -t /root/directory/for/ttlfiles -r /cleaned/images/root/directory

![Local-Run-Code](/Screenshots/local-run-code.png)

Step 5:
    Open your browser and type localhost:5001/load (assuming our port number is 5001) to load all the turtle files into Blazegraph. Check your terminal to see if all the files have been loaded. You should see "Completed loading ttls!" message.

![Local-Completed-Loading](/Screenshots/local-run-completed-loading.png)

Step 6:
    In the same browser, edit your URL to localhost:5001 and hit Enter. The tool is now up and running!

![Local-Sucessful-Run](/Screenshots/local-success.png)

Notes:
1. To use Conda environment, follow the installation requirements in [kgsar.py](/Search-Engine/Root/website/kgsar.py).

2. If Blazegraph does not automatically load all the turtle files, you can call the following API:

    localhost:5001/load

There are more API utilities available in the code.

## Contributing Authors:
**Shivika Prasanna**