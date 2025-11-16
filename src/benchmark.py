import socket
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FuncFormatter
from tqdm import tqdm
from statistics import mean, median
from concurrent.futures import wait, ThreadPoolExecutor
import time

HOST = "localhost"
PORT = 6969
DATA = b"Hello world\r\n\0"

times_by_parallel_bucket = defaultdict(list)

futures = []

def req(current_parallel_bucket):
    start = time.time()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(DATA)
        received = sock.recv(1024)
    end = time.time()
    times_by_parallel_bucket[current_parallel_bucket].append(end - start)



with ThreadPoolExecutor() as executor:
    for i in tqdm(range(100), desc="steps", position=0):
        total_parallel_requests = (i + 1) * 100
        for _ in tqdm(range(total_parallel_requests), desc="simulataneous requests", position=1, leave=False):
            future = executor.submit(req, total_parallel_requests)
            futures.append(future)


print("Waiting all requests to end...")
wait(futures)
print("All requests ended!")

times = [t for times in times_by_parallel_bucket.values() for t in times]
global_mean = mean(times)
global_median = median(times)

print(f"Mean response time: {global_mean * 1000:.3f}ms")
print(f"Median response time: {global_median * 1000:.3f}ms")

out_benchmark = "benchmark.png"
print(f"Generating {out_benchmark}...")
med_by_bucket = {
    b: median(t) * 1000
    for b, t in times_by_parallel_bucket.items()
}

mea_by_bucket = {
    b: mean(t) * 1000
    for b, t in times_by_parallel_bucket.items()
}

sorted_buckets = sorted(med_by_bucket.keys())
medians = [med_by_bucket[b] for b in sorted_buckets]
means = [mea_by_bucket[b] for b in sorted_buckets]
max_requests = max(sorted_buckets)

width = 0.5
step = 2

plt.figure(figsize=(16, 6))
x = np.arange(len(sorted_buckets))[::step]

plt.bar(x - width/2, medians[::step], width, label='Median')
plt.bar(x + width/2, means[::step], width, label='Mean')

plt.xticks(x, sorted_buckets[::step], rotation=45, ha='right')

plt.yscale('log')

def log_tick_formatter(val, pos):
    return f"{val:.3f}"

plt.gca().yaxis.set_major_formatter(FuncFormatter(log_tick_formatter))
plt.gca().yaxis.set_minor_formatter(FuncFormatter(log_tick_formatter))

plt.grid(True, which="both", ls="-", alpha=0.2)

plt.xlabel('Simultaneous requests')
plt.ylabel('Time (ms)')
plt.legend()

plt.text(
    0.02, 0.95,
    f"Max Simultaneous Requests: {max_requests}\n"
    f"Global Mean: {global_mean * 1000:.3f} ms\n"
    f"Global Median: {global_median * 1000:.3f} ms",
    transform=plt.gca().transAxes,
    verticalalignment='top',
    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
)

plt.tight_layout()

plt.savefig(out_benchmark, dpi=300, bbox_inches='tight')
print(f"{out_benchmark} generated.")
