import random


def choose_item(r, scenario_name):
    x = r.random()

    # Default item mix
    p_smoothie = 0.50
    p_juice = 0.30

    # Scenario: more smoothie bowls ordered
    if scenario_name == "More Bowls":
        p_smoothie = 0.40
        p_juice = 0.30

    if x < p_smoothie:
        item_name = "Smoothie"
        if scenario_name == "Slow Service":
            service_time = r.uniform(3.0, 4.5)
        else:
            service_time = r.uniform(2.5, 4.0)

    elif x < p_smoothie + p_juice:
        item_name = "Fresh Pressed Juice"
        if scenario_name == "Slow Service":
            service_time = r.uniform(3.5, 5.5)
        else:
            service_time = r.uniform(3.0, 5.0)

    else:
        item_name = "Smoothie Bowl"
        if scenario_name == "Slow Service":
            service_time = r.uniform(6.0, 8.0)
        else:
            service_time = r.uniform(5.0, 7.0)

    return item_name, service_time


def simulate_jugo(scenario_name):
    simulation_minutes = 120
    random_seed = 42
    r = random.Random(random_seed)

    # Baseline settings
    num_servers = 2
    mean_interarrival = 2.5

    # Scenario 1: more workers
    if scenario_name == "Three Workers":
        num_servers = 3

    # Scenario 2: higher demand
    if scenario_name == "High Demand":
        mean_interarrival = 1.5

    arrival_times = []
    current_time = 0.0

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

    for i in range(len(arrival_times)):
        arrival_time = arrival_times[i]
        item_type, service_time = choose_item(r, scenario_name)

        # Find earliest available server
        best_server = 0
        for j in range(1, num_servers):
            if server_available[j] < server_available[best_server]:
                best_server = j

        service_start = max(arrival_time, server_available[best_server])
        waiting_time = service_start - arrival_time
        departure_time = service_start + service_time

        server_available[best_server] = departure_time
        server_busy[best_server] += service_time

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

    average_utilization = sum(server_busy) / (num_servers * simulation_minutes)

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

    return [
        scenario_name,
        total_arrivals,
        round(average_waiting_time, 2),
        round(average_queue_length, 2),
        throughput,
        round(average_utilization * 100, 2)
    ]


def print_results_table(results):
    print("\nJUGO JUICE EXTENDED MODEL")
    print("-" * 78)
    print(f"{'Scenario':<18}{'Arrivals':<10}{'Avg Wait':<12}{'Avg Queue':<12}{'Throughput':<12}{'Utilization %':<14}")
    print("-" * 78)

    for row in results:
        print(
            f"{row[0]:<18}"
            f"{row[1]:<10}"
            f"{row[2]:<12}"
            f"{row[3]:<12}"
            f"{row[4]:<12}"
            f"{row[5]:<14}"
        )


def run_all_scenarios():
    results = []

    results.append(simulate_jugo("Baseline"))
    results.append(simulate_jugo("Three Workers"))
    results.append(simulate_jugo("High Demand"))
    results.append(simulate_jugo("Slow Service"))

    print_results_table(results)


run_all_scenarios() 