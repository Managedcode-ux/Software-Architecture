from dataclasses import dataclass
from typing import Dict, List, Callable
from datetime import datetime

# Event class to represent different types of events
@dataclass
class Event:
    type: str
    data: Dict
    timestamp: datetime = datetime.now()

# Event broker/bus that manages events and subscriptions
class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
    
    def publish(self, event: Event):
        if event.type in self.subscribers:
            for handler in self.subscribers[event.type]:
                handler(event)

# Example components that will use the event system
class OrderService:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
    
    def place_order(self, user_id: str, product_id: str, quantity: int):
        # Process order logic here
        order_data = {
            "order_id": "123",
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity
        }
        
        # Publish order placed event
        self.event_bus.publish(Event("order_placed", order_data))

class NotificationService:
    def send_order_confirmation(self, event: Event):
        print(f"Sending order confirmation email for Order {event.data['order_id']}")

class InventoryService:
    def update_inventory(self, event: Event):
        print(f"Updating inventory for Product {event.data['product_id']}")
        print(f"Reducing stock by {event.data['quantity']} units")

# Usage example
def main():
    # Create event bus
    event_bus = EventBus()
    
    # Create services
    order_service = OrderService(event_bus)
    notification_service = NotificationService()
    inventory_service = InventoryService()
    
    # Subscribe to events
    event_bus.subscribe("order_placed", notification_service.send_order_confirmation)
    event_bus.subscribe("order_placed", inventory_service.update_inventory)
    
    # Place an order
    order_service.place_order("user123", "prod456", 2)

if __name__ == "__main__":
    main()