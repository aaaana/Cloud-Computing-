
# Import PySpark
import pyspark
from pyspark.sql import SparkSession

#Create SparkSession
spark = SparkSession.builder.master("local[1]").appName("GraphXDemo").getOrCreate()

from graphframes import *

#######################################################
# Recipe 9-1. Create GraphFrames
#######################################################

#######################################################
#     person dataframe : id, Name, age
#######################################################
personsDf = spark.read.csv('hdfs:///mydata/person.csv',header=True, inferSchema=True)

# Create a "persons" SQL table from personsDF DataFrame
#    +--+-------+---+
#    |id|   Name|Age|
#    +--+-------+---+
#    | 1| Andrew| 45|
#    | 2| Sierra| 43|
#    | 3|    Bob| 12|
#    | 4|  Emily| 10|
#    | 5|William| 35|
#    | 6| Rachel| 32|
#    +--+-------+---+
personsDf.createOrReplaceTempView("persons")
spark.sql("select * from persons").show()

# relationship dataframe : src, dst, relation
relationshipDf = spark.read.csv('hdfs:///mydata/relation.csv',header=True, inferSchema=True)
#relationshipDf.show()

# Create a "relationship" SQL table from relationship DataFrame
#     +---+---+--------+
#     |src|dst|relation|
#     +---+---+--------+
#     |  1|  2| Husband|
#     |  1|  3|  Father|
#     |  1|  4|  Father|
#     |  1|  5|  Friend|
#     |  1|  6|  Friend|
#     |  2|  1|    Wife|
#     |  2|  3|  Mother|
#     |  2|  4|  Mother|
#     |  2|  6|  Friend|
#     |  3|  1|     Son|
#     |  3|  2|     Son|
#     |  4|  1|Daughter|
#     |  4|  2|Daughter|
#     |  5|  1|  Friend|
#     |  6|  1|  Friend|
#     |  6|  2|  Friend|
#     +---+---+--------+
relationshipDf.createOrReplaceTempView("relationship")
spark.sql("select * from relationship").show()

# - Create a GraphFrame from both person and relationship dataframes
#     >>> graph
#     GraphFrame(v:[id: int, Name: string ... 1 more field], e:[src:
#     int, dst: int ... 1 more field])
# - A GraphFrame that contains v and e.
#   + The v represents vertices and e represents edges.

graph = GraphFrame(personsDf, relationshipDf)

# - Degrees represent the number of edges that are connected to a vertex.
#   + GraphFrame supports inDegrees and outDegrees.
#     - inDegrees give you the number of incoming links to a vertex.
#     - outDegrees give the number of outgoing edges from a node.
# - Find all the edges connected to Andrew.
#     +--+------+
#     |id|degree|
#     +--+------+
#     | 1|    10|
#     +--+------+
graph.degrees.filter("id = 1").show()

# Find the number of incoming links to Andrew
#      +--+--------+
#      |id|inDegree|
#      +--+--------+
#      | 1|       5|
#      +--+--------+
graph.inDegrees.filter("id = 1").show()

# Find the number of links coming out from Andrew using the outDegrees
#      +--+---------+
#      |id|outDegree|
#      +--+---------+
#      | 1|        5|
#      +--+---------+
graph.outDegrees.filter("id = 1").show()

#####################################################################
# Recipe 9-2. Apply Triangle Counting in a GraphFrame
#####################################################################

# - Find how many triangle relationships the vertex is participating in
#
#     +-----+---+-------+---+
#     |count| id| Name  |Age|
#     +-----+---+-------+---+
#     |    3|  1| Andrew| 45|
#     |    1|  6| Rachel| 32|
#     |    1|  3|    Bob| 12|
#     |    0|  5|William| 35|
#     |    1|  4|  Emily| 10|
#     |    3|  2| Sierra| 43|
#     +-----+---+-------+---+
#
# - A vertex is part of a triangle when it has two adjacent vertices with an 
#   edge between them. For example, Andrew has 3 triangle count.
#   + Andrew - Sierra - Bob
#   + Andrew - Emily - Bib
#   + Andrew - Sierra - Emily
# - A new column count is added in the output that represents the triangle count.
#   + The output shows that Andrew and Sierra have the maximum triangle counts, 
#     since they are involved in 3 kinds of relationships
#     - Andrew as father, friend, and husband and Sierra as mother, 
#       friend, and wife. 
personsTriangleCountDf = graph.triangleCount()
personsTriangleCountDf.show()

