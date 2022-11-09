#########################################################################
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#########################################################################

"""
This is an example implementation of PageRank. For more conventional use,
Please refer to PageRank implementation provided by graphx

Example Usage:
spark-submit examples/src/main/python/pagerank.py hdfs:///mydata/pagerank_data.txt 1
"""

import re
import sys
from operator import add
from pyspark.sql import SparkSession
def computeContribs(urls, rank):
    """Calculates URL contributions to the rank of other URLs."""
    num_urls = len(urls)
    for url in urls:
        yield (url, rank / num_urls)


def parseNeighbors(urls):
    """Parses a urls pair string into urls pair."""
    parts = re.split(r'\s+', urls)
    return parts[0], parts[1]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: pagerank <file> <iterations>", file=sys.stderr)
        sys.exit(-1)

    print("WARN: This is a naive implementation of PageRank and is given as an example!\n" +
          "Please refer to PageRank implementation provided by graphx",
          file=sys.stderr)

    # Initialize the spark context.
    spark = SparkSession\
        .builder\
        .appName("PythonPageRank")\
        .getOrCreate()

    ####################################################
    # Loads in input file. For example,
    #     argv[1] = data/mllib/pagerank_data.txt
    #
    # It should be in format of:
    #     URL         neighbor-URL
    #     URL         neighbor-URL
    #     URL         neighbor-URL
    # Thus,
    #
    #   + Physically, the file contains these line format.
    #          B C
    #          B A
    #          C A
    #          D A
    #          D B
    #          D C
    #          ...
    #     The lines are stored in the RDD "lines"
    #             r[0]
    #          +-------+
    #        0 |  B C  |
    #          +-------+
    #        1 |  B A  |
    #          +-------+
    #        2 |  C A  |
    #          +-------+
    #        3 |  D A  |
    #          +-------+
    #        4 |  D B  |
    #          +-------+
    #        5 |  D C  |
    #          +-------+
    #            ...
    ####################################################
    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])

    ####################################################
    # Loads all URLs from input file and initialize their neighbors.
    #
    #   + "links" contains the list of neighbors of each page,
    #     (pageID, linkList)
    #          (B (C,A))
    #          (C (A))
    #          (D (A,B,C))
    ####################################################
    links = lines.map(lambda urls: parseNeighbors(urls)
                      ).distinct().groupByKey().cache()

    ####################################################
    # Loads all URLs with other URL(s) link to from input file and
    # initialize ranks of them to one.
    #
    # - Initialize each page's rank to 1.0; since we use mapValues,
    #   the resulting RDD will have the same partitioner as links
    #       PR(A)=PR(B)=PR(C)=PR(D)=1
    #
    # - ranks contains the current rank for each page: (pageID, rank):
    #      (B 1)
    #      (C 1)
    #      (D 1)
    ####################################################
    ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))

    #########################################################################
    # Calculates and updates URL ranks continuously using PageRank algorithm.
    #     argv[2] = 10
    #########################################################################
    for iteration in range(int(sys.argv[2])):
        #####################################################################
        # Calculates URL contributions to the rank of other URLs.
        #
        # Step 1: Obtain the link list and rank for each  page ID
        #         by joining between the current ranks RDD and the
        #         static links RDD.
        #
        #             links.join(ranks)
        #
        #         Iteration 0
        #
        #           WebPage   Links       PageRank
        #           ---------------------------------
        #              (B     (C,A          1))
        #              (C     (A            1))
        #              (D     (A,B,C        1))
        #
        # Step 2: Apply flatMap to the ouput of join to create “contribution”
        #         values to send to each of the page’s neighbors.
        #
        #              Dest WebPage      Contributed (i.e., received) PageRank
        #           -----------------------------------------------------------
        #               C                    0.5
        #               A                    0.5
        #               A                    1.0
        #               A                    0.33
        #               B                    0.33
        #               C                    0.33
        #
        #####################################################################
        contribs = links.join(ranks).flatMap(
            lambda url_urls_rank: computeContribs(url_urls_rank[1][0], url_urls_rank[1][1]))

        #####################################################################
        # Step 3: Re-calculates URL ranks based on neighbor contributions.
        #
        #         Add up "contribution" values by dest webpage (i.e. by the page
        #         receiving the contribution) and set that page’s
        #         rank to 0.15 + 0.85 * contributionsReceived.
        #
        #           A = (0.5 + 1.0  + 0.33) * 0.85 + 0.15
        #           B = 0.33 * 0.85 + 0.15
        #           C = (0.5 + 0.33) * 0.85 + 0.15
        #
        #####################################################################
        ranks = contribs.reduceByKey(add).mapValues(
            lambda rank: rank * 0.85 + 0.15)

    # Collects all URL ranks and dump them to console.
    for (link, rank) in ranks.collect():
        print("%s has rank: %s." % (link, rank))

    spark.stop()
