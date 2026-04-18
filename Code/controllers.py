# controllers.py
import pandas as pd
import re
from tkinter import filedialog, messagebox
from models import SchedulerModel, Process

class Controller:
    def __init__(self):
        self.model = SchedulerModel()
        self.view = None
        self.processes = []

    def set_view(self, view):
        self.view = view

    def load_sample_data(self):
        
        self.processes.clear()
        sample_processes = [
            Process(1, 0, 24),
            Process(2, 3, 3),
            Process(3, 6, 3),
            Process(4, 9, 6)
        ]
        self.processes.extend(sample_processes)
        self.refresh_process_list()
        if self.view:
            self.view.algo_menu.set("FCFS")

    def parse_processes_from_text(self, text):
        processes = []
        lines = text.strip().split('\n')
        for i, line in enumerate(lines[1:], 1):
            if not line.strip() or line.startswith('-'):
                continue
            parts = re.split(r'\s+', line.strip())
            if len(parts) >= 3:
                try:
                    arrival = int(parts[1])
                    burst = int(parts[2])
                    processes.append(Process(i, arrival, burst))
                except ValueError:
                    continue
        return processes

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            df = pd.read_csv(file_path)
            if not all(col in df.columns for col in ['ID', 'Arrival', 'Burst']):
                messagebox.showerror("Lỗi", "File CSV cần có cột: ID, Arrival, Burst")
                return

            self.processes.clear()
            for _, row in df.iterrows():
                p = Process(int(row['ID']), int(row['Arrival']), int(row['Burst']))
                self.processes.append(p)

            self.refresh_process_list()
            messagebox.showinfo("Thành công", f"Đã nhập {len(self.processes)} tiến trình.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không đọc được file:\n{str(e)}")

    def refresh_process_list(self):
        if not self.processes:
            self.view.update_process_list("ID\tArrival\tBurst\n")
            return

        text = "ID\tArrival\tBurst\n" + "-"*25 + "\n"
        for p in self.processes:
            text += f"P{p.pid}\t{p.arrival_time}\t{p.burst_time}\n"
        self.view.update_process_list(text)

    def run_scheduler(self):
        if not self.processes:
            text = self.view.process_textbox.get("0.0", "end").strip()
            if text:
                self.processes = self.parse_processes_from_text(text)
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập dữ liệu tiến trình!")
                return

        if len(self.processes) < 1:
            messagebox.showwarning("Cảnh báo", "Cần ít nhất 1 tiến trình!")
            return

        algo_name = self.view.algo_menu.get()

        try:
            if algo_name == "FCFS":
                result, timeline = self.model.simulate_fcfs(self.processes[:])
            else:
                result, timeline = self.model.simulate_sjf_non_preemptive(self.processes[:])

            avg_tat, avg_wt = self.model.calculate_average(result)

            self.view.update_summary(algo_name, avg_tat, avg_wt, len(result))
            self.view.update_result_table(self._format_result(result))
            self.view.draw_gantt_chart(timeline)

            messagebox.showinfo("Hoàn tất", 
                              f"Thuật toán {algo_name} chạy thành công!\n"
                              f"TAT TB: {avg_tat}ms | WT TB: {avg_wt}ms")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi chạy thuật toán:\n{str(e)}")

    def _format_result(self, processes):
        text = "ID\tArr\tBurst\tStart\tFinish\tTAT\tWT\n"
        text += "-" * 50 + "\n"
        for p in processes:
            text += (f"P{p.pid}\t{p.arrival_time}\t{p.burst_time}\t"
                    f"{p.start_time}\t{p.finish_time}\t"
                    f"{p.turnaround_time}\t{p.waiting_time}\n")
        text += "-" * 50 + "\n"
        return text

    def reset(self):
        self.processes.clear()
        self.view.update_process_list("")
        self.view.update_result_table("")
        self.view.update_summary("--", "--", "--", 0)
        self.view.gantt_canvas.delete("all")
        self.view.algo_menu.set("FCFS")

    def export_csv(self):
        if not self.processes:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xuất!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if file_path:
            try:
                df = pd.DataFrame([{
                    'ID': p.pid,
                    'Arrival': p.arrival_time,
                    'Burst': p.burst_time,
                    'Start': getattr(p, 'start_time', 0),
                    'Finish': getattr(p, 'finish_time', 0),
                    'TAT': getattr(p, 'turnaround_time', 0),
                    'WT': getattr(p, 'waiting_time', 0)
                } for p in self.processes])
                df.to_csv(file_path, index=False)
                messagebox.showinfo("Thành công", f"Đã xuất {len(self.processes)} tiến trình ra file.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không xuất được file:\n{str(e)}")
