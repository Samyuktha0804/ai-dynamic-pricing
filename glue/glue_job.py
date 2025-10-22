import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql.functions import col

# Glue job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'input_path', 'output_path'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read raw CSV from S3
df = spark.read.option("header", True).csv(args['input_path'])

# Convert numeric columns
df = df.withColumn("amount", col("amount").cast("double")) \
       .withColumn("demand", col("demand").cast("double")) \
       .withColumn("inventory_level", col("inventory_level").cast("int")) \
       .withColumn("time_of_day", (col("timestamp") % 86400 / 3600).cast("int"))

# Feature engineering: demand/inventory factor
df = df.withColumn("demand_inventory_factor", col("demand") * (1 / (col("inventory_level") + 1)))

# Save processed features back to S3 as CSV
df.write.mode("overwrite").option("header", True).csv(args['output_path'])

job.commit()
