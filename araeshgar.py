import simpy
import random
import numpy as np
import time
from dataclasses import dataclass, field

# Simulation Constants
SIMULATION_TIME = 600  # Total simulation time (10 hours) until finishes all customers still waiting in the queue
WORKING_HOURS = 8 * 60  # 8 hours in minutes
CUSTOMER_ARRIVAL_RATE = 1.2  # Avg customer every 1.2 minutes to reduce overload
MIN_SERVICE_TIME = 5  # Minimum haircut duration (minutes)
MAX_SERVICE_TIME = 30  # Maximum haircut duration (minutes)

@dataclass
class SimulationMetrics:
    wait_times: list = field(default_factory=list)
    queue_lengths: list = field(default_factory=list)
    service_durations: list = field(default_factory=list)
    total_customers: int = 0
    delayed_customers: int = 0
    total_service_time: float = 0.0

class BarberShop:
    def __init__(self, env):
        self.env = env
        self.barber = simpy.Resource(env, capacity=1)
        self.is_open = True

    def serve_customer(self, metrics, service_start_time):
        service_time = random.uniform(MIN_SERVICE_TIME, MAX_SERVICE_TIME)
        metrics.service_durations.append(service_time)
        metrics.total_service_time += service_time
        yield self.env.timeout(service_time)

def customer_arrival(env, shop, metrics):
    customer_id = 1
    while shop.is_open:
        yield env.timeout(random.expovariate(1 / CUSTOMER_ARRIVAL_RATE))
        metrics.total_customers += 1
        env.process(handle_customer(env, shop, customer_id, metrics))
        customer_id += 1

def handle_customer(env, shop, customer_id, metrics):
    arrival_time = env.now
    with shop.barber.request() as req:
        yield req
        service_start_time = env.now
        wait_time = service_start_time - arrival_time
        metrics.wait_times.append(wait_time)
        if wait_time > 0:
            metrics.delayed_customers += 1
        yield env.process(shop.serve_customer(metrics, service_start_time))

def monitor_queue(env, shop, metrics):
    while shop.is_open or shop.barber.count > 0:
        metrics.queue_lengths.append(len(shop.barber.queue))
        yield env.timeout(1)

def close_shop(env, shop):
    yield env.timeout(WORKING_HOURS)
    shop.is_open = False
    while shop.barber.count > 0 or len(shop.barber.queue) > 0:
        yield env.timeout(1)  # Continue running until all customers are served

def run_simulation():
    env = simpy.Environment()
    metrics = SimulationMetrics()
    shop = BarberShop(env)

    # Start simulation processes
    env.process(customer_arrival(env, shop, metrics))
    env.process(monitor_queue(env, shop, metrics))
    env.process(close_shop(env, shop))

    # Run the simulation
    start_time = time.time()
    env.run(until=SIMULATION_TIME)
    end_time = time.time()

    avg_wait = np.mean(metrics.wait_times) if metrics.wait_times else 0
    avg_queue = np.mean(metrics.queue_lengths) if metrics.queue_lengths else 0
    utilization = (metrics.total_service_time / WORKING_HOURS) * 100 if metrics.total_service_time else 0
    max_wait_time = max(metrics.wait_times) if metrics.wait_times else 0
    max_queue_length = max(metrics.queue_lengths) if metrics.queue_lengths else 0

    print(f"Simulation completed in {end_time - start_time:.2f} seconds")
    print(f"Average customer wait time: {avg_wait:.2f} minutes")
    print(f"Maximum customer wait time: {max_wait_time:.2f} minutes")
    print(f"Average queue length: {avg_queue:.2f} customers")
    print(f"Maximum queue length: {max_queue_length:.2f} customers")
    print(f"Barber utilization rate: {utilization:.2f}%")
    print(f"Total customers served: {metrics.total_customers}")
    print(f"Delayed customers: {metrics.delayed_customers}")

if __name__ == "__main__":
    run_simulation()
