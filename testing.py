# File to test each Layer separately
# To be removed before release

from threading import Thread
from Database import DataLayerServer as DLServer
from Server import BusinessLayerServer as BLServer
from Shared import LoadBalancer
from dotenv import load_dotenv
import os

load_dotenv()


def run_load_balancers():
    # Balancer List
    server_list = []

    # Load Balancers
    thread1 = Thread(target=LoadBalancer, args=(os.getenv('DL_LOAD_BALANCER_PORT'),))
    thread2 = Thread(target=LoadBalancer, args=(os.getenv('BL_LOAD_BALANCER_PORT'),))

    server_list.append([thread1, thread2])

    thread1.start()
    thread2.start()


def run_business_layer():
    BLServer()


def run_data_layer():
    DLServer()

