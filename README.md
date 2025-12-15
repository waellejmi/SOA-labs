# PART1
1. Since order service and inventory service are decoupled and not chained, the order service continues to function as normal

2. Replication: each topic is replicated across multiple brokers/  Durable Storage: Kafka persists messages to disk and replicates them for fault tolerance. / acknowledgments: Consumers acknowledge the receipt of messages, allowing Kafka to track which messages have been processed.

3. Consumer id controls which Consumers in a group process which messages.

# PART2
1. Since they share same consumer ID, kafka will load balance the messages between the consumers in same group (2 instances of order service). So each instance will get some of the messages.

2. Assign each consumer instance a unique consumer ID so that each instance gets all the messages.

3. Single instance per group -> full message delivery to that service. Multiple instances in same group -> partitioned delivery among instances.


