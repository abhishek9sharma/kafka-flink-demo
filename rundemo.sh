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
#     --topic transactions2


# #set up fraudsurveillance
# docker exec -it broker kafka-topics --create \
#     --bootstrap-server localhost:9092 \
#     --topic fraudsurveillance2

echo "Browse http://localhost:8501/ to load transaction data to Kafka"
echo "Browse http://localhost:5000/docs to see prediction end point"

echo 'Once you load data from http://localhost:8501/ the final flat file should be produced in data folder'

# echo 'Once you load data from http://localhost:8501/ run below command to see messages processed by flink'
# echo 'docker exec -it broker kafka-console-consumer --from-beginning     --bootstrap-server localhost:9092     --topic fraudsurveillance'

