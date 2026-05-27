import time
import psutil
import os


class Profiler:
    def __init__(self):
        self.results = []

    def start(self):
        self._start_time = time.perf_counter()
        self._process = psutil.Process(os.getpid())
        self._start_mem = self._process.memory_info().rss / 1024  # KB

    def stop(self, algorithm_name, nodes_visited):
        elapsed = time.perf_counter() - self._start_time
        end_mem = self._process.memory_info().rss / 1024  # KB
        mem_used = end_mem - self._start_mem

        result = {
            "algorithm": algorithm_name,
            "nodes_visited": nodes_visited,
            "time_ms": round(elapsed * 1000, 3),
            "memory_kb": round(mem_used, 2)
        }
        self.results.append(result)
        return result

    def print_last(self):
        if not self.results:
            print("No profiling data yet.")
            return
        r = self.results[-1]
        print(f"\n--- Profiler: {r['algorithm']} ---")
        print(f"  Nodes visited : {r['nodes_visited']}")
        print(f"  Time          : {r['time_ms']} ms")
        print(f"  Memory delta  : {r['memory_kb']} KB")

    def print_all(self):
        print("\n========= FULL BENCHMARK REPORT =========")
        for r in self.results:
            print(f"[{r['algorithm']}] nodes={r['nodes_visited']}  "
                  f"time={r['time_ms']}ms  mem={r['memory_kb']}KB")
        print("=========================================\n")