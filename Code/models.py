# models.py
class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = 0
        self.finish_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

    def __str__(self):
        return f"P{self.pid}"

    def reset(self):
        """Reset các giá trị tính toán trước khi chạy thuật toán mới"""
        self.start_time = self.finish_time = self.turnaround_time = self.waiting_time = 0


class SchedulerModel:
    def simulate_fcfs(self, processes):
        """First Come First Served - Non-preemptive"""
        for p in processes:
            p.reset()

        processes = sorted(processes, key=lambda p: p.arrival_time)
        current_time = 0
        timeline = []

        for p in processes:
            if current_time < p.arrival_time:
                current_time = p.arrival_time

            p.start_time = current_time
            p.finish_time = current_time + p.burst_time
            p.turnaround_time = p.finish_time - p.arrival_time
            p.waiting_time = p.start_time - p.arrival_time

            timeline.append((p.start_time, p.finish_time, p.pid))
            current_time = p.finish_time

        return processes, timeline

    def simulate_sjf_non_preemptive(self, processes):
        """Shortest Job First - Non-preemptive"""
        for p in processes:
            p.reset()

        processes = sorted(processes, key=lambda p: p.arrival_time)
        current_time = 0
        completed = []
        timeline = []
        remaining = processes[:]

        while remaining:
            arrived = [p for p in remaining if p.arrival_time <= current_time]

            if not arrived:
                if not remaining:
                    break
                current_time = min(p.arrival_time for p in remaining)
                continue

            shortest = min(arrived, key=lambda p: p.burst_time)

            shortest.start_time = current_time
            shortest.finish_time = current_time + shortest.burst_time
            shortest.turnaround_time = shortest.finish_time - shortest.arrival_time
            shortest.waiting_time = shortest.start_time - shortest.arrival_time

            timeline.append((shortest.start_time, shortest.finish_time, shortest.pid))
            current_time = shortest.finish_time
            completed.append(shortest)
            remaining.remove(shortest)

        return completed, timeline

    def calculate_average(self, processes):
        """Tính trung bình TAT và WT"""
        if not processes:
            return 0.0, 0.0

        avg_tat = sum(p.turnaround_time for p in processes) / len(processes)
        avg_wt = sum(p.waiting_time for p in processes) / len(processes)
        return round(avg_tat, 2), round(avg_wt, 2)