import tkinter as tk
from tkinter import (filedialog, messagebox)
import csv

def fcfs(processes):
    processes.sort(key=lambda x: x['arrival'])
    time = 0
    result = []

    for p in processes:
        if time < p['arrival']:
            time = p['arrival']

        start = time
        finish = start + p['burst']
        waiting = start - p['arrival']
        turnaround = finish - p['arrival']

        result.append({
            **p,
            'start': start,
            'finish': finish,
            'waiting': waiting,
            'turnaround': turnaround
        })

        time = finish

    return result


def sjf_non_preemptive(processes):
    processes = sorted(processes, key=lambda x: x['arrival'])
    time = 0
    completed = []
    ready = []

    while processes or ready:
        while processes and processes[0]['arrival'] <= time:
            ready.append(processes.pop(0))

        if not ready:
            time = processes[0]['arrival']
            continue

        ready.sort(key=lambda x: x['burst'])
        p = ready.pop(0)

        start = time
        finish = start + p['burst']
        waiting = start - p['arrival']
        turnaround = finish - p['arrival']

        completed.append({
            **p,
            'start': start,
            'finish': finish,
            'waiting': waiting,
            'turnaround': turnaround
        })

        time = finish

    return completed
root = tk.Tk()
root.mainloop()