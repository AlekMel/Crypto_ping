import threading
import tkinter as tk
import time
from pythonping import ping

class PingApp:
    def __init__(self, master):
        self.master = master
        master.title("Ping Бирж")
        master.geometry("150x250")
        master.resizable(False, False)

        self.exchanges = {
            "Binance": "api.binance.com",
            "Bybit": "api.bybit.com",
            "OKX": "www.okx.com",
            "MEXC": "api.mexc.com",
            "Bitget": "api.bitget.com"
        }

        self.ping_labels = {}
        for exchange in self.exchanges:
            label = tk.Label(master, text=f"{exchange}: ...")
            label.pack(pady=5)
            self.ping_labels[exchange] = label

        self.start_button = tk.Button(master, text="Старт", command=self.toggle_ping)
        self.start_button.pack(pady=10)

        self.is_running = False
        self.ping_threads = {}

    def toggle_ping(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="Старт")
        else:
            self.is_running = True
            self.start_button.config(text="Стоп")
            for exchange in self.exchanges:
                thread = threading.Thread(target=self.continuous_ping, args=(exchange,))
                thread.start()
                self.ping_threads[exchange] = thread

    def continuous_ping(self, exchange):
        while self.is_running:
            try:
                response_list = ping(self.exchanges[exchange], count=1, timeout=2)
                if response_list.rtt_avg_ms is not None:
                    ping_time = round(response_list.rtt_avg_ms, 2)
                    self.master.after(0, self.update_label, exchange, f"{exchange}: {ping_time} мс")
                else:
                    self.master.after(0, self.update_label, exchange, f"{exchange}: Таймаут")
            except Exception as e:
                self.master.after(0, self.update_label, exchange, f"{exchange}: Ошибка")
            time.sleep(1)  # Пауза между пингами

    def update_label(self, exchange, text):
        self.ping_labels[exchange].config(text=text)

root = tk.Tk()
app = PingApp(root)
root.mainloop()