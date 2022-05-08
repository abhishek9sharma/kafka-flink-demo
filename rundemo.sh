# docker stop $(docker ps|grep kafka-flink-demo_predictionapi| awk '{print $1}')
# docker container rm $(docker container ls -a|grep kafka-flink-demo_predictionapi| awk '{print $1}')
# docker image rm $(docker images|grep kafka-flink-demo_predictionapi| awk '{print $3}')
# docker stop $(docker ps|grep kafka-flink-demo_predictionapi| awk '{print $1}')
# docker container rm $(docker container ls -a|grep kafka-flink-demo_predictionapi| awk '{print $1}')
# docker image rm $(docker images|grep kafka-flink-demo_predictionapi| awk '{print $3}')


docker-compose up  -d --build  
#docker-compose up -d #--build

echo 'Waiting for Kafka pods to come up'
echo -ne '#####                     \r'
sleep 3
echo -ne '#############             \r'
sleep 3
echo -ne '#######################   \r'
echo -ne '\n'
echo 'Kafka started'

##Set up topics
#set up transactions
docker exec -it broker kafka-topics --create \
    --bootstrap-server localhost:9092 \
    --topic transactions

#set up fraudsurveillance
docker exec -it broker kafka-topics --create \
    --bootstrap-server localhost:9092 \
    --topic fraudsurveillance

# docker exec -it broker kafka-topics --create \
#     --bootstrap-server localhost:9092 \
#     --topic sales-usd

# docker exec -it broker kafka-topics --create \
#     --bootstrap-server localhost:9092 \
#     --topic sales-euros

echo "Browse http://localhost:8501/ to load transaction data to Kafka"
echo "Browse http://localhost:5000/docs to see prediciton end point"

#kafka-console-consumer --bootstrap-server localhost:9092 --topic transactions --from-beginning
# docker exec -it broker kafka-topics --create \
#     --bootstrap-server localhost:9092 \
#     --topic sales-euros


# docker exec -it transaction_monitoring_system python3 app/process_transactions.py
