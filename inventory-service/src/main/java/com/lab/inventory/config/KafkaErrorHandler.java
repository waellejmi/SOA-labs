package com.lab.inventory.config;

import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.listener.CommonErrorHandler;
import org.springframework.kafka.listener.MessageListenerContainer;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class KafkaErrorHandler implements CommonErrorHandler {

    private final KafkaTemplate<String, Object> kafkaTemplate;

    @Value("${kafka.topic.order-events-dlq}")
    private String dlqTopic;

    public KafkaErrorHandler(KafkaTemplate<String, Object> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    @Override
    public boolean handleOne(Exception thrownException, ConsumerRecord<?, ?> record,
                            Consumer<?, ?> consumer, MessageListenerContainer container) {
        log.error("Error processing record: {}", record, thrownException);

        try {
            // Send to DLQ
            kafkaTemplate.send(dlqTopic, (String) record.key(), record.value());
            log.info("Message sent to DLQ: {}", record);
        } catch (Exception e) {
            log.error("Failed to send message to DLQ", e);
        }

        // Return false to commit the offset (message handled)
        return false;
    }
}

