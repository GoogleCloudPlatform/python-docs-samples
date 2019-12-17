import pyspark
sc = pyspark.SparkContext()
rdd = sc.parallelize((1,2,3,4,5)
sum = rdd.reduce(lambda x, y: x + y)
