import datetime


class DeadlockEngine:
    def __init__(self, num_processes=3, num_resources=2):
        self.num_processes = num_processes
        self.num_resources = num_resources

        # Varsayılan Matrisler
        self.allocation = [[1, 0], [0, 1], [1, 1]]
        self.max_need = [[2, 1], [1, 2], [1, 1]]
        self.available = [0, 0]

        # Süreç Öncelikleri ve Maliyetleri (Priority: 1 en yüksek, Cost: Sonlandırma maliyeti)
        self.priorities = [1, 2, 3]  # P0, P1, P2
        self.costs = [10, 20, 5]  # P0, P1, P2

    def reset_to_default(self):
        self.num_processes = 3
        self.num_resources = 2
        self.allocation = [[1, 0], [0, 1], [1, 1]]
        self.max_need = [[2, 1], [1, 2], [1, 1]]
        self.available = [0, 0]
        self.priorities = [1, 2, 3]
        self.costs = [10, 20, 5]

    def load_preset(self, preset_name):
        """Hazır Senaryo Kütüphanesi"""
        if preset_name == "Deadlock (Kilitlenme Senaryosu)":
            self.set_dimensions(3, 2)
            self.allocation = [[1, 0], [0, 1], [1, 1]]
            self.max_need = [[2, 1], [1, 2], [1, 1]]
            self.available = [0, 0]
            self.priorities = [1, 2, 3]
            self.costs = [10, 20, 5]
        elif preset_name == "Safe State (Güvenli Senaryo)":
            self.set_dimensions(3, 2)
            self.allocation = [[1, 0], [0, 1], [1, 0]]
            self.max_need = [[2, 1], [1, 1], [1, 1]]
            self.available = [1, 1]
            self.priorities = [1, 2, 3]
            self.costs = [10, 15, 20]
        elif preset_name == "High Starvation (Kaynak Açlığı)":
            self.set_dimensions(4, 2)
            self.allocation = [[2, 0], [0, 2], [1, 1], [0, 0]]
            self.max_need = [[3, 1], [1, 3], [2, 2], [4, 4]]
            self.available = [0, 0]
            self.priorities = [1, 4, 2, 3]
            self.costs = [50, 10, 30, 5]

    def set_dimensions(self, new_p, new_r):
        self.num_processes = new_p
        self.num_resources = new_r
        self.allocation = [[0 for _ in range(new_r)] for _ in range(new_p)]
        self.max_need = [[0 for _ in range(new_r)] for _ in range(new_p)]
        self.available = [0 for _ in range(new_r)]
        self.priorities = [i + 1 for i in range(new_p)]
        self.costs = [(i + 1) * 10 for i in range(new_p)]

    def run_bankers(self):
        work = list(self.available)
        finish = [False] * self.num_processes
        safe_sequence = []

        need = [
            [self.max_need[i][j] - self.allocation[i][j] for j in range(self.num_resources)]
            for i in range(self.num_processes)
        ]

        while len(safe_sequence) < self.num_processes:
            found = False
            for i in range(self.num_processes):
                if not finish[i]:
                    if all(need[i][j] <= work[j] for j in range(self.num_resources)):
                        for j in range(self.num_resources):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
                        safe_sequence.append(f"P{i}")
                        found = True
                        break
            if not found:
                break

        is_safe = len(safe_sequence) == self.num_processes
        return is_safe, safe_sequence

    def get_step_by_step_execution(self):
        """Adım Adım Çalıştırma için Durum Üreteci (Generator/List)"""
        steps = []
        work = list(self.available)
        finish = [False] * self.num_processes
        need = [
            [self.max_need[i][j] - self.allocation[i][j] for j in range(self.num_resources)]
            for i in range(self.num_processes)
        ]

        safe_sequence = []

        for step_idx in range(self.num_processes):
            found = False
            for i in range(self.num_processes):
                if not finish[i]:
                    # Adım 1: Kontrol ediliyor
                    steps.append({
                        "checking_process": f"P{i}",
                        "status": "CHECKING",
                        "work": list(work),
                        "finish": list(finish),
                        "safe_sequence": list(safe_sequence),
                        "msg": f"P{i} süreci kontrol ediliyor... İhtiyaç: {need[i]}, Mevcut Kullanılabilir (Work): {work}",
                    })

                    if all(need[i][j] <= work[j] for j in range(self.num_resources)):
                        for j in range(self.num_resources):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
                        safe_sequence.append(f"P{i}")
                        found = True

                        # Adım 2: Başarılı, kaynaklar salındı
                        steps.append({
                            "checking_process": f"P{i}",
                            "status": "SUCCESS",
                            "work": list(work),
                            "finish": list(finish),
                            "safe_sequence": list(safe_sequence),
                            "msg": f"P{i} tamamlandı! Kaynaklar serbest bırakıldı. Yeni Work: {work}",
                        })
                        break
                    else:
                        steps.append({
                            "checking_process": f"P{i}",
                            "status": "FAILED",
                            "work": list(work),
                            "finish": list(finish),
                            "safe_sequence": list(safe_sequence),
                            "msg": f"P{i} kaynak yetersizliğinden atlandı!",
                        })

            if not found:
                steps.append({
                    "checking_process": None,
                    "status": "DEADLOCK_RISK",
                    "work": list(work),
                    "finish": list(finish),
                    "safe_sequence": list(safe_sequence),
                    "msg": "İlerleme sağlanamadı! Sistem Kilitlenme (Deadlock) riskinde.",
                })
                break

        return steps

    def resolve_deadlock_strategy(self, strategy):
        if strategy == "Victim: Max Allocation (En Çok Kaynak Tüketen)":
            total_allocated = [sum(self.allocation[i]) for i in range(self.num_processes)]
            victim_idx = total_allocated.index(max(total_allocated))
        elif strategy == "Lowest Priority (En Düşük Öncelikliyi Öldür)":
            victim_idx = self.priorities.index(max(self.priorities))
        elif strategy == "Lowest Termination Cost (En Az Maliyetliyi Kurban Et)":
            victim_idx = self.costs.index(min(self.costs))
        elif strategy == "Resource Preemption (Kaynak Geri Alma)":
            victim_idx = self.num_processes - 1
        else:
            victim_idx = self.num_processes - 1

        for j in range(self.num_resources):
            self.available[j] += self.allocation[victim_idx][j]
            self.allocation[victim_idx][j] = 0

        return f"P{victim_idx} süreci seçilen strateji ({strategy}) doğrultusunda işlendi.", victim_idx

    def generate_report(self, is_safe, safe_seq):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = "=========================================\n"
        report += " DEADLOCK SIMULATOR - SISTEM DURUM RAPORU\n"
        report += f" Tarih: {now}\n"
        report += "=========================================\n\n"
        report += f"Sistem Boyutu: {self.num_processes} Süreç (P), {self.num_resources} Kaynak (R)\n\n"
        report += "SÜREÇ ÖNCELİKLERİ VE MALİYETLERİ:\n"
        for i in range(self.num_processes):
            report += f"  P{i}: Priority={self.priorities[i]}, Cost={self.costs[i]}\n"
        report += "\nALLOCATION MATRISI:\n"
        for i, row in enumerate(self.allocation):
            report += f"  P{i}: {row}\n"
        report += "\nMAX NEED MATRISI:\n"
        for i, row in enumerate(self.max_need):
            report += f"  P{i}: {row}\n"
        report += f"\nAVAILABLE VECTOR: {self.available}\n"
        report += "-----------------------------------------\n"
        if is_safe:
            report += "GÜVENLİK DURUMU: GÜVENLİ (SAFE)\n"
            report += f"Güvenli Dizi (Safe Sequence): {' -> '.join(safe_seq)}\n"
        else:
            report += "GÜVENLİK DURUMU: GÜVENSİZ / DEADLOCK RISKI!\n"
        report += "=========================================\n"
        return report