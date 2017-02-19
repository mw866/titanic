# Titanic
The classic Titanic data science project using Spark.
Please refer to './titanic.ipynb' for the compete report.

## Instructions
* Download spark-2.1.0-bin-hadoop2.7

* Install plot.ly using conda in CLI (or Anaconda Navigator in GUI) :


        conda install plotly

* Run Jupyter in a pyspark shell:
https://spark.apache.org/docs/latest/programming-guide.html#using-the-shell


        cd ./titanic
        PYSPARK_DRIVER_PYTHON="jupyter" PYSPARK_DRIVER_PYTHON_OPTS="notebook" "~/Downloads/spark-2.1.0-bin-hadoop2.7/bin/pyspark"


## Reference
* Titatnic tutorial in Python: https://github.com/KaggleCityMo/titanic-tutorial/blob/master/titanic_tutorial_spark16.ipynb

* plot.ly offline plotting: https://plot.ly/python/offline/

* Spark MLlib Guide: http://spark.apache.org/docs/latest/ml-guide.html

* Spark SQL, DataFrames and Datasets Guide: http://spark.apache.org/docs/latest/sql-programming-guide.html

* Spark Python API Reference: http://spark.apache.org/docs/latest/api/python/index.html

* Spark Mlib Evaluation Metrics: https://spark.apache.org/docs/latest/mllib-evaluation-metrics.html


## Troubleshooting
* Unable to extract element from Vectors in DataFrame:
http://stackoverflow.com/questions/37311688/how-to-split-column-of-vectors-into-two-columns

* Null value in test.csv: I154 is empty
