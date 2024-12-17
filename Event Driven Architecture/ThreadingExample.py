import threading
import time

#Without threading
def make_coffee():
    print("Starting to make coffee..")
    time.sleep(2) # Simulating coffee brewing time
    print("Coffee ready")

def make_toast():
    print("Starting to make toast..")
    time.sleep(3) # Simulating toasting time
    print("Toast ready")

make_coffee()
make_toast()
#With threading
class CoffeeMaker(threading.Thread):
    def run(self):
        print("Starting to make coffee using coffee maker..")
        time.sleep(2) # Simulating coffee brewing time
        print("Coffee ready")

class ToastMaker(threading.Thread):
    def run(self):
        print("Starting to make toast using toast maker...")
        time.sleep(3)
        print("Toast is ready!")

coffee_thread = CoffeeMaker()
toast_thread = ToastMaker()

coffee_thread.start()
toast_thread.start()

coffee_thread.join()
toast_thread.join()