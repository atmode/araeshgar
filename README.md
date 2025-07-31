## Barber Shop Simulation

Barber Shop Simulation is a Python implementation for modeling a single-barber shop using discrete-event simulation. This code allows users to simulate customer arrivals, service times, and queue dynamics over an 8-hour day, computing key metrics like wait times and utilization.

### Key Features

- **Customer Arrival Modeling**: Uses exponential distribution for random arrivals via SimPy.
- **Service Handling**: Simulates haircut durations with uniform random times between 5-30 minutes.
- **Metrics Tracking**: Collects data on wait times, queue lengths, and barber utilization using NumPy for calculations.
- **Shop Operations**: Includes logic for shop closure while serving remaining customers, ensuring all queued patrons are handled.

### Usage

To use the Barber Shop Simulation, save the code as `barber_shop_simulation.py` and run it with Python. Adjust constants like `CUSTOMER_ARRIVAL_RATE` for different scenarios. The script outputs performance metrics directly to the console.

### Example

```python
# Run the simulation
if __name__ == "__main__":
    run_simulation()
```

This will produce output similar to:

```
Simulation completed in 0.05 seconds
Average customer wait time: 8.60 minutes
Maximum customer wait time: 25.30 minutes
Average queue length: 1.20 customers
Maximum queue length: 5 customers
Barber utilization rate: 85.00%
Total customers served: 350
Delayed customers: 200
```

(Note: Results vary due to randomness in arrivals and service times.)
