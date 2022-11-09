# 1 .PageRank Theory

1. If the initial PageRank value for each webpage is 1.

PR(A)= 1

PR(B)= 1

PR(C)= 1

Page B has a link to pages C and A. 

Page C has a link to page A. 

Page D has a link to all the three pages. 


Then

A's PageRank is :PR(A)=( 1 - d)+d*(PR(B)/ 2 +PR(C)/ 1 +PR(D)/ 3 )

B's PageRank is: PR(B)=( 1 - d)+d*(PR(D)/ 3 )

C's PageRank is: PR(C)=( 1 - d)+d*(PR(B)/ 2 +PR(D)/ 3 )

D's PageRank is: PR(D)= 1 - d

Damping factor is 0. 85

Then after 1st iteration

Page B would transfer half of its existing value, or 0.5, to page A and the other half, or 0.5, to page C.

Page C would transfer all of its existing value, 1, to the only page it links to, A.

Since D had three outbound links, it would transfer one third of its existing value, or approximately 0.33, to A.

PR(A)= (1-d) + d * (PR(B) / 2 + PR(C) / 1 + PR(D) / 3) = (1-0.85) + 0.85 * (0.5 + 1 + 0.33) = 1.71

PR(B)= (1-d) + d * (PR(D) / 3)= (1-0.85) + 0.85 * 0.33 = 0.43

PR(C)= (1-d) + d * (PR(B) / 2 + PR(D) / 3)= (1-0.85) + 0.85 * (0.5 + 0.33)= 0.86

PR(D)= 1-d= 0.15

# 2. Set up Google Cloud

Go to Menu bar->select Dataproc->Clusters->create cluster->cluster on compute engine->create

Connecting to the Master Node using SecureShell(ssh)

```
rpan@cluster- 8 bc 7 - m:~$hdfsdfs-mkdirhdfs:////mydata
downloadasamplefileandsaveittothemydatadirectory.
rpan@cluster- 8 bc 7 - m:~$curl
[http://optionsdata.baruch.cuny.edu/data](http://optionsdata.baruch.cuny.edu/data) 1 /delivery/data/trades_sample_heade
r.csv|hdfsdfs-put-hdfs:///mydata/trades_sample_header.csv
rpan@cluster- 8 bc 7 - m:~$hdfsdfs-lshdfs:///mydata

curpan@cluster- 8 bc 7 - m:~$curl
[http://optionsdata.baruch.cuny.edu/data](http://optionsdata.baruch.cuny.edu/data) 1 /delivery/data/text_file.txt|hdfsdfs

- put-f - hdfs:///myfiles/text_file.txt
```
# 3 .PageRank +PySpark+ GCP

## 3. 1 Setup PySpark onGCP
## 3. 2 Calculate PageRank manually

Iteration PR(A) PR(B) PR(C)

Create the PageRank using PySpark

Manual input data

vipagerank_data.txt

Data

A B

A C

B C

C A


## 3. 3 Result


Result for first iteration:

Second Iteration:

Result for second iteration:

10 times iteration:


Result:

# 4 .PageRank +Scala + GCP

## 4. 1 Setup Scala on GCP

install scala
```
$curl-fLhttps://github.com/coursier/launchers/raw/master/cs-x 86 _ 64 - pc-linux.gz|gzip-d>
cs&&chmod+xcs&&./cssetup

$exportSCALA_HOME=/usr/local/share/scala

$exportPATH=$PATH:$SCALA_HOME/
```

## 4. 2 Use Scala

Prepare 
```
spark-shell

```
Firstiteration

Seconditeration:

10 timesiteration:

# 5. Shut down GCP
