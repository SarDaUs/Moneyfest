import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models import DeadlockEngine

class DeadlockSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deadlock Simulator & Banker's Algorithm (Pro Edition)")
        self.root.geometry("1400x900")

        self.engine = DeadlockEngine()

        self.alloc_entries = []
        self.max_entries = []
        self.prio_entries = []
        self.cost_entries = []

        self.is_dark_mode = False
        self.execution_steps = []
        self.current_step_idx = 0

        self.setup_ui()

    def setup_ui(self):
        # Stil Yönetimi
        self.style = ttk.Style()
        self.apply_theme()

        self.left_frame = ttk.Frame(self.root, padding="10")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Üst Başlık ve Dark Mode Butonu
        top_bar = ttk.Frame(self.left_frame)
        top_bar.pack(fill=tk.X, pady=5)
        ttk.Label(top_bar, text="Deadlock Control Center", font=("Helvetica", 13, "bold")).pack(side=tk.LEFT)
        self.theme_btn = ttk.Button(top_bar, text="🌙 Dark Mode", command=self.toggle_theme)
        self.theme_btn.pack(side=tk.RIGHT)

        # --- PRESET SCENARIOS ---
        preset_group = ttk.LabelFrame(self.left_frame, text=" Hazır Senaryolar (Presets) ", padding="5")
        preset_group.pack(fill=tk.X, pady=4)
        
        self.preset_cb = ttk.Combobox(preset_group, values=[
            "Deadlock (Kilitlenme Senaryosu)",
            "Safe State (Güvenli Senaryo)",
            "High Starvation (Kaynak Açlığı)"
        ], state="readonly")
        self.preset_cb.current(0)
        self.preset_cb.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        ttk.Button(preset_group, text="Yükle", command=self.load_preset).pack(side=tk.RIGHT, padx=2)

        # --- BOYUT AYARLARI ---
        dim_group = ttk.LabelFrame(self.left_frame, text=" Boyut Ayarları ", padding="5")
        dim_group.pack(fill=tk.X, pady=4)
        dim_row = ttk.Frame(dim_group)
        dim_row.pack(fill=tk.X, pady=2)
        ttk.Label(dim_row, text="Süreç (P):").pack(side=tk.LEFT, padx=2)
        self.p_spin = ttk.Spinbox(dim_row, from_=1, to=6, width=3)
        self.p_spin.set(str(self.engine.num_processes))
        self.p_spin.pack(side=tk.LEFT, padx=2)
        ttk.Label(dim_row, text="Kaynak (R):").pack(side=tk.LEFT, padx=2)
        self.r_spin = ttk.Spinbox(dim_row, from_=1, to=5, width=3)
        self.r_spin.set(str(self.engine.num_resources))
        self.r_spin.pack(side=tk.LEFT, padx=2)
        ttk.Button(dim_row, text="Uygula", command=self.apply_dimensions).pack(side=tk.LEFT, padx=5)

        # --- MATRİS GİRİŞİ ---
        self.input_group = ttk.LabelFrame(self.left_frame, text=" Matris Veri Girişi ", padding="5")
        self.input_group.pack(fill=tk.X, pady=5)
        self.create_matrix_inputs()

        ttk.Button(self.input_group, text="Matris Değerlerini Güncelle", command=self.update_values_from_ui).pack(fill=tk.X, pady=4)

        # --- ADIM ADIM ÇALIŞTIRMA (STEP ENGINE) ---
        step_group = ttk.LabelFrame(self.left_frame, text=" Adım Adım Algoritma Yürütme ", padding="5")
        step_group.pack(fill=tk.X, pady=5)

        step_btn_frame = ttk.Frame(step_group)
        step_btn_frame.pack(fill=tk.X)
        ttk.Button(step_btn_frame, text="▶️ Adım Simülasyonunu Başlat", command=self.start_step_execution).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        ttk.Button(step_btn_frame, text="⏭️ Sonraki Adım", command=self.next_step_execution).pack(side=tk.RIGHT, padx=2)

        # AKILLI ÇÖZÜM STRATEJİLERİ
        strategy_group = ttk.LabelFrame(self.left_frame, text=" Akıllı Kilitlenme Çözümü ", padding="5")
        strategy_group.pack(fill=tk.X, pady=5)

        self.strategy_cb = ttk.Combobox(strategy_group, values=[
            "Victim: Max Allocation (En Çok Kaynak Tüketen)",
            "Lowest Priority (En Düşük Öncelikliyi Öldür)",
            "Lowest Termination Cost (En Az Maliyetliyi Kurban Et)",
            "Resource Preemption (Kaynak Geri Alma)"
        ], state="readonly")
        self.strategy_cb.current(0)
        self.strategy_cb.pack(fill=tk.X, pady=4)
        ttk.Button(strategy_group, text="Seçilen Stratejiyle Çöz", command=self.resolve_deadlock).pack(fill=tk.X, pady=2)

        # RAPOR VE GENEL BUTONLAR
        ttk.Button(self.left_frame, text="📄 Raporu Dosyaya Aktır (.txt)", command=self.export_report).pack(fill=tk.X, pady=4)

        # LOG EKRANI
        ttk.Label(self.left_frame, text="Sistem Durum Logu:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(5, 2))
        self.log_text = tk.Text(self.left_frame, width=42, height=8, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # SAĞ PANEL - GRAFİK
        self.right_frame = ttk.Frame(self.root, padding="10")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.log("Sistem hazır. Dark Mode, Presets & Step Engine eklendi.")
        self.draw_graph()

    def apply_theme(self):
        bg_color = "#1e1e1e" if self.is_dark_mode else "#f0f0f0"
        fg_color = "#ffffff" if self.is_dark_mode else "#000000"
        
        self.root.configure(bg=bg_color)
        self.style.theme_use('clam')
        self.style.configure('.', background=bg_color, foreground=fg_color)
        self.style.configure('TLabelframe', background=bg_color, foreground=fg_color)
        self.style.configure('TLabelframe.Label', background=bg_color, foreground=fg_color)
        self.style.configure('TLabel', background=bg_color, foreground=fg_color)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.theme_btn.config(text="☀️ Light Mode" if self.is_dark_mode else "🌙 Dark Mode")
        self.apply_theme()
        
        log_bg = "#2d2d2d" if self.is_dark_mode else "#f4f4f4"
        log_fg = "#00ffcc" if self.is_dark_mode else "#000000"
        self.log_text.config(bg=log_bg, fg=log_fg)
        
        self.draw_graph()

    def create_matrix_inputs(self):
        for widget in self.input_group.winfo_children():
            widget.destroy()

        res_labels = ", ".join([f"R{j}" for j in range(self.engine.num_resources)])
        ttk.Label(self.input_group, text=f"Allocation [{res_labels}] | Max Need | Prio | Cost", font=("Helvetica", 8, "bold")).pack(anchor=tk.W)
        
        self.alloc_entries = []
        self.max_entries = []
        self.prio_entries = []
        self.cost_entries = []

        for i in range(self.engine.num_processes):
            row_frame = ttk.Frame(self.input_group)
            row_frame.pack(fill=tk.X, pady=1)
            ttk.Label(row_frame, text=f"P{i}:", width=3).pack(side=tk.LEFT)
            
            # Allocation
            alloc_row = []
            for j in range(self.engine.num_resources):
                e = ttk.Entry(row_frame, width=3)
                e.insert(0, str(self.engine.allocation[i][j]))
                e.pack(side=tk.LEFT, padx=1)
                alloc_row.append(e)
            self.alloc_entries.append(alloc_row)

            ttk.Label(row_frame, text="|").pack(side=tk.LEFT, padx=2)

            # Max Need
            max_row = []
            for j in range(self.engine.num_resources):
                e = ttk.Entry(row_frame, width=3)
                e.insert(0, str(self.engine.max_need[i][j]))
                e.pack(side=tk.LEFT, padx=1)
                max_row.append(e)
            self.max_entries.append(max_row)

            ttk.Label(row_frame, text="|").pack(side=tk.LEFT, padx=2)

            # Priority & Cost
            pe = ttk.Entry(row_frame, width=3)
            pe.insert(0, str(self.engine.priorities[i]))
            pe.pack(side=tk.LEFT, padx=1)
            self.prio_entries.append(pe)

            ce = ttk.Entry(row_frame, width=4)
            ce.insert(0, str(self.engine.costs[i]))
            ce.pack(side=tk.LEFT, padx=1)
            self.cost_entries.append(ce)

    def load_preset(self):
        preset_name = self.preset_cb.get()
        self.engine.load_preset(preset_name)
        self.p_spin.set(str(self.engine.num_processes))
        self.r_spin.set(str(self.engine.num_resources))
        self.create_matrix_inputs()
        self.draw_graph()
        self.log(f"Hazır Senaryo Yüklendi: {preset_name}")

    def apply_dimensions(self):
        try:
            new_p = int(self.p_spin.get())
            new_r = int(self.r_spin.get())
            self.engine.set_dimensions(new_p, new_r)
            self.create_matrix_inputs()
            self.draw_graph()
            self.log(f"Sistem boyutu {new_p} Süreç x {new_r} Kaynak olarak güncellendi.")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli tamsayılar girin!")

    def update_values_from_ui(self):
        try:
            for i in range(self.engine.num_processes):
                for j in range(self.engine.num_resources):
                    self.engine.allocation[i][j] = int(self.alloc_entries[i][j].get())
                    self.engine.max_need[i][j] = int(self.max_entries[i][j].get())
                self.engine.priorities[i] = int(self.prio_entries[i].get())
                self.engine.costs[i] = int(self.cost_entries[i].get())
            self.log("Matris, Öncelik ve Maliyet değerleri güncellendi.")
            self.draw_graph()
            messagebox.showinfo("Başarılı", "Tüm değerler başarıyla güncellendi!")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen kutulara geçerli tamsayılar girin!")

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def draw_graph(self, highlight_process=None, status=None):
        self.ax.clear()
        
        bg_color = '#1e1e1e' if self.is_dark_mode else 'white'
        text_color = 'white' if self.is_dark_mode else 'black'
        self.fig.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(bg_color)

        G = nx.DiGraph()
        processes = [f"P{i}" for i in range(self.engine.num_processes)]
        resources = [f"R{i}" for i in range(self.engine.num_resources)]

        G.add_nodes_from(processes)
        G.add_nodes_from(resources)

        edges = []
        edge_colors = []

        for i in range(self.engine.num_processes):
            for j in range(self.engine.num_resources):
                if self.engine.allocation[i][j] > 0:
                    edges.append((f"R{j}", f"P{i}"))
                    edge_colors.append("#3498db")

        for i in range(self.engine.num_processes):
            for j in range(self.engine.num_resources):
                need = self.engine.max_need[i][j] - self.engine.allocation[i][j]
                if need > 0 and self.engine.available[j] < need:
                    edges.append((f"P{i}", f"R{j}"))
                    edge_colors.append("#e67e22")

        G.add_edges_from(edges)

        pos = {}
        for i, p in enumerate(processes):
            pos[p] = (i, 1)
        for j, r in enumerate(resources):
            pos[r] = (j * (max(len(processes)-1, 1) / max(len(resources)-1, 1)), 0)

        # Düğüm Renkleri (Step Animation için)
        node_colors = []
        for p in processes:
            if highlight_process and p == highlight_process:
                if status == "CHECKING":
                    node_colors.append("#f1c40f")  # Sarı
                elif status == "SUCCESS":
                    node_colors.append("#2ecc71")  # Yeşil
                elif status == "FAILED":
                    node_colors.append("#e74c3c")  # Kırmızı
                else:
                    node_colors.append("#8e44ad")
            else:
                node_colors.append("#a0c4ff")

        nx.draw_networkx_nodes(G, pos, nodelist=processes, node_color=node_colors, node_size=1100, ax=self.ax)
        nx.draw_networkx_nodes(G, pos, nodelist=resources, node_color='#b9fbc0', node_shape='s', node_size=1100, ax=self.ax)
        nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold", font_color='black', ax=self.ax)
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edge_colors, arrows=True, arrowsize=16, ax=self.ax)

        self.ax.set_title("Resource Allocation Graph (RAG)", fontsize=12, color=text_color)
        self.ax.axis('off')
        self.canvas.draw()

    def start_step_execution(self):
        self.execution_steps = self.engine.get_step_by_step_execution()
        self.current_step_idx = 0
        self.log("--- Adım Adım Simülasyon Başlatıldı ---")
        self.next_step_execution()

    def next_step_execution(self):
        if not self.execution_steps or self.current_step_idx >= len(self.execution_steps):
            self.log("Simülasyon adımları tamamlandı!")
            messagebox.showinfo("Bitti", "Adım adım simülasyon tamamlandı.")
            return

        step = self.execution_steps[self.current_step_idx]
        self.log(step["msg"])
        self.draw_graph(highlight_process=step["checking_process"], status=step["status"])
        self.current_step_idx += 1

    def resolve_deadlock(self):
        selected_strategy = self.strategy_cb.get()
        result_msg, victim_idx = self.engine.resolve_deadlock_strategy(selected_strategy)
        self.create_matrix_inputs()
        self.log(f"ÇÖZÜM UYGULANDI ({selected_strategy}):")
        self.log(f"> {result_msg}")
        self.draw_graph()
        messagebox.showinfo("Kilitlenme Çözüldü", f"{result_msg}\nKilitlenme açıldı!")

    def export_report(self):
        is_safe, safe_seq = self.engine.run_bankers()
        report_text = self.engine.generate_report(is_safe, safe_seq)
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Deadlock Sistem Raporunu Kaydet"
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(report_text)
            self.log(f"Rapor kaydedildi: {file_path}")
            messagebox.showinfo("Başarılı", "Rapor metin dosyası olarak kaydedildi!")
