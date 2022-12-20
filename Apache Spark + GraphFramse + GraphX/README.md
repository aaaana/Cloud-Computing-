#  Apache Spark + GraphFramse + GraphX
## Create Cluster on GCP 
* refer previous task 
## Prepare data
* upload person.csv and relation.csv from local to the GCP cluster 
## Create HDFS file system and copy the data to hdfs
```
$ hdfs dfs -mkdir hdfs:///mydata
$ hdfs dfs -put ./*csv hdfs:///mydata/
$ hdfs dfs -ls hdfs:///mydata

```

## Create the graphdemo.py file and change the path for data files
## Run the code in pyspark line by line 
```
$ pyspark --version
$ pyspark --packages graphframes:graphframes:0.8.2-spark3.1-s_2.12
$ from graphframes import *
$ personsDf = spark.read.csv('in/persion.csv',header=True, inferSchema=True)
$ personsDf.createOrReplaceTempView("persons")
$ spark.sql("select * from persons").show()

$ relationshipDf = spark.read.csv('in/relationship.csv',header=True, inferSchema=True)

$ relationshipDf.createOrReplaceTempView("relationship")
$ spark.sql("select * from relationship").show()

$ graph = GraphFrame(personsDf, relationshipDf)
$ graph.degrees.filter("id = 1").show()
$ graph.inDegrees.filter("id = 1").show()
$ graph.outDegrees.filter("id = 1").show()

$ personsTriangleCountDf = graph.traiangleCount()
$ personsTriangleCountDf.show()
$ personsTriangleCountDf.createOrReplaceTempView("personsTriangleCount")
$ maxCountDf = spark.sql("select max(count) as max_count from personsTriangleCount")
$ maxCountDf.createOrReplaceTempView("personsMaxTriangleCount")
$ spark.sql("select * from personsTriangleCount P JOIN (select * from personsMaxTriangleCount) M ON (M.max_count = P.count) ").show()

$ pageRank = graph.pageRank(resetProbability=0.20, maxIter=10)
$ pageRank.vertices.printSchema()
$ pageRank.edges.orderBy("weight",ascending=False).show()

$ graph.bfs(fromExpr = "Name='Bob'",toExpr = "Name='William'").show()
$ graph.bfs(fromExpr = "age < 20", toExpr = "name = 'Rachel'").show()
$ graph.bfs(fromExpr = "age < 20", toExpr = "name = 'Rachel'", edgeFilter = "relation != 'Son'").show()
    
```
## Modify graphdemo.py
```
# Import PySpark
$ import pyspark
$ from pyspark.sql import SparkSession

#Create SparkSession
$ spark = SparkSession.builder.master("local[1]").appName("GraphXDemo").getOrCreate()

```
## Run graphdemo.py
```
$ spark-submit --packages graphframes:graphframes:0.8.2-spark3.1-s_2.12 graphdemo.py
```
