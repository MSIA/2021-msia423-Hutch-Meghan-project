# Temporal Modeling of COVID-19 Health Belief Phenotypes 

**Developer**: Meghan Hutch 

**QA support**: Irene Lai

## **Vision**

The COVID-19 pandemic has resulted in an infodemic of information regarding health, science, and public policy. This information not only reflects the public’s perception of our ongoing global health crisis but can also further impact it. Understanding the dynamics of public perception regarding COVID-19 is critical for strategizing policies to manage health. For this reason, we aim to develop a model and supplementary web application that delineates health belief phenotypes regarding perceptions towards COVID-19 susceptibility and severity, and regarding medications like hydroxychloroquine. Moreover, this model aims to explore the trajectory of these phenotypes over the course of the pandemic. If successful, this model can be extensible across other types of social media related content.

## **Mission**

On the backend, we will use an existing dataset of [> 5,500,000 COVID-19 related tweets](https://github.com/HanyinWang/CovidHealthBeliefTweets) previously classified into at least one of five categories: 1) Not related to health belief or related to 2) disease severity, 3) disease susceptibility, 4) benefits or 5) barriers of hydroxychloroquine. Latent Dirichlet Allocation topic modeling will be employed on the annotated tweets in order to identify sub-topics (to be referred to as phenotypes) of the aforementioned categories. 

Users of our application will be able to view the LDA dervied topics (phenotypes) at different time points since the start of the pandemic. dditionally, the app will include visuals to allow users to see how closely related phenotypes are with one another and which words are associated. The dynamic nature of the application will allow users and researchers to better evaluate the temporality of COVID-19 health belief phenotypes. Of note, because of the size of the data and the computational expense of processing text in such a large data source, the models have been pre-run and results have been stored at pre-selected time points. However, those who are interested in testing more time points, may download the repo and input there own timelines. 

## **Success Criteria**

Model performance will be evaluated using a topic coherence value metric such as c_v which uses a normalized point wise mutual information (PMI) and the cosine distance to help assess the semantic similarity between words that fall within the same topic. Such a method can also be used to evaluate the optimal number of topics by identifying which number of topics provides the overall highest coherence. As the tweets in our dataset are all COVID-19 related and have previously been queried to try and identify health related topics, a minimum coherence score of 0.7 is expected (c_v ranges from 0-1, where 1 is indicative of higher coherence). Moreover, once we identify the optimal number of topics, we can label each topic as belonging to one of the major 5 categories of health beliefs. Then we will employ supervised classification in order to test how well unseen tweets will classify into a topic matching its label.

The larger purpose of this application is to help support public awareness of changes in perception of our ensuing pandemic. Thus, widespread engagement with the app, as determined by number of page views, can be used to assess how well the application is achieving public outreach. Moreover, the success of the application can also be determined by quantifying how well the application continues to identify health belief phenotypes as updates regarding our understanding and management of COIVD-19 continues to development.


<!-- toc -->

- [Analysis](#analysis)
- [Results](#results)
- [APP](#app)
- [Directory structure](#directory-structure)
- [Intializing the Project](#running-the-app)
  * [1. Build the Image](#1-build-the-image)
  * [2a. Download data from S3](#2a-download-data-into-s3)
  * [2b. Upload data into S3](#2a-upload-data-into-s3)
  * [3. Generate database table](#3-generate_database-table)
  * [4. Run the models](#run-the-models)
  * [5. Testing](#testing")
  * [6. Run the App](#run-the-app)
  

<!-- tocstop -->

## Analysis

For users and researchers interested in the analysis, the following details the high-level overview of the project. 

1. 5.5 million COVID-19 health related tweets were processed via tokenization, removal of punctuation and lemmenization

2. Data was subset into different time frames of the pandemic: 1) Jan-15-2020-Jan-30-2020 and 2) March 01-2020-March-15-2020

3. Hyperparameter testing in terms of k topics was performed in order to identify the optimal number of topics (as determined by the max coherence score when performing LDA) for each timeframe of tweets

4. For each timeframe tested, the final LDA model was trained using the optimal k

5. Word clouds were generated in order for users and researchers of the app to visulize the themes of the derived topics

6. Moreover, a table was generated to containing the orginal tweets of the time frame. A new column was made to assign the topic_num containing the max probability of being associated with that tweet.

7. For each topic, the 3 tweets containing the highest probability for that topic are saved to a mysql table in order for users to review those tweets when using the app. 

8. Lastly, for each topic, we also count how many tweets had an original annotation of 1) Percieved Suseptibility, 2) Percieved Severity, 3) Percieved Barriers and 4) Percieved Benefits of Hydroxychloroquin. These results are saved in the 'data/results' folder.

## Results
    
While preliminary results are exploratory, we found that the max coherence metric was .... While lower than initially expected, it is believed that performance will improve upon the future deployment of rigorous hyperparameter tuning and removal of superfluous stopwords. Upon review of the word clouds and topic probabilities of tweets and their associated annotations, it does appear possible to identify themes in the topics and to see how these themes differed at different points during the pandemic.

## Deployed APP

[View the app](http://lda-t-publi-11a4tbf1s5d55-2039079140.us-east-1.elb.amazonaws.com/) deployed on Amazon ECS (instructions for building and deploying app locally are included below)


## Directory structure 

```
├── README.md                         <- You are here
├── app
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│    |── config.py                    <- supplementary logging configuration for Flask APP
     ├── flaskconfig.py               <- Configurations for Flask APP
|    ├── logging.conf                 <- Configuration of python loggers
│
├── copilot                           <- Directory for configuration files 
│     |── app.py                      <- Contains manifest.txt file with ECS deployment instructions.
|
├── data                              <- Folder that contains data used or generated when running the models. Only the sample/ subdirectories are tracked by git. 

│   ├── external/                     <- External data sources, usually reference data,  will downloaded from/uploaded to S3 bucket
│   ├── results/                      <- Tables generated from the model.
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── develop/                      <- Current notebooks being used in development.
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
 docker build -f app/Dockerfile -t msia423 .
```

### 2a) Download data from S3

The data used in this project has been generated by the [Luo Lab at Northwestern University](https://labs.feinberg.northwestern.edu/lyg/) and methods are detailed in this [recent manuscript by Wang et al 2021](https://pubmed.ncbi.nlm.nih.gov/33529155/). 


In order to connect to S3, please ensure that you have set AWS credentials as environment variables in your terminal. This can be performed by creating a text file **s3configs.txt** which contains:

```
export AWS_ACCESS_KEY_ID="YOUR ACCESS KEY"
export AWS_SECRET_ACCESS_KEY="YOUR SECRET KEY"
export AWS_DEFAULT_REGION="us-east-1"
```

Save this to the root of the directory. You can then import AWS credentials by running:

```
source s3configs.txt
```

To download data, ensure that you enter your ```lastname``` and ```firstname``` in the indicated line of code:

```bash
docker run --mount type=bind,source="$(pwd)"/data,target=/app/data -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY msia423 run.py --connect_type='download' --s3path='s3://2021-msia423-lastname-firstname/data/tweets.csv' --local_path='data/external/constructs.csv' --s3='s3'

```

### 2b) Upload data into S3

The following docker command uploads the data into a user's S3 Bucket. 

Ensure that you enter your ```lastname``` and ```firstname``` in the indicated line of code:

```
docker run --mount type=bind,source="$(pwd)"/data,target=/app/data -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY msia423 run.py --connect_type='upload' --s3path='s3://2021-msia423-lastname-firstname/data/tweets.csv' --local_path='data/external/constructs.csv' --s3='s3'
```

### 3. Generate database table

Create a text document named .mysqlconfig containing the following: 

```
user="admin"
password="PASSWORD"
host="HOST" 
port="3306"
db_name="msia423_db"
```
Or source your MYSQL variables in another way

MYSQL configures can be imported as follows: 

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
SELECT * from topics;
```

**Show columns in table:**

```bash
SHOW COLUMNS FROM topics;
```
## 4. Run Models

To run the preliminary January and March models, run the following docker command:

```
docker run msia423 models.py

```

## 5. Testing 

To perform unit testing upon cloning of the repo, run the following docker command:

```
docker run msia423 -m pytest test/unit_tests.py
```

## 6. Run the App

To run the Flask APP locally, run the following docker command: 

```
docker run -p 5000:5000 msia423
```
The app should be available at http://0.0.0.0:5000/ in your browser.
