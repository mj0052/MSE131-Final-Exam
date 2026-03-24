# Jugo Juice Waiting Line Simulation (MSE 131 Final Project)

## Overview
This project models a Jugo Juice service system using a waiting line simulation. The goal is to analyze how customer flow, service time, and staffing affect performance measures such as waiting time, queue length, throughput, and utilization.

The system is based on a single queue with multiple workers preparing three types of items:
- Smoothies
- Fresh pressed juices
- Smoothie bowls

---

## Baseline Model
The baseline model represents normal operating conditions at a Jugo Juice location.

### Assumptions
- One common queue
- Two workers serving customers
- First come, first served
- Customers arrive randomly (exponential distribution)
- Service times vary depending on item type:
  - Smoothies: 2.5 to 4.0 minutes
  - Fresh juice: 3.0 to 5.0 minutes
  - Smoothie bowls: 5.0 to 7.0 minutes
- Simulation runs for 120 minutes

### Performance Measures
- Average waiting time
- Average queue length
- Throughput (customers served)
- Worker utilization

---

## Extensions
Five scenarios were tested to analyze system behavior:

1. **Three Workers**  
   Increased number of workers from 2 to 3

2. **High Demand**  
   Increased customer arrival rate (lunch rush)

3. **Slow Service**  
   Increased service times

4. **Fast Service**  
   Decreased service times (efficiency improvement)

5. **More Bowls**  
   Increased proportion of smoothie bowl orders

---

## Key Insights
- Adding a worker significantly reduces waiting time and queue length
- High demand causes major congestion and long delays
- Slower service reduces throughput and increases wait time
- Faster service improves overall system performance
- Product mix (more bowls) increases congestion due to longer prep time

---

## Files
- `jugo_baseline.py` → Baseline simulation model  
- `jugo_extended_model.py` → Extended scenarios and comparisons  

---
