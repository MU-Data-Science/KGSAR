# KGSAR: A knowledge graph for 17th Spanish American Notary Records

# Keyboard:
# Acknowledgments
This work was supported by the National Endowments for the Humanities Grant No. [HAA-271747-20](https://securegrants.neh.gov/publicquery/main.aspx?f=1&gn=HAA-271747-20).

# Installing font locally
This virtual keyboard will work on your browser, even if the font has not been installed locally. To be able to work offline with this, please follow the instructions below.

1. Install the .ttf file by cloning this repository or downloading from [here](https://github.com/MU-Data-Science/KGSAR/blob/main/font/NicolasDeValdiviaYBrizuela-Regular.ttf).
2. Navigate to the folder where the .ttf has been cloned or downloaded.
3. Double click on the .ttf file and click on "Install Font" (shown in the image below).
<img src="docs/static/install.png" width="528" height="178">

The font installation is now complete!

To verify, in your Font Book, find and ensure the tick box is highlighted in blue color.
![](docs/static/verify.png)    

# Docker:
1. Install [Docker] (https://docs.docker.com/get-docker/).
2. Start Docker Desktop.
3. Navigate to 'Images/REMOTE REPOSITORIES" and pull the latest image under the repository 'shivikaprasannamu'. 
As of 11/19/2021, the latest tag is of the name 'test2'.
4. Hover over the image and click on 'PULL'.
5. Navigate to 'Images/LOCAL', hover over the pulled image and click on 'RUN'.
6. Open your browser and type "http://localhost:10010". 
- If the port is already in use, please set another port under 'Optional Settings" before running the image. 