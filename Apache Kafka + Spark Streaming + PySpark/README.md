# Kafka QuickStart - Apache Kafka + Kafka - Python 
## Download kafka
[Download link](https://kafka.apache.org/downloads)

## Start zookeeper, unzip it, and get into the folder
```
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```
## Starting Kafka Brokers
* Create another terminal, do not close zookeeper
```
$ bin/kafka-server-start.sh config/server.properties
```

## Creating Kafka Topics. Create another terminal, do not close zookeeper and kafka broker
```
$ bin/kafka-topics.sh --create --topic input_recommend_product --zookeeper localhost:2181 --partitions 3 --replication-factor 1
```

* if encountering some erros, try below:
```
$ bin/kafka-topics.sh --create --topic input_recommend_product --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

## Creating Producer and Consumer using Kafka-python
```
$ producer.py
$ consumer.py
```

## Run code
* Run consumer.py first 
```
$ python consumer.py
```
* Use a new terminal to run producer.py
```
$ python producer.py
```
* Back to consumer terminal to check the result
