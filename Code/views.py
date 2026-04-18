# views.py
import customtkinter as ctk

class MainView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("Mô phỏng Thuật toán Lập lịch CPU - FCFS và SJF")
        self.geometry("1280x750")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.build_sidebar()
        self.build_main_content()
        self.build_summary_panel()

    def build_sidebar(self):
        sidebar = ctk.CTkFrame(self)
        sidebar.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")
        sidebar.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(sidebar, text="LẬP LỊCH CPU", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        ctk.CTkLabel(sidebar, text="Thuật toán:", 
                    font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(20,5))
        self.algo_menu = ctk.CTkOptionMenu(sidebar, values=["FCFS", "SJF (Non-preemptive)"], 
                                         width=200, height=35)
        self.algo_menu.pack(pady=5, padx=20)

        ctk.CTkLabel(sidebar, text="Danh sách tiến trình:", 
                    font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(20,5))
       
        self.process_textbox = ctk.CTkTextbox(sidebar, height=200, font=ctk.CTkFont(size=12))
        self.process_textbox.pack(pady=8, padx=20, fill="x")

        btn_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        btn_frame.pack(pady=15, padx=20, fill="x")

        self.btn_import = ctk.CTkButton(btn_frame, text="Nhập file CSV",
                                      command=self.controller.import_csv, height=35)
        self.btn_import.pack(side="left", padx=5, fill="x", expand=True)

        self.btn_run = ctk.CTkButton(btn_frame, text="Lập lịch",
                                   fg_color="#22c55e", hover_color="#16a34a",
                                   command=self.controller.run_scheduler, height=35)
        self.btn_run.pack(side="right", padx=5, fill="x", expand=True)

        self.btn_reset = ctk.CTkButton(sidebar, text="Làm mới", fg_color="gray",
                                     hover_color="#6b7280", command=self.controller.reset)
        self.btn_reset.pack(pady=10, padx=20, fill="x")
      
        self.btn_export = ctk.CTkButton(sidebar, text="Xuất file CSV",
                                      command=self.controller.export_csv)
        self.btn_export.pack(pady=5, padx=20, fill="x")

    def build_main_content(self):
        main = ctk.CTkFrame(self)
        main.grid(row=0, column=1, padx=12, pady=12, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(main, text="Biểu đồ Gantt Chart",
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)

        self.gantt_canvas = ctk.CTkCanvas(main, height=180, bg="#1a1d23", highlightthickness=0)
        self.gantt_canvas.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(main, text="Bảng kết quả chi tiết",
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(25,10))

        self.result_textbox = ctk.CTkTextbox(main, height=250, font=ctk.CTkFont(size=12))
        self.result_textbox.pack(fill="both", padx=20, pady=10, expand=True)

    def build_summary_panel(self):
        summary = ctk.CTkFrame(self)
        summary.grid(row=0, column=2, padx=12, pady=12, sticky="nsew")

        ctk.CTkLabel(summary, text="Tóm tắt kết quả",
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        self.summary_label = ctk.CTkLabel(summary,
            text="Thuật toán: --\nTAT trung bình: -- ms\nWT trung bình: -- ms\nSố tiến trình: --",
            justify="left", font=ctk.CTkFont(size=14))
        self.summary_label.pack(pady=40, padx=20)

    # CẬP NHẬT GIAO DIỆN 
    def update_process_list(self, text):
        self.process_textbox.delete("0.0", "end")
        self.process_textbox.insert("0.0", text)

    def update_result_table(self, text):
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", text)

    def update_summary(self, algo_name, avg_tat, avg_wt, num_processes=0):
        text = f"""Thuật toán: {algo_name}
TAT trung bình: {avg_tat} ms
WT trung bình: {avg_wt} ms
Số tiến trình: {num_processes}"""
        self.summary_label.configure(text=text)

    def draw_gantt_chart(self, timeline):
        canvas = self.gantt_canvas
        canvas.delete("all")

        if not timeline:
            canvas.create_text(400, 80, text="Chưa có dữ liệu để vẽ Gantt Chart",
                             fill="#94a3b8", font=("Arial", 14))
            return

        y = 35
        bar_height = 60
        scale = 18
        left_margin = 70
        right_margin = 60

        max_time = max(end for _, end, _ in timeline)
        canvas_width = left_margin + max_time * scale + right_margin
        canvas.configure(width=max(900, canvas_width), height=180)

        canvas.create_text(left_margin, 15, text="Biểu đồ Gantt Chart",
                         fill="white", font=("Arial", 16, "bold"), anchor="w")
       
        canvas.create_line(left_margin, y + bar_height + 30,
                         left_margin + max_time * scale, y + bar_height + 30,
                         fill="white", width=2)

        step = max(1, max_time // 12)
        for t in range(0, max_time + 1, step):
            x = left_margin + t * scale
            canvas.create_line(x, y + bar_height + 25, x, y + bar_height + 35,
                             fill="#94a3b8", width=1)
            canvas.create_text(x, y + bar_height + 50, text=str(t),
                             fill="#94a3b8", font=("Arial", 11), anchor="n")

        colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#f97316", "#ec4899"]
        for i, (start, end, pid) in enumerate(timeline):
            x1 = left_margin + start * scale
            x2 = left_margin + end * scale
            color = colors[i % len(colors)]

            canvas.create_rectangle(x1, y, x2, y + bar_height,
                                  fill=color, outline="white", width=2)
           
            canvas.create_text((x1 + x2) // 2, y + bar_height//2,
                             text=f"P{pid}", fill="white",
                             font=("Arial", 14, "bold"))

            canvas.create_text(x1-5, y - 15, text=str(start),
                             fill="#94a3b8", font=("Arial", 10), anchor="e")
            if (end - start) >= 4:
                canvas.create_text(x2+5, y - 15, text=str(end),
                                 fill="#94a3b8", font=("Arial", 10), anchor="w")

        canvas.create_text(canvas_width - 80, 15, text=f"Tổng: {max_time}ms",
                         fill="#10b981", font=("Arial", 13, "bold"))