# Create a "personsTriangleCount" SQL table from the 
# personsTriangleCountDf DataFrame
personsTriangleCountDf.createOrReplaceTempView("personsTriangleCount")

# Create a "personsMaxTriangleCount" SQL table from the
# maxCountDf DataFrame
#
#     +---------+
#     |max_count|
#     +---------+
#     |        3|
#     +---------+
# - Practice SQL Online
#
maxCountDf = spark.sql("select max(count) as max_count from personsTriangleCount")
maxCountDf.createOrReplaceTempView("personsMaxTriangleCount")

# - Join  with the Persons DataFrame to be able to
#   view the person’s details
# - This is the output
#    +-----+---+------+---+---------+
#    |count| id| Name |Age|max_count|
#    +-----+---+------+---+---------+
#    |    3|  1|Andrew| 45|        3|
#    |    3|  2|Sierra| 43|        3|
#    +-----+---+------+---+---------+
    
spark.sql("select * from personsTriangleCount P JOIN (select * from personsMaxTriangleCount) M ON (M.max_count = P.count) ").show()


#####################################################e#
# Recipe 9-3. Apply a PageRank Algorithm
#######################################################

# PageRank Theory (more info)
#
# >>> pageRank
# GraphFrame(v:[id: int, Name: string ... 2 more fields], e:[src:
# int, dst: int ... 2 more fields])
# - maxIter: Run PageRank for a fixed number of iterations
# - resetProbability: The random reset probability (alpha)
#   + The lower it is, the bigger the score spread between
#     the winners and losers will be
#     – valid ranges are from 0 to 1. Usually, 0.15 is a good score
# - Formula: Damping factor = 1 - resetProbability
pageRank = graph.pageRank(resetProbability=0.20, maxIter=10)

# - You can see from the original persons schema that a new column
#   has been added called pagerank.
# - This column is added by Spark and indicates the pageRank score
#   for the vertex.
#
#     root
#      |-- id: integer (nullable = true)
#      |-- Name: string (nullable = true)
#      |-- Age: integer (nullable = true)
#      |-- pagerank: double (nullable = true)
#
pageRank.vertices.printSchema()

# - Let’s look at the PageRank score for each vertex and the weight
#   for each of the edges.
# - We are going to order the PageRank in descending order so that
#   we can see the most connected person in the family based on
#   the links with the other family members.
#
#     +--+-------+----+------------------+
#     |id|   Name| Age|          pagerank|
#     +--+-------+----+------------------+
#     | 1| Andrew| 45 | 1.787923121897472|
#     | 2| Sierra| 43 | 1.406016795082752|
#     | 6| Rachel| 32 |0.7723665979473922|
#     | 4|  Emily| 10 |0.7723665979473922|
#     | 3|    Bob| 12 |0.7723665979473922|
#     | 5|William| 35 |0.4889602891776001|
#     +--+-------+----+------------------+
# - You can see from this output that Andrew is the most connected person.
pageRank.vertices.orderBy("pagerank",ascending=False).show()


# - Let’s look at the weight contributed by each of the edges.
#   + Here we are listing all the edges in descending order so
#     that the maximum weight is listed first.
#   + Edge weights change the relative value that each link contributes.
#     - By default, all edges are given a uniform value of one.
#     - We can use this attribute to pass less value through certain edge types.
#     - Edge-weighted personalized PageRank .
#     - In the random surfer model, an edge with a larger weight is more likely
#       to be selected by the surfer.
#     - Edge-based Local Push for Personalized PageRank
#     - Constructing weighted TF regulatory network
#     - Personalized PageRank with Edge Weights
#
# - From the output.
#
#       +---+---+--------+------+
#       |src|dst|relation|weight|
#       +---+---+--------+------+
#       |  5|  1|  Friend|   1.0|
#       |  3|  1|     Son|   0.5|
#       |  4|  1|Daughter|   0.5|
#       |  4|  2|Daughter|   0.5|
#       |  6|  1|  Friend|   0.5|
#       |  3|  2|     Son|   0.5|
#       |  6|  2|  Friend|   0.5|
#       |  2|  3|  Mother|  0.25|
#       |  2|  4|  Mother|  0.25|
#       |  2|  1|    Wife|  0.25|
#       |  2|  6|  Friend|  0.25|
#       |  1|  2| Husband|   0.2|
#       |  1|  6|  Friend|   0.2|
#       |  1|  3|  Father|   0.2|
#       |  1|  4|  Father|   0.2|
#       |  1|  5|  Friend|   0.2|
#       +---+---+--------+------+
#
#   + You can identify from the output that the edge 5, 1, Friend
#     gets the maximum weightage.
#     - William’s relationship with Andrew gets the maximum weight
#       since it is unique.
#   + No one other than Andrew is a friend to William.
pageRank.edges.orderBy("weight",ascending=False).show()


