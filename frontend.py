import customtkinter as ctk
from tkinter import ttk, messagebox
import requests
import webbrowser

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
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        self.tipwindow = tw = ctk.CTkToplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = ctk.CTkLabel(
            tw, 
            text=self.text, 
            justify='left',
            fg_color="#ffffe0",
            text_color="black",
            corner_radius=3
        )
        label.pack(padx=5, pady=5)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class BaseWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Monitoring Tugas Akhir")
        self.geometry("1250x600")
        self.configure(fg_color="white")

class ActionButton(ctk.CTkButton):
    def __init__(self, master, text, command):
        super().__init__(
            master,
            text=text,
            command=command,
            fg_color="#333",
            hover_color="#1a73e8",
            text_color="white",
            font=("Lucida Sans", 9, "bold"),
            cursor="hand2",
            corner_radius=5
        )

class MainApp(BaseWindow):
    def __init__(self):
        super().__init__()
        self.create_table()
        self.create_buttons()
        self.load_data()

    def create_table(self):
        columns = ('NIM', 'Nama', 'Judul', 'Matakuliah', 'Link Doc', 'Status', 'Komentar', 'Dosen')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=15)
        
        # Style configuration
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                      background="white",
                      foreground="black",
                      fieldbackground="white",
                      rowheight=25)
        style.map('Treeview', background=[('selected', '#1a73e8')])
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column('NIM', width=80, anchor='center')
            self.tree.column('Nama', width=120)
            self.tree.column('Judul', width=220)
            self.tree.column('Matakuliah', width=220)
            self.tree.column('Link Doc', width=180)
            self.tree.column('Status', width=100, anchor='center')
            self.tree.column('Komentar', width=200)
            self.tree.column('Dosen', width=100, anchor='center')
            
        self.tree.pack(pady=(10, 0), padx=10, fill='both', expand=True)
        ctk.CTkFrame(self, height=2, fg_color='gray').pack(fill='x', pady=(0, 10))

    def create_buttons(self):
        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(fill='x', pady=10, padx=10)

        # Left side buttons
        left_frame = ctk.CTkFrame(button_frame, fg_color="white")
        left_frame.pack(side='left', anchor='w')

        self.buttons = [
            ActionButton(left_frame, "Input TA", lambda: self.placeholder("input")),
            ActionButton(left_frame, "Edit TA", self.edit_ta_dialog),
            ActionButton(left_frame, "Hapus TA", self.delete_ta_dialog),
        ]
        for btn in self.buttons:
            btn.pack(side='left', padx=5, pady=5)

        # Right side buttons
        right_frame = ctk.CTkFrame(button_frame, fg_color="white")
        right_frame.pack(side='right', anchor='e')
        
        lbl_dosen = ctk.CTkLabel(right_frame, text="DOSEN :", text_color="black", fg_color="white")
        lbl_dosen.pack(side='left', padx=(20, 5))
        
        self.btn_periksa = ActionButton(right_frame, "Periksa", self.periksa_ta_dialog)
        self.btn_periksa.pack(side='left', padx=5)

    def placeholder(self, mode, data=None):
        win = ctk.CTkToplevel(self)
        win.title(f"{mode.capitalize()} tugas akhir")
        win.geometry("500x300")
        win.transient(self)
        win.grab_set()

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

            ctk.CTkLabel(win, text=f"Apakah anda yakin ingin menghapus TA\nNIM: {nim}?").pack(pady=20)
            ctk.CTkButton(win, text="HAPUS", command=submit_delete, fg_color="#d9534f", hover_color="#c9302c").pack(pady=10)
            return

        # Form frame
        form_frame = ctk.CTkFrame(win, fg_color="white")
        form_frame.pack(pady=20, padx=20, fill='both', expand=True)

        labels = ["NIM", "judul", "link_dokumen", "kode_mk", "status"]
        entries = {}

        for idx, label in enumerate(labels):
            ctk.CTkLabel(form_frame, text=label.capitalize()+":", anchor='w').grid(row=idx, column=0, sticky='w', padx=10, pady=5)

            if label == "status":
                entry = ctk.CTkComboBox(form_frame, values=["proposal", "revisi", "pengerjaan", "selesai"])
                entry.set("proposal")
            else:
                entry = ctk.CTkEntry(form_frame, width=250)

            entry.grid(row=idx, column=1, padx=10, pady=5)

            if data and label in data:
                if label == "status":
                    entry.set(data[label])
                else:
                    entry.insert(0, data[label])

            entries[label] = entry

        def submit():
            try:
                payload = {key: entry.get() for key, entry in entries.items()}
                
                if mode == "input":
                    url = "http://127.0.0.1:5000/tugas/add"
                    response = requests.post(url, json=payload)
                elif mode == "edit":
                    nim = payload["NIM"]
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

        ctk.CTkButton(form_frame, text="Submit", command=submit).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def get_selected_data(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data terlebih dahulu.")
            return None

        values = self.tree.item(selected[0])["values"]
        if not values or len(values) < 7:
            return None

        keys = ["NIM", "nama_mhs", "judul", "nama_mk", "link_dokumen", "status", "komentar", "nama_dosen"]
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

        win = ctk.CTkToplevel(self)
        win.title("Periksa Tugas Akhir")
        win.geometry("500x400")
        win.transient(self)
        win.grab_set()

        main_frame = ctk.CTkFrame(win, fg_color="white")
        main_frame.pack(pady=20, padx=20, fill='both', expand=True)

        # NIDN Field
        ctk.CTkLabel(main_frame, text="NIDN:", anchor='w').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        nidn_entry = ctk.CTkEntry(main_frame, width=300)
        nidn_entry.grid(row=0, column=1, padx=10, pady=5)

        # Komentar Field
        ctk.CTkLabel(main_frame, text="Komentar:", anchor='w').grid(row=1, column=0, sticky='nw', padx=10, pady=5)
        komentar_entry = ctk.CTkTextbox(main_frame, width=300, height=150)
        komentar_entry.grid(row=1, column=1, padx=10, pady=5)

        # Link Dokumen
        link = data.get("link_dokumen", "")
        if link:
            link_frame = ctk.CTkFrame(main_frame, fg_color="white")
            link_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='w')

            ctk.CTkLabel(link_frame, text="Link Dokumen:", anchor='w').pack(side='left')

            def open_link():
                webbrowser.open(link)

            def copy_link():
                self.clipboard_clear()
                self.clipboard_append(link)
                messagebox.showinfo("Disalin", "Link dokumen telah disalin ke clipboard.")

            link_btn = ctk.CTkButton(
                link_frame, 
                text=link[:30] + "..." if len(link) > 30 else link,
                command=open_link,
                fg_color="transparent",
                text_color="#1a73e8",
                hover_color="#e6f0fd",
                anchor='w'
            )
            link_btn.pack(side='left', padx=5)

            ctk.CTkButton(link_frame, text="Copy", command=copy_link, width=60).pack(side='left', padx=5)

        def submit_periksa():
            try:
                nim = data["NIM"]
                get_id_url = f"http://127.0.0.1:5000/tugas/by_nim/{nim}"
                res = requests.get(get_id_url)
                if res.status_code != 200:
                    messagebox.showerror("Gagal", "Data tugas tidak ditemukan.")
                    return

                id_tugas = res.json()['id_tugas']
                komentar = komentar_entry.get("1.0", "end").strip()
                payload = {
                    "NIDN": nidn_entry.get(),
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

        ctk.CTkButton(
            main_frame, 
            text="Submit", 
            command=submit_periksa
        ).grid(row=3, column=0, columnspan=2, pady=20)

    def load_data(self):
        try:
            response = requests.get("http://127.0.0.1:5000/monitoring/list")
            if response.status_code == 200:
                data = response.json()
                self.tree.delete(*self.tree.get_children())
                for item in data:
                    self.tree.insert('', 'end', values=(
                        item['NIM'], 
                        item['nama_mhs'], 
                        item['judul'], 
                        item['nama_mk'], 
                        item['link_dokumen'],
                        item['status'], 
                        item['komentar'], 
                        item['nama_dosen']
                    ))
            else:
                messagebox.showerror("Error", f"Gagal memuat data: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal terhubung ke server: {str(e)}")

if __name__ == '__main__':
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = MainApp()
    app.mainloop()