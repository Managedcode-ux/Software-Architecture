from dataclasses import dataclass
from typing import Dict,List,Callable
from datetime import datetime
from queue import Queue
import threading
import time

#Event class to represent different types of events
@dataclass
class Event:
    type:str
    data:Dict
    timestamp: datetime = datetime.now()


# Event Channel - Handles queue management for a specific type of event
class EventChannel:
    def __init__(self,channel_name:str):
        self.name = channel_name
        self.queue = Queue()

    def push_event(self, event:Event):
        self.queue.put(event)
    
    def get_event(self):
        self.queue.get()


# Event Progessor - Processes event for a specific type of event
class EventProcessor(threading.Thread):
    def __init__(self,channel:EventChannel,mediator:'OrderMediator'):
        super().__init__()
        self.channel =  channel
        self.mediator = mediator
        self.running =  True

    def run(self):
        while self.running:
            try:
                event = self.channel.get_event()
                self.mediator.process_event(event)
            except Exception as e:
                print(f"Error processing event: {e}")
    

# Event Mediator -  coordinates all event processing
class OrderMediator:
    def __init__(self):
        # Services
        self.order_service = None
        self.notification_service = None
        self.inventory_service = None

        # Channels
        self.order_channel = EventChannel('orders')
        self.notification_channel = EventChannel('notifications')
        self.inventory_channel = EventChannel('inventory')

        # Processors
        self.processors = []
        self.setup_processors()

        def setup_processors(self):
            order_processor = EventProcessor(self.order_channel,self)
            notification_processor =EventProcessor(self.notficiation_channel,self)
            inventory_processor = EventProcessor(self.inventory_channel,self)

            self.processors.extend([order_processor,
                                    notification_processor,
                                    inventory_processor
                                    ])
            
            # Start Processors
            for processor in self.processors:
                processor.start()
        
        def set_services(self,order_service,notificatio_service,inventory_service):
            self.order_service = order_service
            self.notification_service = notificatio_service
            self.inventory_service = inventory_service
    
        def process_event(self,event:Event):
            if event.type == 'order_placed':
                self.notification_channel.push_event(
                    Event("Send notification",event.data)
                )

                self.inventory_channel.push_event(
                    Event("Update Inventory",event.data)
                )

# Services
class OrderService:
    def __init__(self,mediator:OrderMediator):
        self.mediator = mediator
    
    def place_order(self,user_id:str,product_id:str,quantity:int):
        order_data = {
            "order_id": "123",
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity
        }

        self.mediator.order_channel.push_event(
            Event("order_placed", order_data)
        )

class NotificationService:
    def send_order_confirmation(self,event:Event):
        print(f'[Notification Service] Sending order confirmation email for Order {event.data['order_id']}')

class InventoryService:
    def update_inventory(self,event:Event):
        print(f"[Inventory Service] Updating inventory for product
              {event.data['product_id']}")
        
        print(f"[Inventory Service] Reducing stock by 
              {event.data['quantity']} units")

def main():
     
     # Create Mediator
     mediator = OrderMediator()

     # Create Services
     order_service = OrderService(mediator)
     notification_service = NotificationService()
     inventory_service = InventoryService()

     # Set up services in mediator
     mediator.set_services(order_service,notification_service,inventory_service)

     # Place an order
     order_service.place_order("user123","prod456",2)

     # let the event process
     time.sleep(1)

     for processor in mediator.processors:
         processor.running = False

if __name__ == "__main__":
    main() 