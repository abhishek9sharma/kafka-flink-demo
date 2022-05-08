### A simple app to process some transaction using kafka and py-flink


### Steps to run the notebooks/code Used. Run in root mode on Unix Based System

- Install Docker from [here](https://docs.docker.com/get-docker/)

- Navigate to folder `kafka-flink-demo`. Once there run below command

        - you@yourmachine:~/somefolder/kafka-flink-demo$ chmod a+x rundemo.sh  && ./rundemo.sh
        
    If the command runs successfull you should see the below logs when all pods come up
    
        Creating zookeeper     ... done
        Creating predictionapi ... done
        Creating broker        ... done
        Creating flink_processor    ... done
        Creating transaction_loader ... done
        Waiting for Kafka pods to come up
        #######################   
        Kafka started
        Created topic transactions.
        Created topic fraudsurveillance.
        Browse http://localhost:8501/ to load transaction data to Kafka
        Browse http://localhost:5000/docs to see prediction end point
        Once you load data from http://localhost:8501/ the final flat file should be produced in data folder

- If `- you@yourmachine:~/somefolder/kafka-flink-demo/data$` is empty download the file [data_for_ml_ops_test.xlsx]()

        --you@yourmachine:~/somefolder/kafka-flink-demo/data$
            --you@yourmachine:~/somefolder/kafka-flink-demo/data/data_for_ml_ops_test.xlsx

- If `- you@yourmachine:~/somefolder/kafka-flink-demo/models$` is empty copy below files to the models folder

        -- you@yourmachine:~/somefolder/kafka-flink-demo/models$
                --you@yourmachine:~/somefolder/kafka-flink-demo/models/beneficiary.pkl
                --you@yourmachine:~/somefolder/kafka-flink-demo/models/country.pkl
                --you@yourmachine:~/somefolder/kafka-flink-demo/models/model.sav
                --you@yourmachine:~/somefolder/kafka-flink-demo/models/type.pkl

- Go to link [http://localhost:8501/](http://localhost:8501/) and follow the steps to load the messages to Kafka

- Go to [data](/data) folder amf you should see flat files there in below format

        -- you@yourmachine:~/somefolder/kafka-flink-demo/data$
                ├── part-2d870663-cc36-4f3b-a9b7-eb8c0bc21853-11-0
                └── part-2d870663-cc36-4f3b-a9b7-eb8c0bc21853-11-1

- If you use `python3 flink_processor_kfk.py` in  [flink_processor/start.sh](/flink_processor/start.sh) then 

  - Go to console and type below  command : `docker exec -it broker kafka-console-consumer --from-beginning     --bootstrap-server localhost:9092     --topic fraudsurveillance` and you should see something like below
        
        -- you@yourmachine:~/somefolder/kafka-flink-demo  docker exec -it \
                                                          broker kafka-console-consumer \
                                                          --from-beginning     \
                                                          --bootstrap-server localhost:9092     \
                                                          --topic fraudsurveillance
    

        "transaction_time_since_first_april_2022_00am_in_seconds":27,"transaction_amount":11.11,"beneficiary":"Mike","type":"credit_card","country":"France","Flag":"Greater than 5000","modelprediction":""}
        {"transaction_time_since_first_april_2022_00am_in_seconds":154,"transaction_amount":11.11,"beneficiary":"BeerFactory","type":"debit_card","country":"France","Flag":"Greater than 5000","modelprediction":""}
        {"transaction_time_since_first_april_2022_00am_in_seconds":388,"transaction_amount":10.26,"beneficiary":"BeerDream","type":"credit_card","country":"Singapore","Flag":"Greater than 5000","modelprediction":""}
        {"transaction_time_since_first_april_2022_00am_in_seconds":447,"transaction_amount":32.37,"beneficiary":"BeerDream","type":"credit_card","country":"France","Flag":"Greater than 5000","modelprediction":""}
        {"transaction_time_since_first_april_2022_00am_in_seconds":450,"transaction_amount":3826.0,"beneficiary":"Mike","type":"credit_card","country":"France","Flag":"Greater than 5000","modelprediction":""}