from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime
from airflow.decorators import dag, task
import sys
import subprocess

sys.dont_write_bytecode = True
######################################## USER CHOOSEN PARAMETERS ########################################
default_args = {
  'topic' : 'iot-preprocess',    # <<< *** Separate multiple topics by a comma - Viperviz will stream data from these topics to your browser
  'secure': 1,   # <<< *** 1=connection is encrypted, 0=no encryption
  'vipervizport' : 9005,   # <<< *** Port where viperviz is listening
  'offset' : -1,    # <<< *** -1 indicates to read from the last offset always
  'append' : 0,   # << ** Do not append new data in the browser
  'chip' : "amd64", # << ** windows/linux=amd64, MAC/linux=arm64   
  'rollbackoffset' : 500, # *************** Rollback the data stream by rollbackoffset.  For example, if 500, then Viperviz wll grab all of the data from the last offset - 500
  'start_date': datetime (2024, 6, 29),   # <<< *** Change as needed   
  'retries': 1,   # <<< *** Change as needed   
    
}

######################################## DO NOT MODIFY BELOW #############################################

# Instantiate your DAG
@dag(dag_id="tml_system_step_7_kafka_visualization_dag_myawesometmlproject4", default_args=default_args, tags=["tml_system_step_7_kafka_visualization_dag_myawesometmlproject4"], schedule=None,catchup=False)
def startstreaming():    
    

  @task(task_id="startstreamingengine")  
  def startstreamingengine():
        chip = default_args['chip']
        vipervizport = default_args['vipervizport']
       
        ti.xcom_push(key='VIPERVIZPORT',value=vipervizport)
        # start the viperviz on Vipervizport
        # STEP 5: START Visualization Viperviz 
        subprocess.run(["tmux", "new", "-d", "-s", "visualization-viperviz"])
        subprocess.run(["tmux", "send-keys", "-t", "visualization-viperviz", "'cd /Viperviz'", "ENTER"])
        subprocess.run(["tmux", "send-keys", "-t", "visualization-viperviz", "'/Viperviz/viperviz-linux-{} 0.0.0.0 {}'".format(chip,vipervizport), "ENTER"])  

  startstreamingengine()      
        
dag = startstreaming()
