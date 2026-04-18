# main.py
from views import MainView
from controllers import Controller
import customtkinter as ctk

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    controller = Controller()
    view = MainView(controller)
    controller.set_view(view)
    
    # Hiển thị dữ liệu mẫu khi khởi động.
    controller.load_sample_data()
    
    view.mainloop()
