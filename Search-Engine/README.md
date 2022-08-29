# Running the KGSAR Information Retrieval Tool

# Description of KGSAR

KGSAR stands for Knowledge Graphs for Spanish-American notary Records and is a tool that performs information retrieval, given a search word, and allows users to annotate to add, update, or delete more words while searching. These annotated words are then utilized for further model retraining. 

# Accessing using Docker
To run our tool on your system, you can simply pull our docker image (latest: kgsar_v3) by running the following script.

```
    $ ./run-kgsar.sh
```

You will be prompted for the docker login credentials and your system password to enable mailing (this information is not stored anywhere). You will be required to have Docker Desktop installed on your system. The latest docker images contains a subset of 4 rollos and their corresponding knowledge graphs in turtle (.ttl) format.

# Accessing the tool locally

The tool can also be run locally on your machine, on a much larger dataset. To do this, please make the following changes:

Step 1:
    Add the local paths for the images and turtles to [kgsar.py](/Search-Engine/Root/website/kgsar.py).

Step 2:
    Download the images from OneDrive (please request Dr. Praveen Rao for access) and add them to a folder under [Root](/Search-Engine/Root/). Add the [turtle](/KG/Turtles/) files to another folder under Root.

Step 3:
    **a.** In [RWStore.properties](/Search-Engine/Root/website/RWStore.properties), change the path in line 11, to the local path where the Blazegraph jar file is stored.
    **b.** In [run.sh](/Search-Engine/Root/website/run.sh), change the argument paths in line 7 to the local paths set in Step 1.

Step 4:
    **a.** Run the blazegraph jar followed by [kgsar.py](/Search-Engine/Root/website/kgsar.py).

        $ java -server -Xmx4g -jar /path/to/blazegraph.jar
        $ python3 /website/kgsar.py -t /root/directory/for/ttlfiles -r /cleaned/images/root/directory
    
To use Conda environment, follow the installation requirements in [kgsar.py](/Search-Engine/Root/website/kgsar.py).

## Contributing Authors:
**Shivika Prasanna**