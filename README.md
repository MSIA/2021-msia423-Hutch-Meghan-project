# Modeling COVID-19 Health Beliefs

**Developer**: Meghan Hutch 

**QA support**: Irene Lai

## **Vision**

The COVID-19 pandemic has resulted in an infodemic of information regarding health, science, and public policy. This information not only reflects the public’s perception of our ongoing global health crisis but can also further impact it. Understanding the dynamics of public perception regarding COVID-19 is critical for strategizing policies to manage health. For this reason, we aim to develop a model and supplementary web application that delineates health belief phenotypes regarding perceptions towards COVID-19 susceptibility and severity, and regarding medications like hydroxychloroquine. Moreover, this model aims to explore the trajectory of these phenotypes over the course of the pandemic. If successful, this model can be extensible across other types of social media related content.

## **Mission**

On the backend, we will use an existing dataset of [> 5,000,000 COVID-19 related tweets](https://github.com/HanyinWang/CovidHealthBeliefTweets) previously classified into at least one of five categories: 1) Not related to health belief or related to 2) disease severity, 3) disease susceptibility, 4) benefits or 5) barriers of hydroxychloroquine. Latent Dirichlet Allocation topic modeling will be employed on the annotated tweets in order to identify sub-topics (to be referred to as phenotypes) of the aforementioned categories. 

Users of our application will be able to toggle an interactive timeline to examine the identified phenotypes at different time points since the start of the pandemic. Depending on the selected timeframe of interest, the topic model will only run on tweets written during that timeframe. Additionally, the app will include visuals to allow users to see how closely related phenotypes are with one another and which words are associated. The dynamic nature of the application will allow users and researchers to better evaluate the temporality of COVID-19 health belief phenotypes.

## **Success Criteria**

Model performance will be evaluated using a topic coherence metric such as UCI which uses point wise mutual information (PMI) and the cosine distance to help assess the semantic similarity between words that fall within the same topic. Such a method can also be used to evaluate the optimal number of topics by identifying which number of topics provides the overall highest coherence. As the tweets in our dataset are all COVID-19 related and have previously been queried to try and identify health related topics, a minimum coherence score of 0.7 is expected. Moreover, once we identify the optimal number of topics, we can label each topic as belonging to one of the major 5 categories of health beliefs. Then we will employ supervised classification in order to test how well unseen tweets will classify into a topic matching its label.

The larger purpose of this application is to help support public awareness of changes in perception of our ensuing pandemic. Thus, widespread engagement with the app, as determined by number of page views, can be used to assess how well the application is achieving public outreach. Moreover, the success of the application can also be determined by quantifying how well the application continues to identify health belief phenotypes as updates regarding our understanding and management of COIVD-19 continues to development.


<!-- toc -->

- [Directory structure](#directory-structure)
- [Intializing the Project](#running-the-app)
  * [1. Build the Image](#1-build-the-image)
  * [2. Upload data into S3](#2-upload-data-into-s3)
  * [3. Generate database table](#3-generate_database-table)

<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Intializing the Project

### 1. Build the Image 

The Dockerfile for running uploading data to S3 and for building the database table is found in the `root` of the directory. This command builds the Docker image, with the tag `msia423`, based on the instructions in `Dockerfile` and the files existing in this repo

To build the image, run from this directory (the root of the repo): 

```bash
 docker build -t msia423 .
```

### 2a) Upload data into S3

The data used in this project has been generated by the [Luo Lab at Northwestern University](https://labs.feinberg.northwestern.edu/lyg/) and methods are detailed in this [recent manuscript by Wang et al 2021](https://pubmed.ncbi.nlm.nih.gov/33529155/). Due to the large nature of the dataset, a sample of 100 tweets have been uploaded to 'data/sample/tweets.csv'. 

The following docker command uploads the sample data into a user's S3 Bucket. Please ensure that you have set AWS credentials as environment variables in your terminal. This can be performed by creating a text file **s3configs.txt** which contains:

```
export AWS_ACCESS_KEY_ID="YOUR ACCESS KEY"
export AWS_SECRET_ACCESS_KEY="YOUR SECRET KEY"
export AWS_DEFAULT_REGION="us-east-1"
```

Import AWS credentials by running:

```
source s3configs.txt
```

Ensure that you enter your ```lastname``` and ```firstname``` in the indicated line of code:

```bash
docker run --mount type=bind,source="$(pwd)"/data,target=/app/data -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY msia423 run.py --connect_type='upload' --s3path='s3://2021-msia423-lastname-firstname/data/sample_tweets.csv' --s3='s3'
```

### 2b) To download data from S3

Ensure that you enter your ```lastname``` and ```firstname``` in the indicated line of code:

```
docker run --mount type=bind,source="$(pwd)"/data,target=/app/data -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY msia423 run.py --connect_type='download' --s3path='s3://2021-msia423-lastname-firstname/data/sample_tweets.csv' --local_path='data/sample/tweets.csv' --s3='s3'
```

### 3. Generate database table

Import mysql configurations which should contain your  MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, and MYSQL_PORT. Use DATABASE_NAME="msia423_db" to follow along with the following directions

```bash
source .mysqlconfig
```

The following docker command generates a table for future storage of our data. 

```bash
docker run -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_HOST -e MYSQL_PORT -e DATABASE_NAME msia423 run.py --mysql='mysql'
```

## 4. View mysql table

Upon running the docker command to create the mysql table, view the mysql container as follows:

```bash
docker run -it --rm \ mysql:5.7.33 \ mysql \ -h$MYSQL_HOST \ -u$MYSQL_USER \ -p$MYSQL_PASSWORD
```

***Note: If you're using windows, append `winpty` to the following command:***

```bash
winpty docker run -it --rm \ mysql:5.7.33 \ mysql \ -h$MYSQL_HOST \ -u$MYSQL_USER \ -p$MYSQL_PASSWORD
```

**View mysql table:**

```bash
show databases;
```

**Use msia423_db:**

```bash
use msia423_db;
```

**View table:**

```bash
SELECT * from tweets;
```

**Show columns in table:**

```bash
SHOW COLUMNS FROM tweets;
```




