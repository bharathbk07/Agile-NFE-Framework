import sys
import psutil
import time
from datetime import datetime
import matplotlib.pyplot as plt
import random
import os

# File to indicate the monitoring status
LOCK_FILE = "sustainability_metrics.lock"

# Initialize lists to store data
timestamps = []
battery_percentages = []
cpu_usages = []
temperatures = []
uptime = []
idle_times = []
active_cores = []
# active_threads = []
avg_power_per_core = []
# avg_power_per_thread = []

log_file = "sustainability_metrics.log"  # Name of the log file

# Function to write data to a file
def log_data_to_file(data):
    """Append data to the log file."""
    with open(log_file, "a") as file:
        file.write(data + "\n")

def get_temperature():
    """Simulate system temperature as macOS has restrictive APIs."""
    return random.uniform(30, 90)  # Simulated temperature (°C)

def get_uptime():
    """Get system uptime in seconds."""
    return int(time.time() - psutil.boot_time())

def get_idle_time():
    """Simulate idle time percentage."""
    return random.uniform(0, 20)  # Simulated idle time (%)

def get_avg_power_per_core(cpu_usage):
    """Simulate average power usage per core."""
    num_cores = psutil.cpu_count(logical=False)
    return (cpu_usage / num_cores) * random.uniform(0.5, 1.5)  # Simulated power usage (W)

def get_avg_power_per_thread(cpu_usage, num_threads):
    """Simulate average power consumption per thread."""
    return (cpu_usage / num_threads) * random.uniform(0.1, 0.5)  # Simulated power usage (W)

def monitor_sustainability_metrics():
    print("Monitoring sustainability metrics... (Press Ctrl+C to stop)")
    try:
        while os.path.exists(LOCK_FILE):
            # Capture current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            timestamps.append(timestamp)

            # Battery metrics
            battery = psutil.sensors_battery()
            if battery:
                battery_percentages.append(battery.percent)
            else:
                battery_percentages.append(None)

            # CPU metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_usages.append(cpu_usage)

            # System temperature (Simulated)
            temperatures.append(get_temperature())

            # System uptime
            uptime.append(get_uptime())

            # Idle time (Simulated)
            idle_times.append(get_idle_time())

            # Active cores
            active_cores_count = psutil.cpu_count(logical=True)
            active_cores.append(active_cores_count)

            # Active threads and threads power usage
            # try:
            #     # Active threads
            #     threads = sum([p.num_threads() for p in psutil.process_iter()])
            #     active_threads.append(threads)
            # except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
            #     #print(f"Access denied or process not found while fetching threads: {e}")
            #     active_threads.append(0)  # Default value if access denied


            # Avg power per core
            avg_core_power = get_avg_power_per_core(cpu_usage)
            avg_power_per_core.append(avg_core_power)

            #Avg power per thread
            # avg_thread_power = get_avg_power_per_thread(cpu_usage, threads)
            # avg_power_per_thread.append(avg_thread_power)

            # Print current metrics
            # print(f"[{timestamp}] Battery: {battery_percentages[-1]}% | CPU: {cpu_usages[-1]}% | Active Cores: {active_cores[-1]} | temperatures: {temperatures[-1]} C | idle_times: {idle_times[-1]} | uptime:{uptime[-1]} ")
            
            # Prepare data for logging
            log_entry = (f"[{timestamp}] Battery: {battery_percentages[-1]}% | CPU: {cpu_usages[-1]}% | Active Cores: {active_cores[-1]} | "
                        f"Temperatures: {temperatures[-1]} C | Idle Times: {idle_times[-1]} | Uptime: {uptime[-1]}")
        
            log_data_to_file(log_entry)
            
            # Wait for n seconds
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        stop_monitoring()

def generate_graph():
    # Ensure there is data to plot
    if not timestamps:
        print("No data available for graph generation.")
        return

    # Ensure all lists have the same length
    # min_length = min(len(timestamps), len(battery_percentages), len(cpu_usages), len(temperatures),
    #                  len(active_cores), len(active_threads), len(avg_power_per_core), len(avg_power_per_thread))

    min_length = min(len(timestamps), len(battery_percentages), len(cpu_usages), len(temperatures),
                    len(active_cores), len(avg_power_per_core))

    # Trim all lists to the same length
    trimmed_timestamps = timestamps[:min_length]
    trimmed_battery_percentages = battery_percentages[:min_length]
    trimmed_cpu_usages = cpu_usages[:min_length]
    trimmed_temperatures = temperatures[:min_length]
    trimmed_active_cores = active_cores[:min_length]
    # trimmed_active_threads = active_threads[:min_length]
    trimmed_avg_power_per_core = avg_power_per_core[:min_length]
    # trimmed_avg_power_per_thread = avg_power_per_thread[:min_length]

    # Convert timestamps for plotting
    time_labels = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in trimmed_timestamps]

    # Create a new figure
    plt.figure(figsize=(12, 8))

    # Plot metrics
    plt.plot(time_labels, trimmed_battery_percentages, label="Battery Percentage (%)", marker='o', color='blue')
    plt.plot(time_labels, trimmed_cpu_usages, label="CPU Usage (%)", marker='o', color='green')
    plt.plot(time_labels, trimmed_temperatures, label="Temperature (°C)", marker='o', color='red')
    plt.plot(time_labels, trimmed_active_cores, label="Active Cores", linestyle='--', color='purple')
    # plt.plot(time_labels, trimmed_active_threads, label="Active Threads", linestyle='--', color='cyan')
    plt.plot(time_labels, trimmed_avg_power_per_core, label="Avg Power/Core (W)", linestyle='-', color='orange')
    # plt.plot(time_labels, trimmed_avg_power_per_thread, label="Avg Power/Thread (W)", linestyle='-', color='magenta')

    # Labels, legend, and title
    plt.title("Sustainability Metrics Over Time", fontsize=16)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Metrics", fontsize=12)
    plt.legend(loc="upper left", fontsize=10)
    plt.grid(True)

    # Rotate X-axis labels for better readability
    plt.xticks(rotation=45)

    # Adjust layout to avoid overlap
    plt.tight_layout()

    # Save graph locally
    graph_filename = "sustainability_report.png"
    if graph_filename:
        os.remove(graph_filename)
        print('\nRemoved exisitng graph.')
    plt.savefig(graph_filename)
    print(f"\nGraph saved as {graph_filename}")


def start_monitoring():
    if os.path.exists(LOCK_FILE):
        print("Monitoring is already running.")
        return

    with open(LOCK_FILE, "w") as lock_file:
        lock_file.write("running")

    monitor_sustainability_metrics()

def stop_monitoring():
    if os.path.exists(LOCK_FILE):
        generate_graph()
        os.remove(LOCK_FILE)
        print("Monitoring stopped.")     
    else:
        print("Monitoring is not running.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sustainability_metrics.py [start|stop]")
        sys.exit(1)

    command = sys.argv[1].lower()
    if command == "start":
        start_monitoring()
    elif command == "stop":
        stop_monitoring()
    else:
        print("Invalid command. Use 'start' or 'stop'.")
