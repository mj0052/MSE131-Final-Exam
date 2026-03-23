import random
import csv


def choose_item(r):
    # Returns item name and service time based on probabilities
    x = r.random()

    if x < 0.50:
        item_name = "Smoothie"
        service_time = r.uniform(2.5, 4.0)
    elif x < 0.80:
        item_name = "Fresh Pressed Juice"
        service_time = r.uniform(3.0, 5.0)
    else:
        item_name = "Smoothie Bowl"
        service_time = r.uniform(5.0, 7.0)

    return item_name, service_time


def simulate_jugo():
    # -------------------------
    # Parameters
    # -------------------------
    simulation_minutes = 120
    num_servers = 2
    mean_interarrival = 2.5
    random_seed = 42

    r = random.Random(random_seed)

    # -------------------------
    # Generate arrival times
    # -------------------------
    arrival_times = []
    current_time = 0.0

    while True:
        interarrival = r.expovariate(1 / mean_interarrival)
        current_time = current_time + interarrival

        if current_time > simulation_minutes:
            break

        arrival_times.append(current_time)

    # -------------------------
    # Server tracking
    # -------------------------
    server_available = [0.0] * num_servers
    server_busy = [0.0] * num_servers

    # -------------------------
    # Customer result lists
    # -------------------------
    customer_ids = []
    item_types = []
    service_times = []
    server_ids = []
    service_starts = []
    waiting_times = []
    departure_times = []

    # -------------------------
    # Simulate each customer
    # -------------------------
    for i in range(len(arrival_times)):
        customer_id = i + 1
        arrival_time = arrival_times[i]

        item_type, service_time = choose_item(r)

        # Find earliest free server
        best_server = 0
        for j in range(1, num_servers):
            if server_available[j] < server_available[best_server]:
                best_server = j

        service_start = max(arrival_time, server_available[best_server])
        waiting_time = service_start - arrival_time
        departure_time = service_start + service_time

        # Update server
        server_available[best_server] = departure_time
        server_busy[best_server] = server_busy[best_server] + service_time

        # Save results
        customer_ids.append(customer_id)
        item_types.append(item_type)
        service_times.append(service_time)
        server_ids.append(best_server + 1)
        service_starts.append(service_start)
        waiting_times.append(waiting_time)
        departure_times.append(departure_time)

    # -------------------------
    # Performance measures
    # -------------------------
    total_arrivals = len(arrival_times)

    if total_arrivals == 0:
        average_waiting_time = 0
        max_waiting_time = 0
        average_service_time = 0
    else:
        average_waiting_time = sum(waiting_times) / total_arrivals
        max_waiting_time = max(waiting_times)
        average_service_time = sum(service_times) / total_arrivals

    throughput = 0
    for t in departure_times:
        if t <= simulation_minutes:
            throughput += 1

    utilization_by_server = []
    for busy_time in server_busy:
        utilization_by_server.append(busy_time / simulation_minutes)

    average_utilization = sum(utilization_by_server) / num_servers

    # -------------------------
    # Average queue length
    # -------------------------
    # Queue length = waiting customers only
    events = []

    for i in range(total_arrivals):
        events.append((arrival_times[i], "arrival"))
        events.append((service_starts[i], "start"))

    # If same time, process service start before arrival
    events.sort(key=lambda x: (x[0], 0 if x[1] == "start" else 1))

    queue_length = 0
    max_queue_length = 0
    area_under_queue = 0.0
    last_time = 0.0

    for event in events:
        event_time = event[0]
        event_type = event[1]

        if event_time > simulation_minutes:
            event_time = simulation_minutes

        if event_time > last_time:
            area_under_queue = area_under_queue + queue_length * (event_time - last_time)
            last_time = event_time

        if event_type == "arrival":
            queue_length = queue_length + 1
            if queue_length > max_queue_length:
                max_queue_length = queue_length
        else:
            queue_length = queue_length - 1

    if last_time < simulation_minutes:
        area_under_queue = area_under_queue + queue_length * (simulation_minutes - last_time)

    average_queue_length = area_under_queue / simulation_minutes

    # -------------------------
    # Print summary
    # -------------------------
    print("JUGO JUICE BASELINE MODEL RESULTS")
    print("---------------------------------")
    print("Simulation length (minutes):", simulation_minutes)
    print("Number of workers:", num_servers)
    print("Average interarrival time (minutes):", round(mean_interarrival, 2))
    print("Total arrivals:", total_arrivals)
    print("Throughput:", throughput)
    print("Average waiting time (minutes):", round(average_waiting_time, 2))
    print("Maximum waiting time (minutes):", round(max_waiting_time, 2))
    print("Average service time (minutes):", round(average_service_time, 2))
    print("Average queue length:", round(average_queue_length, 2))
    print("Maximum queue length:", max_queue_length)
    print("Average utilization:", round(average_utilization * 100, 2), "%")

    for i in range(num_servers):
        print("Utilization of worker", i + 1, ":", round(utilization_by_server[i] * 100, 2), "%")

    # -------------------------
    # Save customer data to CSV
    # -------------------------
    file_name = "jugo_customer_results.csv"

    with open(file_name, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Customer ID",
            "Arrival Time",
            "Item Type",
            "Service Time",
            "Server ID",
            "Service Start",
            "Waiting Time",
            "Departure Time"
        ])

        for i in range(total_arrivals):
            writer.writerow([
                customer_ids[i],
                round(arrival_times[i], 3),
                item_types[i],
                round(service_times[i], 3),
                server_ids[i],
                round(service_starts[i], 3),
                round(waiting_times[i], 3),
                round(departure_times[i], 3)
            ])

    print("Customer results saved to jugo_customer_results.csv")


simulate_jugo()