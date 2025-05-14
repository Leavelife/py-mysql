import tkinter as tk
from tkinter import ttk
import requests

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_pointerx() + 20
        y = self.widget.winfo_pointery() + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, justify='left',
            background="#ffffe0", relief='solid', borderwidth=1,
            font=("Segoe UI", 9)
        )
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

# ⬛ Base class untuk window (Encapsulation)
class BaseWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Monitoring Tugas Akhir")
        self.geometry("1000x500")
        self.configure(bg="white")

# ⬛ Class tombol (Inheritance)
class ActionButton(tk.Button):
    def __init__(self, master, text, command):
        super().__init__(
            master,
            text=text,
            command=command,
            bg="#444",           # tombol background (dark gray)
            fg="white",          # teks putih
            activebackground="#666",  # warna saat ditekan
            activeforeground="white",
            relief="flat",       # gaya flat
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=5,
            bd=0
        )

# ⬛ Main Window
class MainApp(BaseWindow):
    def __init__(self):
        super().__init__()
        self.create_table()
        self.create_buttons()
        self.load_data()

    def create_table(self):
        columns = ('NIM', 'Nama', 'Judul', 'Link Doc', 'Status', 'Komentar', 'Dosen')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column('NIM', width=80, anchor='center')
            self.tree.column('Nama', width=120)
            self.tree.column('Judul', width=220)
            self.tree.column('Link Doc', width=180)
            self.tree.column('Status', width=100, anchor='center')
            self.tree.column('Komentar', width=200)
            self.tree.column('Dosen', width=100, anchor='center')
        self.tree.pack(pady=(10, 0), padx=10, fill='both', expand=True)
        tk.Frame(self, height=2, bg='gray').pack(fill='x', pady=(0, 10))


    def create_buttons(self):
        frame = tk.Frame(self, bg="black")
        frame.pack(pady=10)

        self.buttons = [
            ActionButton(frame, "MHS", self.placeholder),
            ActionButton(frame, "Input TA", self.placeholder),
            ActionButton(frame, "Edit TA", self.placeholder),
            ActionButton(frame, "Hapus TA", self.placeholder),
            ActionButton(frame, "Dosen", self.placeholder),
            ActionButton(frame, "EDIT TA mahasiswa", self.placeholder)
        ]

        for btn in self.buttons:
            btn.pack(side=tk.LEFT, padx=8, pady=5)


    # ⬛ Contoh Polymorphism (semua tombol panggil fungsi ini tapi bisa diganti nanti)
    def placeholder(self):
        print("Fungsi belum diimplementasikan")
    
    def load_data(self):
        try:
            response = requests.get("http://127.0.0.1:5000/monitoring/list")
            data = response.json()
            for item in data:
                row_id = self.tree.insert('', tk.END, values=(
                    item['NIM'], item['nama_mhs'], item['judul'], item['link_dokumen'],
                    item['status'], item['komentar'], item['nama_dosen']
                ))
            self.tree.bind("<Motion>", self.on_mouse_move)

        except Exception as e:
            print(f"Gagal mengambil data: {e}")
    
    def show_tooltip(self, event, text):
        self.tooltip = Tooltip(self.tree, text)
        self.tooltip.show_tip()

    def hide_tooltip(self, event):
        if hasattr(self, 'tooltip'):
            self.tooltip.hide_tip()

    def on_mouse_move(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            row_id = self.tree.identify_row(event.y)
            col = self.tree.identify_column(event.x)

            if row_id:
                item = self.tree.item(row_id)['values']

                # Ambil teks sesuai kolom
                col_index = int(col.replace('#', '')) - 1
                if 0 <= col_index < len(item):
                    text = str(item[col_index])

                    # Tampilkan tooltip jika beda dari sebelumnya
                    if getattr(self, 'last_tooltip_text', None) != text:
                        if hasattr(self, 'tooltip'):
                            self.tooltip.hide_tip()
                        self.tooltip = Tooltip(self.tree, text)
                        self.tooltip.show_tip()
                        self.last_tooltip_text = text
        else:
            if hasattr(self, 'tooltip'):
                self.tooltip.hide_tip()
                self.last_tooltip_text = None

# ⬛ Run App
if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
