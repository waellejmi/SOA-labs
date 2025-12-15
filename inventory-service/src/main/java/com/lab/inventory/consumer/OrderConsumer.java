package com.lab.inventory.consumer;

import com.lab.inventory.dto.OrderEventDTO;
import com.lab.inventory.model.InventoryItem;
import com.lab.inventory.repository.InventoryRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Slf4j
public class OrderConsumer {
    
    private final InventoryRepository inventoryRepository;
    
    @KafkaListener(
        topics = "${kafka.topic.order-events}",
        groupId = "${spring.kafka.consumer.group-id}",
        containerFactory = "kafkaListenerContainerFactory"
    )
    public void consumeOrderEvent(
            @Payload OrderEventDTO event,
            @Header(KafkaHeaders.RECEIVED_PARTITION) int partition,
            @Header(KafkaHeaders.OFFSET) long offset,
            Acknowledgment acknowledgment) {
        
        log.info("Received order event from partition {} offset {}: {}", partition, offset, event);
        
        try {
            if ("ORDER_CREATED".equals(event.getEventType())) {
                // Simulate potential error
                if (event.getQuantity() < 0) {
                    throw new IllegalArgumentException("Invalid quantity: " + event.getQuantity());
                }
                
                InventoryItem item = new InventoryItem(
                    event.getOrderId(),
                    event.getProductName(),
                    event.getQuantity()
                );
                
                InventoryItem saved = inventoryRepository.save(item);
                log.info("Inventory reserved: {}", saved);
                
                // Manual acknowledgment
                acknowledgment.acknowledge();
            }
        } catch (Exception e) {
            log.error("Error processing order event: {}", event, e);
            throw e; // Will trigger error handler
        }
    }
}
