# Titanic
The classic Titanic data science project using Spark.
Please refer to './titanic.ipynb' for the compete report.

## Instructions: Setup Local Development Environemtn
* Download spark-2.1.0-bin-hadoop2.7

* Install plot.ly using conda in CLI (or Anaconda Navigator in GUI) :


        conda install plotly

* Run Jupyter in a pyspark shell:
https://spark.apache.org/docs/latest/programming-guide.html#using-the-shell


        cd ./titanic
        PYSPARK_DRIVER_PYTHON="jupyter" PYSPARK_DRIVER_PYTHON_OPTS="notebook" "~/Downloads/spark-2.1.0-bin-hadoop2.7/bin/pyspark"


## Instructions: AWS EMR
* Accessing the Spark Web UIs: http://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-history.html
1. Set up SSH Tunnel
2. Configure  SOCKS Proxy in Browser (using Foxy Proxy)
3. Test the proxy: http://master-public-dns-name/
4. Accesss the Web Interfaces: 
    * Zepplin (Notebook): 8890 
    * Spark (Cluster log): 18080 
    * Ganglia (Monitoring): */ganglia/
    * Hadoop (MapReduce): 8088/cluster

* Install Git on AWS EMR: sudo yum install git-all



## Reference
* Titatnic tutorial in Python: https://github.com/KaggleCityMo/titanic-tutorial/blob/master/titanic_tutorial_spark16.ipynb

* Spark MLlib Guide: http://spark.apache.org/docs/latest/ml-guide.html

* Spark SQL, DataFrames and Datasets Guide: http://spark.apache.org/docs/latest/sql-programming-guide.html

* Spark Python API Reference: http://spark.apache.org/docs/latest/api/python/index.html

* Spark Mlib Evaluation Metrics: https://spark.apache.org/docs/latest/mllib-evaluation-metrics.html

* Spark on AWS EMR: http://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-launch.html

* AWS EMR - Overview: https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-overview.html

* AWS EMR - Upload Data to Amazon S3: http://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-upload-s3.html


## Troubleshooting
* Unable to extract element from Vectors in DataFrame: Using User-defined Functions (UDF)
http://stackoverflow.com/questions/37311688/how-to-split-column-of-vectors-into-two-columns

* Null value in test.csv: I154 is empty

* AWS EMR "Terminated with errorsFailed to provision ec2 instances because 'The requested instance profile EMR_AutoScaling_DefaultRole is invalid'":
Removed EMR_AutoScaling_DefaultRole
https://aws.amazon.com/premiumsupport/knowledge-center/emr-default-role-invalid/

* No output from ssh -i ~/aws_root.pem -ND xxxx: It's expected due to -N (no command)

## Addtional Resourcse
* http://cloudacademy.com/blog/big-data-getting-started-with-amazon-emr-apache-spark-and-apache-zeppelin-part-two-of-two/
* http://cloudacademy.com/blog/big-data-amazon-emr-apache-spark-and-apache-zeppelin-part-one-of-two/

