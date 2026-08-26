import os
import sys
import shutil
import string
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_path, relative_path)

def get_removable_drives():
    drives = []
    if sys.platform == 'win32':
        import ctypes
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drive_path = f"{letter}:\\"
                drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive_path)
                # DRIVE_REMOVABLE = 2, DRIVE_FIXED = 3
                if drive_type == 2:
                    drives.append(f"{letter}: (Cartão SD / Removível)")
                elif drive_type == 3 and letter not in ['C']:
                    drives.append(f"{letter}: (Disco)")
            bitmask >>= 1
    return drives

class InstallerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pokémon X & Y - No Trade Evolutions Installer")
        self.geometry("620x540")
        self.resizable(False, False)
        
        # Color theme
        self.bg_color = "#1e1e2e"
        self.card_bg = "#2b2b3d"
        self.accent_color = "#e056fd"
        self.btn_color = "#0984e3"
        self.text_color = "#f5f6fa"
        self.subtext_color = "#a4b0be"
        self.success_color = "#00b894"
        
        self.configure(bg=self.bg_color)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg=self.bg_color)
        header_frame.pack(fill="x", padx=25, pady=(20, 10))
        
        title_lbl = tk.Label(header_frame, text="⚡ Pokémon No-Trade Evolutions", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg=self.bg_color)
        title_lbl.pack(anchor="w")
        
        subtitle_lbl = tk.Label(header_frame, text="Instalador Oficial para Nintendo 3DS e Emuladores (Citra / Azahar)", font=("Segoe UI", 9), fg=self.subtext_color, bg=self.bg_color)
        subtitle_lbl.pack(anchor="w", pady=(2, 0))
        
        # Tabs / Card Frame
        card = tk.Frame(self, bg=self.card_bg, highlightbackground="#3d3d5c", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=25, pady=10)
        
        # Mode Selection
        self.mode_var = tk.StringVar(value="3ds")
        
        mode_frame = tk.Frame(card, bg=self.card_bg)
        mode_frame.pack(fill="x", padx=20, pady=(15, 10))
        
        rb1 = tk.Radiobutton(mode_frame, text="🎮 Console Nintendo 3DS (Luma3DS)", variable=self.mode_var, value="3ds", command=self.on_mode_change,
                             font=("Segoe UI", 10, "bold"), fg="#ffffff", bg=self.card_bg, selectcolor=self.bg_color, activebackground=self.card_bg, activeforeground="#ffffff")
        rb1.pack(side="left", padx=(0, 20))
        
        rb2 = tk.Radiobutton(mode_frame, text="💻 Emulador (Citra / Azahar / Lime3DS)", variable=self.mode_var, value="emu", command=self.on_mode_change,
                             font=("Segoe UI", 10, "bold"), fg="#ffffff", bg=self.card_bg, selectcolor=self.bg_color, activebackground=self.card_bg, activeforeground="#ffffff")
        rb2.pack(side="left")
        
        # Separator
        sep = tk.Frame(card, height=1, bg="#3d3d5c")
        sep.pack(fill="x", padx=20, pady=5)
        
        # Target path selection frame
        self.path_frame = tk.Frame(card, bg=self.card_bg)
        self.path_frame.pack(fill="x", padx=20, pady=10)
        
        self.path_label = tk.Label(self.path_frame, text="Selecione o Cartão SD do seu 3DS:", font=("Segoe UI", 10), fg=self.text_color, bg=self.card_bg)
        self.path_label.pack(anchor="w", pady=(0, 5))
        
        input_subframe = tk.Frame(self.path_frame, bg=self.card_bg)
        input_subframe.pack(fill="x")
        
        self.drives = get_removable_drives()
        self.drive_var = tk.StringVar()
        if self.drives:
            self.drive_var.set(self.drives[0])
        else:
            self.drive_var.set("Nenhum cartão SD detectado automaticamente")
            
        self.drive_combo = ttk.Combobox(input_subframe, textvariable=self.drive_var, values=self.drives, state="readonly", font=("Segoe UI", 10))
        self.drive_combo.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(input_subframe, text="Procurar...", font=("Segoe UI", 9), bg="#4834d4", fg="#ffffff", relief="flat", padx=12, pady=4, command=self.browse_folder, cursor="hand2")
        browse_btn.pack(side="right")
        
        # Info Box
        self.info_box = tk.Label(card, text="", font=("Segoe UI", 9), fg=self.subtext_color, bg="#202030", justify="left", padx=12, pady=10, relief="flat", anchor="w")
        self.info_box.pack(fill="x", padx=20, pady=10)
        self.update_info_text()
        
        # Action Button
        self.install_btn = tk.Button(card, text="✨ INSTALAR MOD AGORA", font=("Segoe UI", 11, "bold"), bg=self.success_color, fg="#ffffff", relief="flat", pady=10, command=self.do_install, cursor="hand2")
        self.install_btn.pack(fill="x", padx=20, pady=(5, 15))
        
        # Status Label
        self.status_lbl = tk.Label(self, text="Pronto para instalar.", font=("Segoe UI", 9), fg=self.subtext_color, bg=self.bg_color)
        self.status_lbl.pack(pady=(0, 15))

    def on_mode_change(self):
        if self.mode_var.get() == "3ds":
            self.path_label.config(text="Selecione o Cartão SD do seu 3DS:")
            self.drive_combo.config(values=get_removable_drives())
        else:
            self.path_label.config(text="Selecione a pasta do Emulador ou Mods:")
            appdata = os.getenv('APPDATA', '')
            candidates = []
            for emu in ['Citra', 'Azahar', 'Lime3DS']:
                p = os.path.join(appdata, emu, 'load', 'mods')
                if os.path.exists(p):
                    candidates.append(p)
                else:
                    candidates.append(os.path.join(appdata, emu))
            self.drive_combo.config(values=candidates)
            if candidates:
                self.drive_var.set(candidates[0])
            else:
                self.drive_var.set("Selecione a pasta de Mods do Emulador")
        self.update_info_text()

    def update_info_text(self):
        if self.mode_var.get() == "3ds":
            self.info_box.config(text="📌 Instruções para Nintendo 3DS:\n1. O instalador copiará os arquivos para SD:/luma/titles/...\n2. Ligue o 3DS segurando [SELECT] e marque '(x) Enable game patching'.\n3. Salve com [START] e abra seu Pokémon X ou Y normalmente!")
        else:
            self.info_box.config(text="📌 Instruções para Emulador (Citra / Azahar / Lime3DS):\n1. O instalador copiará a pasta romfs para a pasta de mods do jogo.\n2. Inicie o Pokémon X ou Y no emulador e as evoluções já estarão ativas!")

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Selecione a pasta de destino")
        if folder:
            self.drive_var.set(folder)

    def do_install(self):
        dest = self.drive_var.get()
        if not dest or "Nenhum" in dest or "Selecione" in dest:
            messagebox.showerror("Erro", "Por favor selecione a unidade ou pasta de destino.")
            return

        # Extract drive letter or folder path
        if len(dest) >= 2 and dest[1] == ':':
            if len(dest) > 3 and '(' in dest:
                dest_path = f"{dest[0]}:\\"
            else:
                dest_path = dest
        else:
            dest_path = dest

        try:
            # Source of files
            source_pkg = resource_path("Mod-Package")
            if not os.path.exists(source_pkg):
                # Fallback to local script relative dir
                source_pkg = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Mod-Package"))

            if self.mode_var.get() == "3ds":
                src_luma = os.path.join(source_pkg, "3DS_Luma3DS", "luma")
                dst_luma = os.path.join(dest_path, "luma")
                if not os.path.exists(src_luma):
                    raise FileNotFoundError(f"Arquivos do mod não encontrados em {src_luma}")
                
                shutil.copytree(src_luma, dst_luma, dirs_exist_ok=True)
                self.status_lbl.config(text="✅ Mod instalado com sucesso no Cartão SD!", fg=self.success_color)
                messagebox.showinfo("Sucesso!", f"Mod instalado com sucesso no Cartão SD ({dest_path})!\n\nLembre-se:\nLigue o seu 3DS segurando SELECT e ative a opção '(x) Enable game patching'.")
            else:
                # Emulator
                src_emu_x = os.path.join(source_pkg, "Citra_Lime3DS", "Pokemon_X", "romfs")
                src_emu_y = os.path.join(source_pkg, "Citra_Lime3DS", "Pokemon_Y", "romfs")
                
                # If destination is already the mods folder or root emulator folder
                dst_x = os.path.join(dest_path, "0004000000055D00", "romfs")
                dst_y = os.path.join(dest_path, "0004000000055E00", "romfs")
                
                shutil.copytree(src_emu_x, dst_x, dirs_exist_ok=True)
                shutil.copytree(src_emu_y, dst_y, dirs_exist_ok=True)
                
                self.status_lbl.config(text="✅ Mod instalado com sucesso no Emulador!", fg=self.success_color)
                messagebox.showinfo("Sucesso!", "Mod instalado com sucesso para Pokémon X e Pokémon Y no Emulador!")

        except Exception as e:
            messagebox.showerror("Erro na Instalação", f"Ocorreu um erro ao copiar os arquivos:\n{str(e)}")
            self.status_lbl.config(text="❌ Falha na instalação.", fg="#e74c3c")

if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()
