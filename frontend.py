import tkinter as tk
from tkinter import ttk, messagebox
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

# Base class untuk window (Encapsulation)
class BaseWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Monitoring Tugas Akhir")
        self.geometry("1000x500")
        self.configure(bg="white")

# Class tombol (Inheritance)
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

# Main Window
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
        __frame = tk.Frame(self, bg="white")
        __frame.pack(fill=tk.X, pady=10, padx=10)

        left_frame = tk.Frame(__frame, bg="white")
        left_frame.pack(side=tk.LEFT, anchor=tk.W)

        self.buttons = [
            ActionButton(__frame, "Input TA", lambda: self.placeholder("input")),
            ActionButton(__frame, "Edit TA", self.edit_ta_dialog),
            ActionButton(__frame, "Hapus TA", self.delete_ta_dialog),
        ]
        for btn in self.buttons:
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        right_frame = tk.Frame(__frame, bg="white")
        right_frame.pack(side=tk.RIGHT, anchor=tk.E)
        
        # Label dan tombol di kanan
        lbl_dosen = tk.Label(right_frame, text="DOSEN :", bg="white", fg="black")
        lbl_dosen.pack(side=tk.LEFT, padx=(20, 5))
        
        self.btn_periksa = ActionButton(right_frame, "Periksa", self.periksa_ta_dialog)
        self.btn_periksa.pack(side=tk.LEFT, padx=5)

    # Contoh Polymorphism (semua tombol panggil fungsi ini tapi bisa diganti nanti)
    def placeholder(self, mode, data=None):
        win = tk.Toplevel(self)
        win.title(f"{mode.capitalize()} tugas akhir")

        if mode == "delete":
            for widget in win.winfo_children():
                widget.destroy()

            nim = data.get("NIM", "________")

            def submit_delete():
                try:
                    get_id_url = f"http://127.0.0.1:5000/tugas/by_nim/{nim}"
                    res = requests.get(get_id_url)
                    if res.status_code == 200:
                        id_tugas = res.json()['id_tugas']
                        url = f"http://127.0.0.1:5000/tugas/delete/{id_tugas}"
                        response = requests.delete(url)
                    else:
                        messagebox.showerror("Gagal", f"Data tidak ditemukan untuk NIM {nim}")
                        return

                    if response.status_code in [200, 201]:
                        messagebox.showinfo("Sukses", "Hapus berhasil")
                        self.tree.delete(*self.tree.get_children())
                        self.load_data()
                        win.destroy()
                    else:
                        messagebox.showerror("Gagal", f"Gagal hapus: {response.text}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            tk.Label(win, text=f"Apakah anda yakin ingin menghapus TA\nNIM: {nim}?").pack(pady=10)
            tk.Button(win, text="HAPUS", command=submit_delete).pack(pady=10)
            return  # <-- PENTING: jangan lanjut ke bawah

        # selain delete
        labels = ["NIM", "judul", "link_dokumen", "kode_mk"]
        entries = {}

        for idx, label in enumerate(labels):
            tk.Label(win, text=label).grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            entry = tk.Entry(win, width=30)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            if data and label in data:
                entry.insert(0, data[label])
            entries[label] = entry

        def submit():
            try:
                payload = {key: entry.get() for key, entry in entries.items()}
                
                if mode == "input":
                    url = "http://127.0.0.1:5000/tugas/add"
                    response = requests.post(url, json=payload)
                elif mode == "edit":
                    nim = payload["NIM"]  # Perbaikan di sini
                    url = f"http://127.0.0.1:5000/tugas/update/{nim}"
                    response = requests.put(url, json=payload)

                if response.status_code in [200, 201]:
                    messagebox.showinfo("Sukses", f"{mode.capitalize()} berhasil")
                    self.tree.delete(*self.tree.get_children())
                    self.load_data()
                    win.destroy()
                else:
                    messagebox.showerror("Gagal", f"Gagal {mode}: {response.text}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Submit", command=submit).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def get_selected_data(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data terlebih dahulu.")
            return None

        values = self.tree.item(selected[0])["values"]
        if not values or len(values) < 7:
            return None

        # Kolom: 'NIM', 'Nama', 'Judul', 'Link Doc', 'Status', 'Komentar', 'Dosen'
        keys = ["NIM", "nama_mhs", "judul", "link_dokumen", "status", "komentar", "nama_dosen"]
        return dict(zip(keys, values))

    def edit_ta_dialog(self):
        data = self.get_selected_data()
        if data:
            self.placeholder("edit", data)

    def delete_ta_dialog(self):
        data = self.get_selected_data()
        if data:
            self.placeholder("delete", data)

    def periksa_ta_dialog(self):
        data = self.get_selected_data()
        if not data:
            return

        win = tk.Toplevel(self)
        win.title("Periksa Tugas Akhir")

        labels = ["NIDN", "status", "komentar"]
        entries = {}

        for idx, label in enumerate(labels):
            tk.Label(win, text=label).grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            if label == "status":
                entry = ttk.Combobox(win, values=["proposal", "revisi", "pengerjaan", "selesai"])
                entry.current(0)
            elif label == "komentar":
                entry = tk.Text(win, width=40, height=5)
            else:
                entry = tk.Entry(win, width=30)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[label] = entry
        
         # 🔗 Tampilkan link dokumen
        link = data.get("link_dokumen", "")
        if link:
            link_frame = tk.Frame(win)
            link_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)

            tk.Label(link_frame, text="Link Dokumen:").pack(side=tk.LEFT)
            link_label = tk.Label(link_frame, text=link, fg="blue", cursor="hand2", wraplength=300)
            link_label.pack(side=tk.LEFT, padx=5)

            def open_link(event=None):
                import webbrowser
                webbrowser.open(link)

            def copy_link():
                self.clipboard_clear()
                self.clipboard_append(link)
                messagebox.showinfo("Disalin", "Link dokumen telah disalin ke clipboard.")

            link_label.bind("<Button-1>", open_link)

            tk.Button(link_frame, text="Copy Link", command=copy_link).pack(side=tk.LEFT, padx=10)

        def submit_periksa():
            try:
                # Ambil id_tugas dari NIM
                nim = data["NIM"]
                get_id_url = f"http://127.0.0.1:5000/tugas/by_nim/{nim}"
                res = requests.get(get_id_url)
                if res.status_code != 200:
                    messagebox.showerror("Gagal", "Data tugas tidak ditemukan.")
                    return

                id_tugas = res.json()['id_tugas']

                # Ambil input
                komentar = entries["komentar"].get("1.0", "end").strip()
                payload = {
                    "NIDN": entries["NIDN"].get(),
                    "status": entries["status"].get(),
                    "komentar": komentar
                }

                url = f"http://127.0.0.1:5000/monitoring/update/{id_tugas}"
                response = requests.put(url, json=payload)

                if response.status_code == 200:
                    messagebox.showinfo("Sukses", "Data berhasil diperiksa.")
                    self.tree.delete(*self.tree.get_children())
                    self.load_data()
                    win.destroy()
                else:
                    messagebox.showerror("Gagal", f"Gagal periksa: {response.text}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Submit", command=submit_periksa).grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

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

# Run App
if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
