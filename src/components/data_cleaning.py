import os
import sys
import pandas as pd
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging

@dataclass
class DataCleaningConfig:
    raw_data_path: str=os.path.join('artifacts','data.csv')

class DataCleaning:
    def __init__(self):
        self.cleaning_config = DataCleaningConfig()
    
    def initiate_data_cleaning(self):
        logging.info("Cleaning data")
        try:
            df = pd.read_csv('notebook\data\data.csv')
            pd.set_option('mode.chained_assignment',None)

            df = df[df['Salary Estimate'] != '-1']
            df = df[df['Company Name']!='-1']

            #salary parsing
            df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
            df['employer_provided'] = df['Salary Estimate'].apply((lambda x: 1 if 'employer provided salary' in x.lower() else 0))

            df = df[df['Salary Estimate']!='-1']
            salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
            salary = salary.apply(lambda x: x.replace('$','').replace('K','').replace('.00',''))
            salary = salary.apply(lambda x: x.lower().replace('employer provided salary:','').replace('per hour',''))
            df['min_salary'] = salary.apply(lambda x: int(x.split('-')[0]))
            df['max_salary'] = salary.apply(lambda x: int(x.split('-')[1]))
            df['avg_salary'] = (df['min_salary'] + df['max_salary'])/2

            #Company name text
            df['company_text'] = df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-4],axis=1)

            #state field
            df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1] if ',' in x else 'Remote')

            #age of company
            df['age'] = df['Founded'].apply(lambda x:2023 - x)

            #parsing of job description (python,etc.)
            #python
            df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
            #r studio
            df['r_yn'] = df['Job Description'].apply(lambda x: 1 if 'r-studio' in x.lower() else 0)

            #spark
            df['spark_yn'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)

            #aws
            df['aws_yn'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)

            #excel
            df['excel_yn'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

            df.to_csv(self.cleaning_config.raw_data_path,index=False,header=True)
            logging.info("Cleaning data is completed")
        except Exception as e:
            raise CustomException (e,sys)

if __name__ == '__main__':
    obj = DataCleaning()
    obj.initiate_data_cleaning()