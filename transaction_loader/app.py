import streamlit as st
import pandas as pd
import os

from load_transactions import *





st.sidebar.markdown("1. Load the file which contains transaction records")
data_file = st.sidebar.file_uploader("Choose a file")
if data_file is not None:
     transactions_df =pd.read_excel(data_file, engine='openpyxl')
     st.markdown("### 1. Loaded Transctions. Below is a snapshot")
     st.write(transactions_df)
     transaction_records = transactions_df.to_dict(orient ='records')
     
     kafka_source_topic_env = os.environ['kafka_source_topic']
     kafka_server_name_env  = os.environ['kafka_server_name']
     kafka_server_port_env  = int(os.environ['kafka_server_port']) 
     kafka_source_groupid_env = os.environ['kafka_source_groupid']
     kafka_linger_ms_env = int(os.environ['kafka_linger_ms'])
     kafka_partitioner_env = os.environ['kafka_partitioner']
          
     st.sidebar.markdown("2.  Kafka Configuration Change  if Required")
     kafka_server_name = st.sidebar.text_input(label='kafka_server_name', value=kafka_server_name_env)
     kafka_server_port = st.sidebar.text_input(label = 'kafka_server_port',value=kafka_server_port_env)
     kafka_linger_ms = st.sidebar.text_input(label = 'kafka_linger_ms',value=kafka_linger_ms_env)
     kafka_client_id = st.sidebar.text_input(label = 'kafka_client_id',value='transactions-1')
     kafka_group_id = st.sidebar.text_input(label = 'kafka_group_id',value=kafka_source_groupid_env)
     
     kafka_partitioner = st.sidebar.text_input(label = 'kafka_partitioner',value=kafka_partitioner_env)
     kafka_topic = st.sidebar.text_input(label = 'kafka_topic',value=kafka_source_topic_env)

     kafka_config = {
          'bootstrap.servers': ":".join([kafka_server_name, kafka_server_port]),
          'linger.ms': int(kafka_linger_ms),
          'client.id': kafka_client_id,
          'partitioner': kafka_partitioner
     }

     st.markdown("### 2. Below  is the default Kafka Configuration Change  if Required")
     st.json(kafka_config)

     st.markdown("### 3.Load Transaction to Kafka")
     records_loaded = False
     if st.button(label="Load Records"):
          load_records_kafka(transaction_records, kafka_config, kafka_source_topic_env, st)
     st.write("Loaded all message to Kafka")