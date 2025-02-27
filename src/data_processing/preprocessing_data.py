import sys
import boto3
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import SparkSession
from awsglue.job import Job
import pandas as pd

def preprocessing() :
	data = pd.read_csv("s3://project-real-estate/New_dataset1.csv")
	df=data.drop(['Unnamed: 0'],axis=1)
# Split single column into two columns use apply()
	df[['Bedrooms','Bathrooms','Surface']] = df["Category"].apply(lambda x: pd.Series(str(x).split("\n")))
	df1=df.dropna()
	df1['Bedrooms'] = df1['Bedrooms'].str.replace(r'bedrooms', '')
	df1['Bathrooms'] = df1['Bathrooms'].str.replace(r'bathrooms', '')
	df1['Bedrooms'] = df1['Bedrooms'].str.replace(r'bedroom', '')
	df1['Bathrooms'] = df1['Bathrooms'].str.replace(r'bathroom', '')
	df1['Surface'] = df1['Surface'].str.replace(r'm²', '')
	df1['Price'] = df1['Price'].str.replace(r'MAD', '')
	columns = ['Surface','Price']
	for i in columns :
    		df1[i] = df1[i].str.replace(r'\u202f', '')
	df1 = df1[df1.Price != 'Demande de prix']
	df1['Price'] = df1['Price'].astype(int)
	df1['Surface'] = df1['Surface'].astype(int)
	df1['Bathrooms'] = df1['Bathrooms'].astype(int)
	df2 = df1[df1['Bedrooms'] != 'Studio']
	df2['Bedrooms'] = df2['Bedrooms'].astype(int)
# Split single column into two columns use apply()
	df2[['Neighborhood', 'City']] = df2['Location'].str.split(', ', 1, expand=True)
	df3=df2.drop(["Location",'Category'],axis=1)
	return df3


args = getResolvedOptions(sys.argv, ['JOB_NAME', 'bucket_name', 'file_path'])

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

s3 = args['bucket_name']
file_path = args['file_path']

# apply preprocessing function
preprocessed_df = preprocessing()

# save preprocessed data to S3 as a CSV file
preprocessed_df.to_csv(f"s3://{s3}/preprocessed_data.csv", index=False)


## Commit the job and exit
job.commit()