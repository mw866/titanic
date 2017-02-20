#  CS 5304 HW1 - Tier 3 Report
By Chris M. Wang (mw866@cornell.edu)

## Requirement 1: A maximum 1-page discussion of the value of this assignment.

### Why would we assign it? 
Titanic is the basic problem for Machine Learning. And it is relatively easy as the starter project on Spark.
### What value should you obtain from it? 
It has helped me to better understand the following important concepts:
* the distributed nature of the Spark/Hadoop
* the compute infrastructure for working with large scale data science projects

### How does this exercise compare with selecting data science tools for a first project at a recently formed Startup company?
Personally, I feel this is better suited for most beginners the the tool selection project. Only after one is familiarized with one tool can he/she assess other tools.

## Requirement 2### 2. A maximum 1-page discussion with suggestions for how we could improve the assignment.
Since this is a starter project, it helps to structure the questions in a concise and linear manner.

## Requirement 3### 3. A maximum 2-page discussion describing how you will build a data science pipeline for analyzing large and small data sets for this course.

I plan to following the following model almost linearly:

1. Select possible relevant features by eliminating obviously irrelevant ones.
2. Index string features to integer values
3. Replace null feature values with approximation or zero
4. Assemble feature columns into feature vectors
5. Measure performance of various ML models on training data
6. Select best performing ML model based on the measured performances
7. Train selected ML model
8. Perform classification/regression/clustering using trained ML model
9. Some manual sanity check


