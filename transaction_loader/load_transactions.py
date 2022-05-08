import atexit
import json
import logging
import os
import random
import time
import sys





from logutils import set_logger
msglogger = set_logger('transaction_load_logger')
from confluent_kafka import Producer

class ProducerCallback:
    def __init__(self, ix, record, log_success=False):
        self.ix = ix
        self.record = record
        self.log_success = log_success
        

    def __call__(self, err, msg):
        if err:
            mslogger.error('Error producing record {}'.format(self.record))
        elif self.log_success:
            msglogger.info('Produced {} with indwex {} to topic {} partition {} offset {}'.format(
                self.record,
                self.ix,
                msg.topic(),
                msg.partition(),
                msg.offset()
            ))


def load_records_kafka(transaction_records, kafka_config, kafka_topic, st):

    
    kafka_producer = Producer(kafka_config)
    atexit.register(lambda p: p.flush(), kafka_producer)
    st.write("{} records to load".format(len(transaction_records)))
    
    for ix, record in enumerate(transaction_records):
        log_flag = ix%50==0
        kafka_producer.produce(topic=kafka_topic,
                        value=json.dumps(record),
                        on_delivery=ProducerCallback(ix, record, log_success=True))

        if log_flag:
            kafka_producer.poll(1)
            time.sleep(3)
        if ix%50==0:
            loginfo = "Loaded {} records".format(ix+1)
            msglogger.info(loginfo)
            st.write(loginfo)
    st.write("{} records Loaded".format(len(transaction_records)))