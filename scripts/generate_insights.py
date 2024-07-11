import re
from collections import defaultdict
import os

# Regular expression to match the log line format and extract function name and execution time
log_pattern = re.compile(r"Execution Time: (\w+) executed in ([\d.]+) seconds")

# Data structure to hold execution times for each function
execution_times = defaultdict(list)

# Read the log file in src/logs
log_file_path = os.path.join(os.path.dirname(__file__), '..', 'src\logs', 'app_performance.log')
with open(log_file_path, 'r') as log_file:
    for line in log_file:
        # Match the log line format
        match = log_pattern.search(line)
        if match:
            # Extract function name and execution time
            function_name, execution_time = match.groups()
            # Add the execution time to the list of times for the function
            execution_times[function_name].append(float(execution_time))

# Compute and display insights
for function_name, times in execution_times.items():
    total_time = sum(times)
    average_time = total_time / len(times)
    print(f"Function: {function_name}")
    print(f"  Total Execution Time: {total_time:.6f} seconds")
    print(f"  Average Execution Time: {average_time:.6f} seconds")
    print(f"  Number of Calls: {len(times)}\n")