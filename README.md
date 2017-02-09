# Titanic
The classic Titanic data analytics project using Spark.
CS 5304 HW1

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

* plot.ly layout: https://www.reddit.com/r/IPython/comments/3tibc8/tip_on_how_to_run_plotly_examples_in_offline_mode/?st=iyytvw2o&sh=3b58b433
