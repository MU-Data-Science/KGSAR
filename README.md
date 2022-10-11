# KGSAR: A knowledge graph for 17th Spanish American Notary Records

The goal of this project is to develop an informational retrieval system that utilizes knowledge graphs that has been made available to historians and other users. We have processed 20,000 images from a collection of 200,000 images containing handwritten notary documents that are now digitized. We used deep learning methods such as Keras-OCR and YOLO-OCR for identifying words within these cleaned digitized images and then utilized Resource Description Framework (RDFs) and SPARQL to query [Blazegraph](https://blazegraph.com) that acts as the graph storage. Blazegraph is an open-source graph database supporting Blueprints and RDF/SPARQL APIs and can support upto 50 Billion edges on a single machine.

Apart from the various features our novel system provides, we have also developed a keyboard that users can use if they are interested in exploring or preparing documents in the handwriting of Baldibia y Brisuela, a 17th century interim notary officer, in the city of Buenos Aires, Argentina, in 1658.

Our collaborative work can also be found on [UMKC-BigDataLab](https://github.com/UMKC-BigDataLab/DeepLearningSpanishAmerican). This includes character and words datasets, and retraining the models.

# Table of Contents
[Tools Required](#tools-required)

[Generating Knowledge Graphs](#generating-knowledge-graphs)

[KGSAR as an Information Retrieval System](#kgsar-as-an-information-retrieval-system)

[Keyboard](#keyboard)

[Team](#team)

[Publications](#publications)

[Acknowledgments](#acknowledgments)

# Tools Required
<ul>
    <li> Cloudlab
    <li> Docker (Docker Desktop)
    <li> Terminal (MacOS - Click on Launchpad -> Others -> click Terminal) or PowerShell (Windows - Click start -> type PowerShell -> click Windows PowerShell)
</ul>

# Generating Knowledge Graphs
The images in this dataset are from the digitized collection of Spanish-American notary records from 17th century, available at Archivo General de la República Argentina (National Archives), Buenos Aires. To create our dataset for model training, we extracted characters from the deeds notarized by Don Nicolas de Baldibia y Brisuela who acted as interim notary while serving as alcalde ordinario (city councilman) in the city of Buenos Aires in 1658. 

The images were first cleaned and denoised. Then, deep learning methods such as Keras-OCR and YOLO-OCR have been applied to generate predictions and bounding boxes. This information, along with the document and page information have been stored as knowledge graphs. The ontology definition can be found in [this](/KG/Turtles/definitions.ttl) file. To run this pipeline, the steps have been mentioned in this [README.md](/KG/README.md). The turtle files generated for the 20,000 images can be found in [this](/KG/Turtles/) directory.

It is recommended to use Cloudlab for generating knowledge graphs, as the dataset size is large and the computation may take longer. You may signup for a Cloudlab account [here](https://cloudlab.us/signup.php). Once you have setup an account, please follow the steps below.

## Starting an experiment on Cloudlab

Step 1: After you login, you will be able to see all the existing experiments. If you do not have one already, click on "Experiments" and then "Start experiment".

Step 2: Pick a project and select any available resource. You may check the availability by clicking on "Resource Availability".

Step 3: Choose a name for your experiment and number of nodes and click on "Next". You may change the number of hours, however, it is recommended to extend the experiment only if you require the node for longer.

Your experiment will be ready in a few minutes!

## Setting up Conda environment

Step 1: Set a public and private key to be able to successfully SSH into the experiment. Once successful, SSH into the experiment from your terminal for MacOS users and Putty for Windows users. The SSH command is available in the "List View", under "SSH command".

Step 2: Once you are logged in, change the directory to "/mydata" and create a new directory.

    $ cd /mydata
    $ mkdir kgsar_exp

Step 3: Clone this repository.

    $ git clone https://github.com/MU-Data-Science/KGSAR.git

Step 4: Create and activate a new Conda environment with Python version 3.7.3. This version is important as there are library dependencies.

    $ cd /mydata && wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
    $ bash Anaconda3-2022.05-Linux-x86_64.sh -b -p /mydata/anaconda3
    $ export PATH=/mydata/anaconda3/bin:$PATH
    $ echo 'export PATH=/mydata/anaconda3/bin:$PATH' >> ~/.profile && . ~/.profile
    $ conda init
    $ cd kgsar_exp && conda create -n name_of_environment python=3.7.3
    $ conda activate name_of_environment

Step 5: Install all the required packages.

    $ pip3 install tensorflow==2.4.3 or pip3 install tensorflow==2.6.2
    $ pip3 install pandas
    $ pip3 install matplotlib
    $ pip3 install scipy
    $ pip3 install sklearn
    $ pip3 install rdflib
    $ pip3 install imutils
    $ pip3 install keras-ocr
    $ pip3 install openpyxl
    $ pip3 install xlrd
    $ pip3 install --upgrade opencv-python==4.5.4.60

You are now ready to generate knowledge graphs by following the execution instructions in the [KG-Gen-README.md](/KG/README.md)!

<b>NOTE:</b> The given instructions have been tested in an environment with Python version 3.7.3. If using any other Python versions, you may encounter version mismatch issues for other packages being used.
 
# KGSAR as an Information Retrieval System
The knowledge graphs were then uploaded into Blazegraph using SPARQL queries. The system allows users to search for a keyword and the query API is then called with the search word. Blazegraph internally performs [FullTextIndex](https://github.com/blazegraph/database/wiki/FullTextSearch), which allows for exact and partial matching. The resulting images with the bounding boxes are then ordered and displayed to the user.

The system also allows users to annotate further on the result images. The user may choose to correct/update a word, add new labels in the image or simply delete an incorrect prediction. These are then emailed to us and this allows us to do further retraining on our models for better, more accurate predictions.

There are multiple ways this tool can be accessed.

## Docker Image
1. Clone this repository and navigate to the 'Search Engine' [folder](/Search-Engine/).
2. Run [run-kgsar.sh](/Search-Engine/run-kgsar.sh)

Further execution instructions are available in this [Accessing-Docker-README.md](/Search-Engine/README.md#accessing-using-docker).

## Running on a local system

If you wish to run the tool outside of the Docker image, that is, not using a Docker Image, please follow the steps mentioned in the README below.

Clone this repository and make the changes in this [Accessing-Tool-Locally-README.md](/Search-Engine/README.md#accessing-the-tool-locally)

## Docker Desktop

Using the available Docker Desktop application, you can also pull our Docker image and run our tool.

Step 1: Install [Docker](https://docs.docker.com/get-docker/).

Step 2: Start Docker Desktop.

Step 3: Navigate to 'Images/REMOTE REPOSITORIES" and pull the latest image under the repository 'shivikaprasannamu'. 
As of 08/29/2022, the latest tag is of the name 'kgsar_v3' and this is a private image. You <u>will</u> be prompted for the password for the repository. Please contact Dr. Praveen Rao or Shivika Prasanna for this. 
By default, you will be able to pull our public image named 'kgsar'. 

Step 4: Hover over the image and click on 'PULL'.

Step 5: Navigate to 'Images/LOCAL', hover over the pulled image and click on 'RUN'. Under 'Container Ports', click on the plus sign and add '9999'.

Step 6: Open your browser and type "http://localhost:5002". 

## Rebuilding a Docker image

If you wish to create your own Docker image, please follow the following:

Assuming you have cloned the directory and are inside the Search-Engine folder, create two folders for Images and Turtle files (outside the Root directory). Replace or add the turtle files and the images to their respective folders and run the following command from inside the current Search-Engine folder:

```
    $ docker build -t name_of_image .
```

Once the docker image is built, you can push the image to your Docker repository using the following:

```
    $ docker push name_of_repository:tag_name
```

You can also locally run this image using the following command:

```
    $ docker run -p 5001:5001 -p 9999:9999 name_of_tag
```

Note: <b>If you have not made any changes to the RWStoreProperties and run.sh files, you will be able to build and run your new image successfully. The files in this repository are by default set to running the image from Docker.</b>

Taken from [Docker Documentation](https://docs.docker.com/engine/reference/commandline/image_build/). 

Disclaimer: All the experiments have been done on Cloudlab and MacOS (version 12.4, M1 chip, 2020).

# Keyboard
## Installing font locally
This virtual keyboard will work on your browser, even if the font has not been installed locally. To be able to work offline with this, please follow the instructions below.

Step 1: Install the .ttf file by cloning this repository or downloading from [here](https://github.com/MU-Data-Science/KGSAR/blob/main/font/NicolasDeValdiviaYBrizuela-Regular.ttf).
Step 2: Navigate to the folder where the .ttf has been cloned or downloaded.
Step 3: Double click on the .ttf file and click on "Install Font" (shown in the image below).
<img src="docs/static/install.png" width="528" height="178">

The font installation is now complete!

To verify, in your Font Book, find and ensure the tick box is highlighted in blue color.
![](docs/static/verify.png)  

## Accessing the Keyboard
You can directly access the keyboard using this [link](https://mu-data-science.github.io/KGSAR/). However, to see the font locally in your system after downloading your file from the notepad attached to the keyboard, please install the font as described in the above section.

# Team
Faculty - Dr. Praveen Rao (Co-PI, MU), Dr. Viviana Grieco (PI, UMKC)

Current Ph.D students - Shivika Prasanna (MU), Nouf Alrasheed (UMKC)

Past M.S. students - Parshad Suthar (MU), Pooja Purushatma (MU)

Our website can be accessed [here](https://www.umkc.edu/mide/NEH-Project/).

# Publications
1. Shivika Prasanna, Nouf Alrasheed, Parshad Suthar, Pooja Purushatma, Praveen Rao and Viviana Grieco - KGSAR: A Knowledge Graph-Based Tool for Managing Spanish Colonial Notary Records. In the 21st International Semantic Web Conference (ISWC 2022), 4 pages, China, 2022. (demo, to appear)
2. Nouf Alrasheed, Praveen Rao, and Viviana Grieco - Character Recognition of Seventeenth-Century Spanish American Notary Records Using Deep Learning. In Digital Humanities Quarterly (DHQ) Journal, Vol. 15, No. 4, 16 pages,  2021.
3. Nouf Alrasheed, Shivika Prasanna, Ryan Rowland, Praveen Rao, Viviana Grieco, and Martin Wasserman - Evaluation of Deep Learning Techniques for Content Extraction in Spanish Colonial Notary Records. In 3rd Workshop on Structuring and Understanding of Multimedia Heritage Contents (SUMAC), co-located with ACM Multimedia 2021, pages 23-30, 2021.

# Acknowledgments
This work was supported by the National Endowments for the Humanities Grant No. [HAA-271747-20](https://securegrants.neh.gov/publicquery/main.aspx?f=1&gn=HAA-271747-20) and a [Research and Creative Works Strategic Investment Tier 3 Award from the University of Missouri System](https://www.umsystem.edu/president-blog/strategic-plan-research-investments).
