from __future__ import annotations

import pendulum
from airflow.decorators import task
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor 
import tsslogging
import os
from datetime import datetime

# TML Solution template for processing
# Use this DAG to start processing data with:
# 1. visualization
# 2. containerization
# 3. documentationa


with DAG(
    dag_id="solution_preprocessing_ml_ai_restapi_dag",
    start_date=datetime(2023, 1, 1),
    schedule=None,
) as dag:
  start_task = BashOperator(
    task_id="start_tasks_tml_preprocessing_ml_ai",
    bash_command="echo 'Start task'",
  )
# STEP 1: Get the Parameters
  sensor_A = ExternalTaskSensor(
      task_id="solution_task_getparams",
      external_dag_id="tml_system_step_1_getparams_dag",
      external_task_id="getparams",
  )
# STEP 2: Create the Kafka topics
  sensor_B = ExternalTaskSensor(
      task_id="solution_task_createtopic",
      external_dag_id="tml_system_step_2_kafka_createtopic_dag",
      external_task_id="setupkafkatopics",
  )
# STEP 3: Produce data to topic        
  sensor_C = ExternalTaskSensor(
      task_id="solution_task_producetotopic",
      external_dag_id="tml_read_RESTAPI_step_3_kafka_producetotopic_dag",
      external_task_id="gettmlsystemsparams",
  )
# STEP 4: Preprocess the data        
  sensor_D = ExternalTaskSensor(
      task_id="solution_task_preprocess",
      external_dag_id="tml_system_step_4_kafka_preprocess_dag",
      external_task_id="processtransactiondata",
  )
# STEP 5: ML        
  sensor_E = ExternalTaskSensor(
      task_id="solution_task_ml",
      external_dag_id="tml_system_step_5_kafka_machine_learning_dag",
      external_task_id="performSupervisedMachineLearning",
  )
# STEP 6: Predictions        
  sensor_F = ExternalTaskSensor(
      task_id="solution_task_prediction",
      external_dag_id="tml_system_step_6_kafka_predictions_dag",
      external_task_id="performPredictions",
  )    
# STEP 7: Visualization        
  sensor_G = ExternalTaskSensor(
      task_id="solution_task_visualization",
      external_dag_id="tml_system_step_7_kafka_visualization_dag",
      external_task_id="startstreamingengine",
  )
# STEP 8: Containerize the solution        
  sensor_H = ExternalTaskSensor(
      task_id="solution_task_containerize",
      external_dag_id="tml_system_step_8_deploy_solution_to_docker_dag",
      external_task_id="dockerit",
  )
# STEP 9: PrivateGPT      
  sensor_I = ExternalTaskSensor(
      task_id="solution_task_ai",
      external_dag_id="tml_system_step_9_privategpt_qdrant_dag",
      external_task_id="startprivategpt",
  )            
# STEP 10: Document the solution
  sensor_J = ExternalTaskSensor(
      task_id="solution_task_document",
      external_dag_id="tml_system_step_10_documentation_dag",
      external_task_id="generatedoc",
  )

  start_task >> sensor_A >> sensor_B >> [sensor_C, sensor_D, sensor_E, sensor_F, sensor_I, sensor_G, sensor_H] >> sensor_J
