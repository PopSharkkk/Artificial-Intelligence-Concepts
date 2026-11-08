"""
Solusi CSP untuk Tugas No. 1 (Menu Makanan) dan Tugas No. 2 (Penjadwalan Kelas).
Mendukung penyelesaian exact, forward checking, dan pencarian seluruh solusi yang konsisten.
"""

from itertools import product
from typing import Dict, List, Tuple, Any

# ==============================================================================
# TUGAS 1: PERANCANGAN MENU MAKANAN (CSP)
# ==============================================================================

class Tugas1FoodMenuCSP:
    def __init__(self):
        self.variables = ["Appetizer", "Beverage", "Main_Course", "Dessert"]
        self.domains = {
            "Appetizer": ["veggies", "escargot"],
            "Beverage": ["water", "soda", "milk"],
            "Main_Course": ["fish", "beef", "pasta"],
            "Dessert": ["apple pie", "ice cream", "cheese"]
        }

    def satisfies_constraints(self, assignment: Dict[str, str]) -> bool:
        # Constraint (i): Vegetarian constraint
        # Appetizer harus veggies ATAU Main_Course harus pasta atau fish
        if "Appetizer" in assignment and "Main_Course" in assignment:
            app = assignment["Appetizer"]
            mc = assignment["Main_Course"]
            if not (app == "veggies" or mc in ["pasta", "fish"]):
                return False

        # Constraint (ii): Total cost constraint
        # Jika Appetizer == escargot, maka Beverage HANYA water
        if "Appetizer" in assignment and "Beverage" in assignment:
            if assignment["Appetizer"] == "escargot" and assignment["Beverage"] != "water":
                return False

        # Constraint (iii): Calcium constraint
        # Setidaknya salah satu di antara milk (Beverage), ice cream (Dessert), atau cheese (Dessert)
        if "Beverage" in assignment and "Dessert" in assignment:
            bev = assignment["Beverage"]
            des = assignment["Dessert"]
            has_calcium = (bev == "milk") or (des in ["ice cream", "cheese"])
            if not has_calcium:
                return False

        return True

    def forward_checking_appetizer_escargot(self) -> Dict[str, List[str]]:
        """
        Simulasi Forward Checking jika Appetizer = 'escargot'.
        Variabel yang belum di-assign: Beverage, Main_Course, Dessert.
        """
        initial_domains = {var: list(self.domains[var]) for var in self.variables}
        # Step 1: Assign Appetizer = escargot
        initial_domains["Appetizer"] = ["escargot"]
        assigned = {"Appetizer": "escargot"}

        # Domain penyaringan
        pruned_domains = {}
        for var in ["Beverage", "Main_Course", "Dessert"]:
            valid_vals = []
            for val in initial_domains[var]:
                # Cek constraint biner antara Appetizer dan var ini
                trial = dict(assigned)
                trial[var] = val
                if self.satisfies_constraints(trial):
                    valid_vals.append(val)
            pruned_domains[var] = valid_vals

        return pruned_domains

    def find_all_solutions(self) -> List[Dict[str, str]]:
        solutions = []
        for app in self.domains["Appetizer"]:
            for bev in self.domains["Beverage"]:
                for mc in self.domains["Main_Course"]:
                    for des in self.domains["Dessert"]:
                        assignment = {
                            "Appetizer": app,
                            "Beverage": bev,
                            "Main_Course": mc,
                            "Dessert": des
                        }
                        if self.satisfies_constraints(assignment):
                            solutions.append(assignment)
        return solutions


# ==============================================================================
# TUGAS 2: PENJADWALAN KELAS KULIAH (CSP)
# ==============================================================================

class Tugas2ClassSchedulingCSP:
    def __init__(self):
        # 5 Variabel: C1, C2, C3, C4, C5
        self.variables = ["C1", "C2", "C3", "C4", "C5"]
        
        # Domain tiap kelas berdasarkan ketersediaan profesor:
        # Prof A: {C3, C4} -> C3 dan C4 bisa A
        # Prof B: {C2, C3, C4, C5} -> C2, C3, C4, C5 bisa B
        # Prof C: {C1, C2, C3, C4, C5} -> semua bisa C
        self.domains = {
            "C1": ["C"],
            "C2": ["B", "C"],
            "C3": ["A", "B", "C"],
            "C4": ["A", "B", "C"],
            "C5": ["B", "C"]
        }

        # Overlapping pairs (tidak boleh diajar profesor yang sama)
        # C1 (8:00-9:00) vs C2 (8:30-9:30): Overlap 8:30-9:00
        # C2 (8:30-9:30) vs C3 (9:00-10:00): Overlap 9:00-9:30
        # C2 (8:30-9:30) vs C4 (9:00-10:00): Overlap 9:00-9:30
        # C3 (9:00-10:00) vs C4 (9:00-10:00): Overlap 9:00-10:00
        # C3 (9:00-10:00) vs C5 (9:30-10:30): Overlap 9:30-10:00
        # C4 (9:00-10:00) vs C5 (9:30-10:30): Overlap 9:30-10:00
        self.conflicts = [
            ("C1", "C2"),
            ("C2", "C3"),
            ("C2", "C4"),
            ("C3", "C4"),
            ("C3", "C5"),
            ("C4", "C5")
        ]

    def is_valid(self, assignment: Dict[str, str]) -> bool:
        for u, v in self.conflicts:
            if u in assignment and v in assignment:
                if assignment[u] == assignment[v]:
                    return False
        return True

    def solve_backtracking(self) -> List[Dict[str, str]]:
        solutions = []

        def backtrack(curr_assignment: Dict[str, str], var_index: int):
            if var_index == len(self.variables):
                solutions.append(dict(curr_assignment))
                return

            var = self.variables[var_index]
            for val in self.domains[var]:
                curr_assignment[var] = val
                if self.is_valid(curr_assignment):
                    backtrack(curr_assignment, var_index + 1)
                del curr_assignment[var]

        backtrack({}, 0)
        return solutions


# ==============================================================================
# MAIN DEMONSTRASI & PENGUJIAN
# ==============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DEMO PENYELESAIAN TUGAS 1 (MENU MAKANAN)")
    print("=" * 60)
    t1 = Tugas1FoodMenuCSP()
    
    print("\n[b] Simulasi Forward Checking (Appetizer = 'escargot'):")
    pruned = t1.forward_checking_appetizer_escargot()
    for var, dom in pruned.items():
        print(f"  - Sisa Domain {var}: {dom}")

    all_sol_1 = t1.find_all_solutions()
    print(f"\n[c] Total Solusi Valid Ditemukan: {len(all_sol_1)}")
    print("Contoh 3 Solusi:")
    for i, sol in enumerate(all_sol_1[:3], 1):
        print(f"  Solusi {i}: {sol}")

    print("\n" + "=" * 60)
    print("DEMO PENYELESAIAN TUGAS 2 (PENJADWALAN KELAS KULIAH)")
    print("=" * 60)
    t2 = Tugas2ClassSchedulingCSP()
    all_sol_2 = t2.solve_backtracking()
    print(f"\nTotal Solusi Valid Ditemukan: {len(all_sol_2)}")
    for i, sol in enumerate(all_sol_2, 1):
        print(f"  Solusi {i}: {sol}")
