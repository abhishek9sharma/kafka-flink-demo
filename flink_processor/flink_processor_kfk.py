# from dotenv import load_dotenv
# load_dotenv(dotenv_path = '.env')

import os,json
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings,DataTypes
from pyflink.table.udf import udf
import requests
import json
import logging



config = {
   'kafka_source_topic_env' : os.environ['kafka_source_topic'],
   'kafka_server_name_env'  : os.environ['kafka_server_name'],
   'kafka_server_port_env'  : os.environ['kafka_server_port'],
   'kafka_source_groupid_env' : os.environ['kafka_source_groupid'],
   'kafka_linger_ms_env' : int(os.environ['kafka_linger_ms']),
   'kafka_partitioner_env' : os.environ['kafka_partitioner'],     
   'kafka_sink_topic_env'  : os.environ['kafka_sink_topic'],
}

config['kafka_bootstrap_servers'] = ":".join([
    config['kafka_server_name_env'],
    config['kafka_server_port_env']])

ddl_source_table = """
    CREATE TABLE transactions (
        transaction_time_since_first_april_2022_00am_in_seconds BIGINT,
        transaction_amount DOUBLE,
        beneficiary VARCHAR,
        type VARCHAR,
        country VARCHAR,
        proctime AS PROCTIME()
    ) WITH (
        'connector' = 'kafka',
        'topic' = '{}',
        'properties.bootstrap.servers' = '{}',
        'properties.group.id' = '{}',
        'format' = 'json'
    )
""".format(
   config['kafka_source_topic_env'],
   config['kafka_bootstrap_servers'],
   config['kafka_source_groupid_env']
    )


ddl_sink_table = """
    CREATE TABLE fraudsurveillance (
        transaction_time_since_first_april_2022_00am_in_seconds BIGINT,
        transaction_amount DOUBLE,
        beneficiary VARCHAR,
        type VARCHAR,
        country VARCHAR,
        Flag VARCHAR,
        modelprediction VARCHAR
    ) WITH (
        'connector' = 'kafka',
        'topic' = '{}',
        'properties.bootstrap.servers' = '{}',
        'format' = 'json'
    )
""".format(
    config['kafka_sink_topic_env'],
    config['kafka_bootstrap_servers']
       )


def get_streaming_env():
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.new_instance()\
                      .in_streaming_mode()\
                      .use_blink_planner()\
                      .build()

    tbl_env = StreamTableEnvironment.create(stream_execution_environment=env,
                                            environment_settings=settings)
    
    tbl_env.get_config().get_configuration().set_string("execution.checkpointing.interval", "2s")

    # add kafka connector dependency
    kafka_jar = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'flink-sql-connector-kafka_2.11-1.13.0.jar')
    tbl_env.get_config()\
            .get_configuration()\
            .set_string("pipeline.jars", "file://{}".format(kafka_jar))
    
    return tbl_env

def get_prediction_from_svc(svc_url, payload):
    
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", svc_url, headers=headers, data=payload)
    return response

@udf(result_type=DataTypes.STRING())
def get_flag(transaction_amount):
    if transaction_amount>5000:
        return "Scored by Model"
    else:
        return "Greater than 5000"

@udf(result_type=DataTypes.STRING())
def get_prediction_score(
    transaction_time_since_first_april_2022_00am_in_seconds, 
    transaction_amount,
    beneficiary,
    type,
    country):
    prediction = 'UNKNOWN'
    try:
        payload_data = {
            "transaction_time_since_first_april_2022_00am_in_seconds": transaction_time_since_first_april_2022_00am_in_seconds,
            "transaction_amount": transaction_amount,
            "beneficiary": beneficiary,
            "type": type,
            "country": country
        }
        payload = json.dumps(payload_data)
        svc_url = os.environ['svcurl']
   
        resp = get_prediction_from_svc(svc_url, payload)
        respvalue = json.loads(resp.text)
        prediction = respvalue['prediction']
    except Exception as e:
        prediction = 'FAILED with exception {}'.format(e)
    return prediction
   

def main():

    tbl_env = get_streaming_env()

    #Set up source table
    tbl_env.execute_sql(ddl_source_table)
    tbl = tbl_env.from_path('transactions')
    flinklogger.info('Source Schema')
    tbl.print_schema()

    #set up udfs
    tbl_env.create_temporary_function("GETFLAG", get_flag)
    tbl_env.create_temporary_function("GETPREDSCORE", get_prediction_score)


    # set up sink table
    tbl_env.execute_sql(ddl_sink_table)
    
    

    #Insert into Sink
    tbl_env.execute_sql("""
                INSERT INTO fraudsurveillance
                    SELECT  transaction_time_since_first_april_2022_00am_in_seconds, 
                            transaction_amount,
                            beneficiary,
                            type,
                            country,
                            GETFLAG(transaction_amount) as Flag,
                            CASE
                                WHEN transaction_amount > 5000 THEN GETPREDSCORE(transaction_time_since_first_april_2022_00am_in_seconds, 
                                                                        transaction_amount,
                                                                        beneficiary,
                                                                        type,
                                                                        country)
                                ELSE ''
                            END AS modelprediction
                FROM transactions
                """).wait()

if __name__ == '__main__':
    print(os.listdir())
    flinklogger = logging.getLogger('flinklogger')
    flinklogger.info('Starting job ')
    main()
