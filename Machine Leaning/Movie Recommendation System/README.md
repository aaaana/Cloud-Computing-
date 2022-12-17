# Implementation on GCP 
* [Google Slide] (https://docs.google.com/presentation/d/1UrF22QwhtrPH9wG5J1EefAUCjHTc83bwmwcmJqAYRIE/edit?usp=sharing)
## Create Clsuter on GCP 
* Enable the Google Cloud Engine API and Dataproc API
* Create a Dataproc Cluster
* Connecting to the Master Node using Secure Shell (ssh)
## Download and store data in HDFS
```
$ hdfs dfs -mkdir hdfs:///mydata
```
* Upload and store movielens.py from local
```
$ hdfs dfs -put recommendation_engine_movielens.py hdfs:///mydata
$ hdfs dfs -ls hdfs:///mydata
```
* Install pyspark 
```
$ pyspark
```
* put data into same environment 
```
$ hdfs dfs -put movies.csv hdfs:///mydata
$ hdfs dfs -put ratings.csv hdfs:///mydata
```
* Run the Code
```
$ spark-submit recommendation_engine_movielens.py
```


