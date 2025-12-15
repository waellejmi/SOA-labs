# PART1
1- Since order service and inventory service are decoupled and not chained, the order service continues to function as normal
2 - replication: each topic is replicated across multiple brokers/  Durable Storage: Kafka persists messages to disk and replicates them for fault tolerance. / acknowledgments: Consumers acknowledge the receipt of messages, allowing Kafka to track which messages have been processed.
3- consumer id controls which Consumers in a group process which messages.
