# kafka_lab1.md

## Download and extract Kafka
Download Kafka, by running the command below:
```
wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.12-2.8.0.tgz
```

Extract kafka from the zip file by running the command below.
```
tar -xzf kafka_2.12-2.8.0.tgz
```
This creates a new directory 'kafka_2.12-2.8.0' in the current directory.

## start ZooKeeper
ZooKeeper is required for Kafka to work. Start the ZooKeeper server.
```
cd kafka_2.12-2.8.0
bin/zookeeper-server-start.sh config/zookeeper.properties
```

## Start the Kafka broker service

Start a new terminal.

```
cd kafka_2.12-2.8.0
bin/kafka-server-start.sh config/server.properties
```

## Create a topic
Open a new terminal.

You need to create a topic before you can start to post messages.

To create a topic named news, start a new terminal and run the command below.
```
cd kafka_2.12-2.8.0
bin/kafka-topics.sh --create --topic news --bootstrap-server localhost:9092
```

## Start Producer
```
bin/kafka-console-producer.sh --topic news --bootstrap-server localhost:9092
```

Once the producer starts, and you get the '>' prompt, type any text message and press enter. Or you can copy the text below and paste. The below text sends three messages to kafka.
```
Good morning
Good day
Enjoy the Kafka lab
```

## Start Consumer
Open a new terminal.
```
cd kafka_2.12-2.8.0
bin/kafka-console-consumer.sh --topic news --from-beginning --bootstrap-server localhost:9092
```
You should see all the messages you sent from the producer appear here.

You can go back to the producer terminal and type some more messages, one message per line, and you will see them appear here.