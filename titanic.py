
# coding: utf-8

# In[1]:

get_ipython().magic(u'pylab inline')

import numpy as np
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions
from pyspark.ml.feature import VectorAssembler


# In[2]:

def prepare_data(data):
   ## Fill missing Age values with the average age per class

   explore_age_df = data.orderBy('Age', ascending=True)

   avg_age_df = explore_age_df.where(explore_age_df['Age'].isNotNull()).groupBy('Pclass').avg('Age')
   avg_age_df = avg_age_df.select('Pclass', avg_age_df['avg(Age)'].alias('Age'))

   avg_age_list = avg_age_df.collect()

   # Replace null values with the average age values from our passenger class list
   data_with_age_df = (data
                        .select('*', 
                                when(data['Age'].isNull() & (data['Pclass'] == 1), 
                                     avg_age_list[0].Age)
                                .otherwise(when(data['Age'].isNull() & (data['Pclass'] == 2), 
                                                avg_age_list[1].Age)
                                           .otherwise(when(data['Age'].isNull() & (data['Pclass'] == 3), 
                                                           avg_age_list[2].Age)
                                                      .otherwise(col('Age')))).alias('FilledAge')))

   # Replace the Age column values with those from our FilledAge column and then drop FilledAge.
   data_with_age_df = data_with_age_df.withColumn('Age', data_with_age_df['FilledAge']).drop('FilledAge')

   ## Index Sex

   def sex_to_int(sex):
     if(sex.lower() == 'male'):
       return 0
     else:
       return 1
   sex_classify = functions.udf(sex_to_int, IntegerType())

   sex_int_df = data_with_age_df.select('*', sex_classify(data_with_age_df['Sex']).alias('IntSex'))
   data_sex_indexed_df = sex_int_df.withColumn('Sex', sex_int_df['IntSex']).drop('IntSex').cache()

   data_sex_indexed_df

   ## Index Cabin

   def cabin_to_int(cabin):
       if cabin:
           return ord(cabin[0])-ord('A')+1 #A:1; B:2; C:3; D:4; None:0
       else:
           return 0
   cabin_classify = functions.udf(cabin_to_int, IntegerType())

   cabin_int_df = data_sex_indexed_df.select('*', cabin_classify(data_sex_indexed_df['Cabin']).alias('IntCabin'))
   data_cabin_indexed_df = cabin_int_df.withColumn('Cabin', cabin_int_df['IntCabin']).drop('IntCabin').cache()

   data_cabin_indexed_df

   ##  Index Embarked

   def embarked_to_int(embarked):
       if embarked == 'C':   #Cherbourg; 
           return 1 #TBD
       elif embarked == 'Q': #Queenstown; 
           return 2
       elif embarked == 'S': #Southampton)
           return 3    
       else:
           return 0
   embarked_classify = functions.udf(embarked_to_int, IntegerType())

   embarked_int_df = data_cabin_indexed_df.select('*', embarked_classify(data_sex_indexed_df['Embarked']).alias('IntEmbarked'))
   data_embarked_indexed_df = embarked_int_df.withColumn('Embarked', embarked_int_df['IntEmbarked']).drop('IntEmbarked').cache()

   return data_embarked_indexed_df


# ## Intitialize Train data

# In[3]:

train_data = (sqlContext
                 .read
                 .format('csv')
                 .options(header='true', inferSchema='true')
                 .load('./data/train.csv'))
train_data.cache()
train_data = prepare_data(train_data)
train_data.show(1)


# ## Assemble feature vectors

# In[4]:

assembler = VectorAssembler(
    inputCols=['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked'], outputCol='features'
)

train_data = assembler.transform(train_data).select('PassengerId',col('Survived').alias('label'),'features')
train_data.show(1,truncate=False)


# In[5]:

splits = train_data.randomSplit([0.8, 0.2])
train_train = splits[0].cache() #caching brings significant ~30% perofromance improvement to fitting
train_test = splits[1].cache()
train_train, train_test


# ### Benchmarking various classifiers

# In[6]:

from pyspark.ml.classification import *
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

for classifier in (NaiveBayes, LogisticRegression, RandomForestClassifier, MultilayerPerceptronClassifier): # '[]' won't work
    
    if classifier != MultilayerPerceptronClassifier:
        model = classifier()
    else:
        #Number of inputs = the size of feature vectors. Number of outputs = the total number of labels.
        features_size = train_train.select("features").first()[0].size
        model = classifier(layers=[features_size,10,2]) 
    model_trained = model.fit(train_train)

    train_test_predicted = model_trained.transform(train_test)

    evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction") 
    accuracy = evaluator.evaluate(train_test_predicted, {evaluator.metricName: "accuracy"}) # f1|weightedPrecision|weightedRecall|accuracy
    print(""+classifier.__name__.ljust(30) + '\t' + str(accuracy))
#     test_predicted.show(10)

#     print('Wrong predictions for error analysis')
#     test_predicted.filter(test_predicted['prediction'] != test_predicted['label']).show(5)


# ## Working on Test data

# In[7]:

test_data = (sqlContext
                 .read
                 .format('csv')
                 .options(header='true', inferSchema='true')
                 .load('./data/test.csv'))
test_data.cache()
test_data.show(5)

test_data = prepare_data(test_data)
test_data


# In[8]:

test_assembler = VectorAssembler(
    inputCols=['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked'], outputCol='features'
)

test_data = test_assembler.transform(test_data).select('PassengerId','features')
test_data.show(1,truncate=False)


# ### Proceed with Random Forest

# In[9]:

rf_model = RandomForestClassifier()
rf_model_fitted = rf_model.fit(train_data)
rf_model_fitted


# In[10]:

rf_test_predicted = rf_model_fitted.transform(test_data)
rf_test_predicted.show(1,truncate=False)


# In[11]:

rf_test_predicted.select("PassengerId", col("prediction").alias('Survived')).write.csv("output",mode='overwrite',header=True)


# ### Cluster most probabable survivors

# In[12]:

def extract_survival_prob(probability):
    return probability.values[1].item() 

extract_survival_prob_udf = functions.udf(extract_survival_prob, FloatType())

survival_prob_udf_df = rf_test_predicted.select('*', extract_survival_prob_udf(rf_test_predicted['probability']).alias('survival_prob_udf'))
# survival_prob_udf_df.show(1)

survival_prob_df = survival_prob_udf_df.withColumn('probability', survival_prob_udf_df['survival_prob_udf']).drop('survival_prob_udf').cache()
survival_prob_df.show(1)


# In[13]:

likely_survivors_df = survival_prob_df.filter("probability > 0.8")

likely_survivors_df=likely_survivors_df.drop('probability','rawPrediction','prediction')
likely_survivors_df.show(5)


# In[14]:

from pyspark.ml.clustering import GaussianMixture

gmm = GaussianMixture().setK(2).setSeed(607262)
gmm_model = gmm.fit(likely_survivors_df)
print assembler.getInputCols()
gmm_model.gaussiansDF.select('mean').show(5, truncate=False)
# gmm_model.gaussiansDF.write.csv("output")


# In[15]:

gmm_model.weights


# In[16]:

gmm_model.summary.clusterSizes


# In[ ]:



