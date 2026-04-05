import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import copy

class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = int(arrival)
        self.burst = int(burst)
        self.start = 0
        self.finish = 0
        self.waiting = 0
        self.turnaround = 0

def read_csv(file_path):
    processes = []
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = {k.strip().lower(): v for k, v in row.items()}
            processes.append(Process(
                row.get('process'),
                row.get('arrival'),
                row.get('burst')
            ))
    return processes

def fcfs(processes):
    processes.sort(key=lambda x: x.arrival)
    time = 0
    for p in processes:
        if time < p.arrival:
            time = p.arrival
        p.start = time
        p.finish = time + p.burst
        p.waiting = p.start - p.arrival
        p.turnaround = p.finish - p.arrival
        time = p.finish
    return processes

def sjf(processes):
    time = 0
    completed = []
    processes = sorted(processes, key=lambda x: x.arrival)
    ready = []

    while processes or ready:
        while processes and processes[0].arrival <= time:
            ready.append(processes.pop(0))

        if ready:
            ready.sort(key=lambda x: x.burst)
            p = ready.pop(0)
        else:
            time = processes[0].arrival
            continue

        p.start = time
        p.finish = time + p.burst
        p.waiting = p.start - p.arrival
        p.turnaround = p.finish - p.arrival
        time = p.finish
        completed.append(p)

    return completed

def write_full_csv(path, fcfs_result, sjf_result):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)

        # FCFS
        writer.writerow(["FCFS RESULT"])
        writer.writerow(["Process","Arrival","Burst","Start","Finish","Waiting","Turnaround"])
        for p in fcfs_result:
            writer.writerow([p.pid, p.arrival, p.burst, p.start, p.finish, p.waiting, p.turnaround])

        writer.writerow([])

        # SJF
        writer.writerow(["SJF RESULT"])
        writer.writerow(["Process","Arrival","Burst","Start","Finish","Waiting","Turnaround"])
        for p in sjf_result:
            writer.writerow([p.pid, p.arrival, p.burst, p.start, p.finish, p.waiting, p.turnaround])

def draw_gantt(canvas, processes, y):
    x = 20
    scale = 15

    for p in processes:
        width = max(p.burst * scale, 20)
        canvas.create_rectangle(x, y, x + width, y + 30)
        canvas.create_text(x + width/2, y + 15, text=p.pid)
        canvas.create_text(x, y + 50, text=str(p.start))
        x += width

    canvas.create_text(x, y + 50, text=str(processes[-1].finish))

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling (FCFS & SJF)")

        # TOP
        top = tk.Frame(root)
        top.pack(pady=10)

        tk.Button(top, text="Load CSV", command=self.load_file, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Run", command=self.run, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Export CSV", command=self.export, width=12).pack(side=tk.LEFT, padx=5)

        self.algo = tk.StringVar(value="FCFS")
        tk.Radiobutton(top, text="FCFS", variable=self.algo, value="FCFS").pack(side=tk.LEFT)
        tk.Radiobutton(top, text="SJF", variable=self.algo, value="SJF").pack(side=tk.LEFT)

        # CANVAS
        self.canvas = tk.Canvas(root, width=900, height=500)
        self.canvas.pack()

        self.processes = []
        self.fcfs_result = []
        self.sjf_result = []

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path:
            self.processes = read_csv(path)
            messagebox.showinfo("OK", "Loaded file!")

    def run(self):
        if not self.processes:
            messagebox.showerror("Error", "Load file first!")
            return

        self.canvas.delete("all")

        self.fcfs_result = fcfs(copy.deepcopy(self.processes))
        self.sjf_result = sjf(copy.deepcopy(self.processes))

        if self.algo.get() == "FCFS":
            result = self.fcfs_result
            title = "FCFS"
        else:
            result = self.sjf_result
            title = "SJF"

        y_text = 20
        total_wt = 0

        for p in result:
            line = f"{p.pid} | Start:{p.start} | Finish:{p.finish} | Waiting:{p.waiting} | Turnaround:{p.turnaround}"
            self.canvas.create_text(450, y_text, text=line)
            y_text += 20
            total_wt += p.waiting

        avg_wt = total_wt / len(result)
        self.canvas.create_text(450, y_text + 10, text=f"Avg Waiting: {avg_wt:.2f}")

        self.canvas.create_text(100, 200, text=f"{title} Gantt Chart")
        draw_gantt(self.canvas, result, 220)

    def export(self):
        if not self.processes:
            messagebox.showerror("Error", "Load file first!")
            return

        # 👉 Tự động lưu cùng thư mục code
        path = "output.csv"

        # Luôn tính lại để đảm bảo có dữ liệu
        fcfs_result = fcfs(copy.deepcopy(self.processes))
        sjf_result = sjf(copy.deepcopy(self.processes))

        write_full_csv(path, fcfs_result, sjf_result)

        messagebox.showinfo("OK", f"Đã lưu file output.csv cùng thư mục code!")
#main
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