#######################################################
# Recipe 9-4. Apply the Breadth First Algorithm
#######################################################

# - Use Breadth First Search to find the shortest path
#   between William and Bob
#   + fromExpr: Expression to identify the from vertex.
#   + toExpr: Expression to identify the vertex.
# - From this code notice that we are calling the bfs method with
#   + fromExpr = "Name='Bob'"
#   + toExpr = "Name='William'"
# - Here is the output
#
#     +------------+-----------+---------------+--------------+----------------+
#     |        from|         e0|             v1|            e1|              to|
#     +------------+-----------+---------------+--------------+----------------+
#     |[3, Bob, 12]|[3, 1, Son]|[1, Andrew, 45]|[1, 5, Friend]|[5, William, 35]|
#     +------------+-----------+---------------+--------------+----------------+
#
# - You can replace people’s names with city names and find the shortest distance.
graph.bfs(fromExpr = "Name='Bob'",toExpr = "Name='William'").show()


# - We modified the expressions so that we are looking for all people
#   younger than 20 to find ways to connect to Rachel.
# - Here is the output:
#
#     +--------------+----------------+---------------+--------------+---------------+
#     |          from|              e0|             v1|            e1|             to|
#     +--------------+----------------+---------------+--------------+---------------+
#     |  [3, Bob, 12]|     [3, 1, Son]|[1, Andrew, 45]|[1, 6, Friend]|[6, Rachel, 32]|
#     |  [3, Bob, 12]|     [3, 2, Son]|[2, Sierra, 43]|[2, 6, Friend]|[6, Rachel, 32]|
#     |[4, Emily, 10]|[4, 1, Daughter]|[1, Andrew, 45]|[1, 6, Friend]|[6, Rachel, 32]|
#     |[4, Emily, 10]|[4, 2, Daughter]|[2, Sierra, 43]|[2, 6, Friend]|[6, Rachel, 32]|
#     +--------------+----------------+---------------+--------------+---------------+
#
# - Notice that Bob and Emily are both listed in the output.
#   + Since Rachel is a friend to both Andrew and Sierra, they are the
#     vertex between Bob and Emily.
#   + Bob and Emily need to go through either Andrew or Sierra to
#     be able to connect to Rachel.
graph.bfs(fromExpr = "age < 20", toExpr = "name = 'Rachel'").show()


# - If you want to restrict some of the paths
#   + Let’s say you want the kids to only go through the parents,
#     then you can use the edgeFilter to determine through which
#     relationships Bob and Emily can connect to Rachel.
# - The following code shows the usage of the edgeFilter attribute.
#   + We are going to say that only the daughter is allowed in the results.
# - The code uses the edgeFilter attribute to filter
#   out the edges while identifying the shortest paths.
# - Here is the output that shows how Emily can connect to Rachel:
#
#     +--------------+----------------+---------------+--------------+---------------+
#     |          from|              e0|             v1|            e1|             to|
#     +--------------+----------------+---------------+--------------+---------------+
#     |[4, Emily, 10]|[4, 1, Daughter]|[1, Andrew, 45]|[1, 6, Friend]|[6, Rachel, 32]|
#     |[4, Emily, 10]|[4, 2, Daughter]|[2, Sierra, 43]|[2, 6, Friend]|[6, Rachel, 32]|
#     +--------------+----------------+---------------+--------------+---------------+
graph.bfs(fromExpr = "age < 20", toExpr = "name = 'Rachel'", edgeFilter = "relation != 'Son'").show()
