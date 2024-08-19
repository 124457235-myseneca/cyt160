from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.decorators import dag, task
import os 
import sys

sys.dont_write_bytecode = True

######################################################USER CHOSEN PARAMETERS ###########################################################
default_args = {
 'solutionname': 'mysolution',   # <<< *** Provide a name for your solution - No spaces or special characters in the name
 'description': 'This is an awesome real-time solution built by TSS',   # <<< *** Provide a description of your solution
    
    
 'start_date': datetime (2024, 6, 29),   # <<< *** Change as needed   
 'retries': 1,   # <<< *** Change as needed   
}

############################################################### DO NOT MODIFY BELOW ####################################################
# Instantiate your DAG
@dag(dag_id="tml_system_step_10_documentation_dag", default_args=default_args, tags=["tml-system-step-10-documentation-dag"], schedule=None,  catchup=False)
def starttmldeploymentprocess():
    # Define tasks
  basedir = "/"
  viperconfigfile=basedir + "/Viper-produce/viper.env"

  @task(task_id="getparams")
  def getparams():
     VIPERHOST=""
     VIPERPORT=""
     HTTPADDR=""
     with open(basedir + "/Viper-produce/admin.tok", "r") as f:
        VIPERTOKEN=f.read()

     if VIPERHOST=="":
        with open(basedir + '/Viper-produce/viper.txt', 'r') as f:
          output = f.read()
          VIPERHOST = HTTPADDR + output.split(",")[0]
          VIPERPORT = output.split(",")[1]

     ti.xcom_push(key='VIPERTOKEN',value=VIPERTOKEN)
     ti.xcom_push(key='VIPERHOST',value=VIPERHOST)
     ti.xcom_push(key='VIPERPORT',value=VIPERPORT)
     ti.xcom_push(key='HTTPADDR',value=HTTPADDR)
    
     return [VIPERTOKEN,VIPERHOST,VIPERPORT,HTTPADDR]
     
     tmlsystemparams=getparams()
     if tmlsystemparams[1]=="":
        print("ERROR: No host specified")
    
dag = starttmldeploymentprocess()
