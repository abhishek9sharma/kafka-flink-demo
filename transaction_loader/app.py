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
     #st.write(transaction_records[0:10])
     #transaction_records = transaction_records[0:200]
     
     st.sidebar.markdown("2.  Kafka Configuration Change  if Required")
     kafka_server_name = st.sidebar.text_input(label='kafka_server_name',value='broker')
     kafka_server_port = st.sidebar.text_input(label = 'kafka_server_port',value='29092')
     kafka_linger_ms = st.sidebar.text_input(label = 'kafka_linger_ms',value='200')
     kafka_client_id = st.sidebar.text_input(label = 'kafka_client_id',value='transactions-1')
     kafka_partitioner = st.sidebar.text_input(label = 'kafka_partitioner',value='murmur2_random')
     kafka_topic = st.sidebar.text_input(label = 'kafka_topic',value='transactions')

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
          load_records_kafka(transaction_records, kafka_config, kafka_topic, st)
     st.write("Loaded all message to Kafka")