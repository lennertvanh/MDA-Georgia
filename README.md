# **MDA-Georgia**

## Table of contents
- [Introduction](#introduction)
- [Data](#data)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Repository](#repository)
- [Resources](#resources)
- [Authors](#authors)

--- 
## Introduction
`MDA-Georgia` is an app giving insights about the noise and weather datasets concerning the city of Leuven. 
This had to be done as project for the course 'Modern Data Analytics' at KU Leuven during the 2022-2023 academic year. This app has been developed with the Dash interactive Python framework developed by [Plotly](https//plot.ly/).

---

## Data  

For the entire project, we used noise level and noise events data, weather data, traffic data, and a small corpus of scientific articles on noise pollution. 

The noise data contains noise levels which were monitored for the entire year of 2022, for 9 different locations in the centre of Leuven. The noise events were also recorded and were assigned a certainty level and a noise source class. All the noise data was provided by KU Leuven. The weather data from 2022 was retrieved from the [Leuven.cool network](https://rdr.kuleuven.be/dataset.xhtml?persistentId=doi:10.48804/SSRN3F). We scraped the traffic data from [Telraam](https://telraam-api.net/), which is documented in detail in the notebook _ScrapingTelraam.ipynb_. Finally, we scraped some scientific articles from PubMed Central about noise pollution to highlight the importance of our research topic, which is documented in the _NLP_ folder. 
 
---

## Installation

### Built With
* [Dash](https://dash.plot.ly/) - Main server and interactive components 
* [Plotly Python](https://plot.ly/python/) - Used to create the interactive plots

### Requirements
We suggest you to create a separate virtual environment running Python 3.9 for this app, and install all of the required dependencies there. Run in Terminal/Command Prompt:

```
git clone https://github.com/lennertvanh/MDA-Georgia.git
cd dash-sample-apps/apps/dash-manufacture-spc-dashboard/
python3 -m virtualenv venv
```
In UNIX system: 

```
source venv/bin/activate
```
In Windows: 

```
venv\Scripts\activate
```

To install all of the required `pip` packages to this environment, simply run:

```
pip install -r requirements.txt
```

Now, you're all set to succesfully run the app!

_**IMPORTANT**_:

The app was deployed on Heroku. Since the compressed app could only take up 500MB, we were obliged to create separate requirements files to run the app and to run any file in the repository. It’s important to mention that the _**requirements.txt**_ file contains the necessary packages to run the app, while the _**requirements-full.txt**_ file contains _all_ the necessary packages to run the app and all other files in the repository. So, if you also want to run any of our notebooks, run this line in the terminal instead:

```
pip install -r requirements-full.txt
```

---

## Usage

Run this app locally by running the following code in the terminal:
```
python app.py
```
The terminal will give the message 'Dash is running on [_http link_]'. By following this link, the homepage of the app will open in your browser. You can dive in and explore the app by clicking the links at the top of the page, which are categorized under 3 titles:

1. _Explore the noise data_: these pages contain interactive visualizations concerning the noise levels and noise events data
2. _Explore the weather data_: these pages show interactive visualizations concerning the meteo data
3. _Analysis_: these pages contain visualizations that combine different datasets, and display the results of the modeling 



---

## Examples

Explain what the user can see/do in the app, what the app shows (GIFs, screenshots, ...)

---

## Repository 

In this section, we provide a brief explanation of the structure and files in our repository. 

* _Data for visualization_: folder with data used for creating visualizations in the app
* _Data for modeling_: folder with data used for modeling, split in training and test data
* _Pages_: .py files for each page in the Dash app
* _Assets_: 
* _Exploration data_: folder with jupyter notebooks where we initially explored the data and created basic visualizations
* _NLP_: 
* _Preprocessing.ipynb_: jupyter notebook where we preprocessed the noise and weather data for both visualization and modelling purposes
* _Modelling_: 
* _app.py_: 
* _requirements.txt_:
* _ScrapingHolidays.ipynb_: jupyter notebook where we scraped holidays in 2022
* _ScrapingTelraam.ipynb_: jupyter notebook where we scraped and preprocessed traffic data 


---

## Resources
* [Dash User Guide](https://dash.plot.ly/)
* [Weather data from Leuven.cool network](https://rdr.kuleuven.be/dataset.xhtml?persistentId=doi:10.48804/SSRN3F)
* [Coloring for Colorblindness](https://davidmathlogic.com/colorblind/#%23D81B60-%231E88E5-%23FFC107-%23004D40)
* [Coolors Color Palette](https://coolors.co/223164-132244-eb862e-2a9d8f-e6af2e)
* [OpenAI. (2023). ChatGPT (April 20 version) [Large language model].](https://chat.openai.com/)
* [Plotly Graphing Libraries](https://plotly.com/python/)
* add other resources 

---

## Authors
* Grégoire Corluy - GregoireCorluy
* Ying Tian - yingtian1
* Yasemin Uslu - yasemin98
* Lennert Vanhaeren - lennertvanh
* Axl Wynants - awynants
