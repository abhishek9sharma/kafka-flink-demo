### A simple app to process some transaction using kafka and py-flink


### Steps to run the notebooks/code Used. Run in root mode on Unix Based System

- Install Docker from [here](https://docs.docker.com/get-docker/)

- Navigate to folder `kafka-flink-demo`. Once there run below command

        - you@yourmachine:~/somefolder/kafka-flink-demo$ chmod a+x rundemo.sh  && ./rundemo.sh
        
    If the command runs successfull you should see the below logs
    
            Creating network "kafka-flink-demo_default" with the default driver
            Creating predictionapi      ... done
            Creating zookeeper          ... done
            Creating transaction_loader ... done
            Creating broker             ... done
            Waiting for Kafka pods to come up
            #######################   
            Kafka started
            Created topic transactions.
            Browse http://localhost:8501/ to load transaction data to Kafka
            Browse http://localhost:5000/docs to see prediciton end point

- If `- you@yourmachine:~/somefolder/kafka-flink-demo/data$` is empty download the file [data_for_ml_ops_test.xlsx]()

        --you@yourmachine:~/somefolder/kafka-flink-demo/data$
            --you@yourmachine:~/somefolder/kafka-flink-demo/data/data_for_ml_ops_test.xlsx

- Go to link [http://localhost:8501/](http://localhost:8501/) and follow the steps to load the messages to Kafka

 
    

