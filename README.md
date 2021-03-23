# Zemoga Big Data project

This project contains the develop of the tech test for Python developer

## User Guide

![desire-arch](https://github.com/jcardenasc93/zemoga_datasets/blob/main/project_images/user_guide0.png)

This web application allows to upload the three `*.csv` files that compose the dataset. After this the user can browse through the linked data by different selectors that match with the corresponding fields until get the specific column name that requires. Finally when data points are found the user can download a `JSON` file with the data points information.

### Upload dataset files

The user uploads the corresponding `*.csv` files for each of the following fields: Namespaces, Column and Datapoints. To identify the uploaded dataset the form requires a name too.

![desire-arch](https://github.com/jcardenasc93/zemoga_datasets/blob/main/project_images/user_guide1.png)

When the dataset is successfully created the browser will ask to download a `anomalies_report.csv` file. This file contains all the detected anomalies across the files. Duplicated rows, no matching schema (Uncompleted fields), etc. This report specify the file, the line and the anomaly type found in the dataset. Even with those anomalies found the user could use the application to continue browsing the dataset to search for specific datapoints associated to a column table.

![desire-arch](https://github.com/jcardenasc93/zemoga_datasets/blob/main/project_images/user_guide2.png)

### Browse datasets

The interface asks to the user to select a dataset to browse, when the user selects a dataset then another view is rendered, that is the _fetch_ view, where the user browse the dataset linked data specifying a namespace, database, table and finally a column to lookup for related datapoints.

![desire-arch](https://github.com/jcardenasc93/zemoga_datasets/blob/main/project_images/user_guide4.png)

* The field options are filtered based on the previous user selection

  ![desire-arch](https://github.com/jcardenasc93/zemoga_datasets/blob/main/project_images/user_guide5.png)

  ![desire-arch](https://github.com/jcardenasc93/zemoga_datasets/blob/main/project_images/user_guide6.png)

### Download report

Finally when the user selections match with a datapoint the application show the number of datapoints found and ask for a file name (without spaces) to create the datapoints report in an specific `JSON` structure. Once the application creates the file the browser will download it

![desire-arch](https://github.com/jcardenasc93/zemoga_datasets/blob/main/project_images/user_guide8.png)

![desire-arch](https://github.com/jcardenasc93/zemoga_datasets/blob/main/project_images/user_guide9.png)



## Desired Architecture

Next you can see the desired architecture that I consider that would be provisioned in AWS Cloud services. Below you find the architecture components description

![desire-arch](https://github.com/jcardenasc93/zemoga_datasets/blob/main/project_images/desired_arch.png)

1. **AWS Fargate (App Layer):** This component handles the web application layer deployed over AWS Fargate service, this is ideal for the web application layer because is a low weight and low processing app so a deploy based in containers fits with the performance requirements. The app is a [django](https://www.djangoproject.com/) based web app with additional component to handle batch tasks like file uploading, this component is [Celery](https://docs.celeryproject.org/en/stable/index.html) a reliable distributed system to process queue tasks in short time
2. **Mongo Cluster:** The mongoDB cluster allows to persist the data coming from `*.csv` files, in order to retrieve linked data with the specified relationships. This service ([Mongo Atlas]((https://www.mongodb.com/))) is great choice because allows cluster deployments with different cloud services vendors.
3. **Computing cluster:** The computing cluster build on EC2 computing instances that has enough process power to handle the data frames generated by the application. Processes like clean data, prefetch data or find anomalies or dirty data should be executed here.
4. **Amazon SQS:** This service is the communication bridge between the application layer and the processing layer. Both send and receive messages with relevant information to run specific actions.
5. **Amazon S3:** The storage bucket to keep the uploaded `*.csv` files and the generated `*.csv` and `*.json` files

## Current Architecture

The delivered application was deployed in the follow architecture

![er-model](https://github.com/jcardenasc93/zemoga_datasets/blob/main/project_images/current_arch.png)

This is a simple monolithic app deployed in a basic free [Heroku dyno](https://www.heroku.com/dynos), this component embeds the app layer and the processing layer, so the same dyno performs application layer related operations and data frame processing as well. The mongoDB cluster component was provisioned over the [Mongo Atlas](https://www.mongodb.com/) services described before in the free plan subscription.

## Tech Requirements

* [python 3.8](https://www.python.org/downloads/release/python-388/)

* [pipenv](https://pipenv.pypa.io/en/latest/) (To install it just run `pip3 install pipenv`)

* [Django 3.1](https://www.djangoproject.com/download/)

  

## Steps to launch the project on a local machine

To launch the project just follow the next steps:

1. Clone the repo
2. Run `cd zemoga_datasets && pipenv install` this command will install the required packages
3. Copy `.env.example` file to `.env` and adjust the environment variables values with the given in the file
4. Create the `DJANGO_SECRET_KEY` with the following command `python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'`
5. Activate the virtual environment with `pipenv shell`
6. Finally just run `python manage.py runserver` and the app will be serve in your `localhost` on port `8000`

## Software Components

### Django

As described before this application is build with django web framewrok, this is a open-source framework that allows develop and deploy web application based on python in a really straightforward way. Based on a fork of the MVC architecture; defined as MVT (Model View Template) , the framework ensures low coupling and is focused in the DRY (Don't Repeat Yourself) concept. One of its most powerful tools is the Django ORM, make query process really easy and efficient. 

#### MVT

* **Model**

  Is the interface between the data and the application, so exist a python object representation of each row in the database and you can access them like a simple python class

* **View**

  This is the logic business interface, so different parts of the program executes based on the incoming requests. The view interacts constantly with the Model layer to read and write data.

* **Template**

  The template is the presentation layer (what users see). So this layer is composed of `*.html`, `*.css` and `*.js` files normally. The template layer acts like the user interface between the browser and the View layer.

### Djongo

Django was developed to works with relational databases such like PostgreSQL, SQLite or MySQL. But the [djongo project](https://www.djongomapper.com/) is the best approach to integrate NoSQL databases with Django applications. Keeps the fundamentals key concepts of Django framework and the integration with the MVT pattern just works. Djongo implements a different Model layer inherited from the base Django Model layer, so the ORM is capable to make queries to mongoDB instances.

### Pandas

The [pandas](https://pandas.pydata.org/) tool is very popular open source package to manipulate data and make analysis with it. The core component of this package is `DataFrame` component, this is a two dimensional data structure just like a spreadsheet, this allows to have different columns with different data types and apply different kind of operations over the data.

This component process the data coming from the `*.csv` files, so the data manipulation can be performed over pandas data frames and then be replicated to the database layer. With pandas the execution of pre-fetch data operations are perform, so basically this tool search for duplicated rows, anomalies in the data, to be reported later in the anomalies report file.







