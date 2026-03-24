import random


def choose_item(r):
    x = r.random()

    # Item probabilities
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


def simulate_baseline():
    simulation_minutes = 120
    random_seed = 42
    r = random.Random(random_seed)

    num_servers = 2
    mean_interarrival = 2.5

    arrival_times = []
    current_time = 0.0

    # Generate arrivals
    while True:
        interarrival = r.expovariate(1 / mean_interarrival)
        current_time += interarrival

        if current_time > simulation_minutes:
            break

        arrival_times.append(current_time)

    server_available = [0.0] * num_servers
    server_busy = [0.0] * num_servers

    service_starts = []
    waiting_times = []
    service_times = []
    departure_times = []

    # Process customers
    for i in range(len(arrival_times)):
        arrival_time = arrival_times[i]
        item_type, service_time = choose_item(r)

        # Find earliest available server
        best_server = 0
        for j in range(1, num_servers):
            if server_available[j] < server_available[best_server]:
                best_server = j

        service_start = max(arrival_time, server_available[best_server])
        departure_time = service_start + service_time
        waiting_time = service_start - arrival_time

        server_available[best_server] = departure_time

        # Only count busy time within simulation window
        busy_start = service_start
        busy_end = departure_time

        if busy_start < simulation_minutes:
            if busy_end > simulation_minutes:
                busy_end = simulation_minutes
            server_busy[best_server] += (busy_end - busy_start)

        service_starts.append(service_start)
        waiting_times.append(waiting_time)
        service_times.append(service_time)
        departure_times.append(departure_time)

    total_arrivals = len(arrival_times)

    if total_arrivals == 0:
        average_waiting_time = 0
        average_service_time = 0
    else:
        average_waiting_time = sum(waiting_times) / total_arrivals
        average_service_time = sum(service_times) / total_arrivals

    throughput = 0
    for t in departure_times:
        if t <= simulation_minutes:
            throughput += 1

    utilization = sum(server_busy) / (num_servers * simulation_minutes)

    # Queue length calculation
    events = []
    for i in range(total_arrivals):
        events.append((arrival_times[i], "arrival"))
        events.append((service_starts[i], "start"))

    events.sort(key=lambda x: (x[0], 0 if x[1] == "start" else 1))

    queue_length = 0
    area_under_queue = 0.0
    last_time = 0.0

    for event in events:
        event_time, event_type = event

        if event_time > simulation_minutes:
            event_time = simulation_minutes

        if event_time > last_time:
            area_under_queue += queue_length * (event_time - last_time)
            last_time = event_time

        if event_type == "arrival":
            queue_length += 1
        else:
            queue_length -= 1

    if last_time < simulation_minutes:
        area_under_queue += queue_length * (simulation_minutes - last_time)

    average_queue_length = area_under_queue / simulation_minutes

    print("\nJUGO JUICE BASELINE MODEL")
    print("-" * 60)
    print("Total arrivals:", total_arrivals)
    print("Average waiting time:", round(average_waiting_time, 2), "minutes")
    print("Average queue length:", round(average_queue_length, 2))
    print("Throughput:", throughput)
    print("Utilization:", round(utilization * 100, 2), "%")


simulate_baseline()