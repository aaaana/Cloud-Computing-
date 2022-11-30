# Description

<img width="500" alt="image" src="https://user-images.githubusercontent.com/93315926/194803849-7c4c723f-81a1-48ef-b068-12dd25496823.png">

# Design

* Step 1: Generate an input file to the Pi MapReduce program
    * Step 1.1: Create a regular Java program which accepts two command line arguments.
    * R: The radius
    * N: The number of (x, y) pairs to create
    The Java program then randomly generates N pairs of (x, y) and displays them on the standard output.
  Step 1.2: Run the program created in Step 1.1 and save the result in a file. The file is the input to Step 2's Pi MapReduce program.

* Step 2: Create a MapReduce program to calculate the numbers of inside darts and outside darts.
* Step 3: Use the file generated in Step 1.2 as the input to execute the MapReduce program created in Step 2
* Step 4: Calculate Pi in the driver program based on the numbers of inside darts and outside darts.

# Implement

## Requirment

* GCP Environment
<img width="600" alt="image" src="https://user-images.githubusercontent.com/93315926/194799644-6b303972-e90e-4fc4-821b-0b26e2df9a6d.png">

* Hadoop environment
<img width="600" alt="image" src="https://user-images.githubusercontent.com/93315926/194799724-14031ad3-43db-4f36-a668-faf70a279365.png">

* Java environment

## Prepare input data
```
  $ mkdir PiCalculation
  $ cd PiCalculation
  $ vi GenerateRandomNumbers.java
  $ javac GenerateRandomNumbers.java
  $ java -cp . GenerateRandomNumbers
```

Input data will store in PiCalculationInput

## Setup passphraseless ssh
Now check that you can ssh to the localhost without a passphrase:
```
  $ cd hadoop-3.3.4/
  $ ssh localhost
```
If you cannot ssh to localhost without a passphrase, execute the following commands:
```
  $ ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
  $ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
  $ chmod 0600 ~/.ssh/authorized_keys
```

## Make the HDFS directories required to execute MapReduce jobs(Copy input data to HDFS)
```
  $ cd ..
  $ cd hadoop-3.3.4/
  $ bin/hdfs namenode -format
  $ sbin/start-dfs.sh
  $ wget http://localhost:9870/
  $ bin/hdfs dfs -mkdir /user
  $ bin/hdfs dfs -mkdir /user/rpan
  $ bin/hdfs dfs -mkdir /user/rpan/picalculate
  $ bin/hdfs dfs -mkdir /user/rpan/picalculate/input
  $ bin/hdfs dfs -put ../PiCalculation/PiCalculationInput /user/rpan/picalculate/input
```
> If you can not copy input into hadoop dictionary, please restart the virtual machine.

## Prepare code

* Build PiCalculation java file
```
  $ cd /hadoop-3.3.4
  $ vi PiCalculation.java      
```

* Compile PiCalculation.java and create a jar
```
  $ bin/hadoop com.sun.tools.javac.Main PiCalculation.java
  $ jar cf wc.jar PiCalculation*class  
```

## Run

* Execute
```
  $ bin/hadoop jar wc.jar PiCalculation /user/rpan/calculate/input /user/rpan/picalculate/output4
```

* Output
```
  $ bin/hdfs dfs -ls /user/rpan/picalculate/output4
  $ bin/hdfs dfs -cat /user/rpan/picalculate/output4/part-r-00000 
```

* Stop
```
  $ sbin/stop-dfs.sh
```

## Test Result

Test Case:

How many random numbers to generate: 1000000
Radius = 200

<img width="700" alt="image" src="https://user-images.githubusercontent.com/93315926/194802159-668eb99d-39c7-4feb-b0ee-1921e827bf41.png">

## Detail Design Presentation
[Pi calculation using MapReduce](https://docs.google.com/presentation/d/1SfhsLRsk71G_YDLw-eBnDyk6nwd0qdZ1rLrxOv_LQGE/edit#slide=id.g25f6af9dd6_0_0)

# References
Chang, H. (2022, 10 09). Overview of Pi Calculation. Overview of Pi Calculation. https://hc.labnet.sfbu.edu/~henry/npu/classes//mapreduce/pi/slide/overview.html   

Strengths and Weaknesses of MapReduce. (2016, September 11). LinkedIn. Retrieved October 10, 2022, from https://www.linkedin.com/pulse/strengths-weaknesses-mapreduce-muazzam-ali 

Taylor, D. (2022, September 17). What is MapReduce in Hadoop? Big Data Architecture. Guru99. Retrieved October 10, 2022, from https://www.guru99.com/introduction-to-mapreduce.html 

Value of Pi in Maths - Definition, Forms & Solved Examples. (n.d.). Byju's. Retrieved October 10, 2022, from https://byjus.com/maths/value-of-pi/  







