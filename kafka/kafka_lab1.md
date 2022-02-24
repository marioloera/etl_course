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

list the topis
```
bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

describe topics
```
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic bankbranch
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

## Start Producer with keys

Ok, we can now start a new producer and consumer, this time using message keys.
You can start a new producer with the following message key commands:

--property parse.key=true to make the producer parse message keys
--property key.separator=: define the key separator to be the : character,

so our message with key now looks like the following key-value pair example: 
    - 1:{"atmid": 1, "transid": 102}. Here the message key is 1, which also corresponds to the ATM id, and the value is the transaction JSON object, {"atmid": 1, "transid": 102}.

Start a new producer with message key enabled:
```
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic bankbranch --property parse.key=true --property key.separator=:
```

Publish message with keys
```
1:{"atmid": 1, "transid": 102}
1:{"atmid": 1, "transid": 103}
2:{"atmid": 2, "transid": 202}
2:{"atmid": 2, "transid": 203}
1:{"atmid": 1, "transid": 104}
```

## Start Consumer with keys

and start a new consumer with
--property print.key=true --property key.separator=: arguments to print the keys


```
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch --from-beginning --property print.key=true --property key.separator=:
```
Now, you should see that messages that have the same key are being consumed in the same order
(e.g., trans102 -> trans103 -> trans104) as they were published.

This is because each topic partition maintains its own message queue, and new messages are enqueued (appended to the end of the queue) as they get published to the partition. Once consumed, the earliest messages will be dequeued and nno longer be available for consumption.

Recall that with two partitions and no message keys specified, the transaction messages were published to the two partitions in rotation:

Partition 0: [{"atmid": 1, "transid": 102}, {"atmid": 2, "transid": 202}, {"atmid": 1, "transid": 104}]
Partition 1: [{"atmid": 1, "transid": 103}, {"atmid": 2, "transid": 203}]

As you can see, the transaction messages from atm1 and atm2 got scattered across both partitions. 
It would be difficult to unravel this and consume messages from one ATM with the same order as they were published.

However, with message key specified as the atmid value, the messages from the two ATMs will look like the following:

Partition 0: [{"atmid": 1, "transid": 102}, {"atmid": 1, "transid": 103}, {"atmid": 1, "transid": 104}]
Partition 1: [{"atmid": 2, "transid": 202}, {"atmid": 2, "transid": 203}]
Messages with the same key will always be published to the same partition, so that their published order will be preserved within the message queue of each partition.

As such, we can keep the states or orders of the transactions for each ATM.


## Consumer Offset
Topic partitions keeps published messages in a sequence, like a list. Message offset indicates a message's position in the sequence. For example, the offset of an empty Partition 0 of bankbranch is 0, and if you publish the first message to the partition, its offset will be 1.

By using offsets in the consumer, you can specify the starting position for message consumption, such as from the beginning to retrieve all messages, or from some later point to retrieve only the latest messages

## Consumer Group
In addition, we normally group related consumers together as a consumer group. For example, we may want to create a consumer for each ATM in the bank and manage all ATM related consumers together in a group.

So let's see how to create a consumer group, which is actually very easy with the --group argument.

In the consumer terminal, stop the previous consumer if it is still running.

Run the following command to create a new consumer within a consumer group called atm-app:
```
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch --group atm-app
```

you should not expect any messages to be consumed.
This is because the offsets for both partitions have already reached to the end. In other words,
all messages have already been consumed, and therefore dequeued, by previous consumers.

Show the details of the consumer group
```
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group atm-app
```

Recall that we have published 10 messages in total, and we can see the CURRENT-OFFSET column of partition 1 is 6 and CURRENT-OFFSET of partition 0 is 4, and they add up to 10 messages.

The LOG-END-OFFSETcolumn indicates the last offset or the end of the sequence, which is 6 for partition 1 and 4 for partition 0. Thus, both partitions have reached the end of their queues and no more messages are available for consumption.

Meanwhile, you can check the LAG column which represents the count of unconsumed messages for each partition. Currently it is 0 for all partitions, as expected

## Reset offset

We can reset the index with the --reset-offsets argument.

First let's try resetting the offset to the earliest position (beginning) using --reset-offsets --to-earliest.

Stop the previous consumer if it is still running, and run the following command to reset the offset:

```
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092  --topic bankbranch --group atm-app --reset-offsets --to-earliest --execute
```


Shift the offset to left by 2 using --reset-offsets --shift-by -2:
```
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092  --topic bankbranch --group atm-app --reset-offsets --shift-by -2 --execute
```
