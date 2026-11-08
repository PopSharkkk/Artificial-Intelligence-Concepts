import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def style_table(table, col_widths, headers, data):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Header Row
    hdr_row = table.rows[0]
    for i, title in enumerate(headers):
        cell = hdr_row.cells[i]
        cell.text = title
        set_cell_background(cell, "1F497D")  # Dark Blue
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.name = "Calibri"
            run.font.size = Pt(10)
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)

    # Data Rows
    for r_idx, row_data in enumerate(data):
        row = table.rows[r_idx + 1]
        bg = "F2F5F9" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.text = str(val)
            set_cell_background(cell, bg)
            p = cell.paragraphs[0]
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(9.5)
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)

    # Set Column Widths
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

def generate_report():
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Set Normal Font
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Calibri'
    font_normal.size = Pt(11)
    font_normal.color.rgb = RGBColor(51, 51, 51)

    # Document Header / Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = title_p.add_run("LAPORAN PENYELESAIAN TUGAS CSP (CONSTRAINT SATISFACTION PROBLEM)")
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(31, 73, 125)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(16)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = sub_p.add_run("Mata Kuliah: Konsep Kecerdasan Artifisial (KKA) - Teknik Informatika ITS")
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(89, 89, 89)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # BAGIAN 1: TUGAS NO. 1
    # =========================================================================
    h1 = doc.add_heading(level=1)
    r1 = h1.add_run("1. TUGAS NO. 1: PERANCANGAN MENU MAKANAN (FOOD MENU CSP)")
    r1.font.color.rgb = RGBColor(31, 73, 125)
    r1.font.bold = True

    p_intro1 = doc.add_paragraph()
    p_intro1.paragraph_format.space_after = Pt(6)
    p_intro1.add_run("Anda diminta merancang menu makanan di suatu event yang terdiri dari 4 variabel: ")
    p_intro1.add_run("Appetizer, Beverage, Main_Course, ").bold = True
    p_intro1.add_run("dan ")
    p_intro1.add_run("Dessert").bold = True
    p_intro1.add_run(". Semua tamu mendapatkan menu yang sama dan harus mematuhi ketiga batasan diet berikut:")

    bullets_t1 = [
        ("Variabel & Domain:", "Appetizer ∈ {veggies, escargot}, Beverage ∈ {water, soda, milk}, Main_Course ∈ {fish, beef, pasta}, Dessert ∈ {apple pie, ice cream, cheese}."),
        ("Batasan (i) - Vegetarian:", "Appetizer harus sayuran (veggies) ATAU Main_Course harus pasta atau fish."),
        ("Batasan (ii) - Total Biaya:", "Jika memilih escargot, maka pilihan untuk beverage HANYA water. (escargot ⇒ water)."),
        ("Batasan (iii) - Kalsium:", "Harus memilih setidaknya satu di antara milk (Beverage), ice cream (Dessert), atau cheese (Dessert).")
    ]
    for b_title, b_desc in bullets_t1:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        bp.add_run(b_title + " ").bold = True
        bp.add_run(b_desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Sub a
    h2_a = doc.add_heading(level=2)
    r2_a = h2_a.add_run("(a) Constraint Graph dari Permasalahan Menu")
    r2_a.font.color.rgb = RGBColor(38, 38, 38)
    
    p_ga = doc.add_paragraph()
    p_ga.paragraph_format.space_after = Pt(6)
    p_ga.add_run("Constraint graph merupakan graf di mana node merepresentasikan variabel dan edge tak-berarah (undirected edge) merepresentasikan constraint biner (relasi batasan antara dua variabel):")
    
    edges_desc = [
        ("Edge (Appetizer - Main_Course):", "Mewakili Batasan (i) Vegetarian."),
        ("Edge (Appetizer - Beverage):", "Mewakili Batasan (ii) Biaya Total (escargot ⇒ water)."),
        ("Edge (Beverage - Dessert):", "Mewakili Batasan (iii) Kebutuhan Kalsium.")
    ]
    for et, ed in edges_desc:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(2)
        bp.add_run(et + " ").bold = True
        bp.add_run(ed)

    # Insert Image 1
    img1_path = r"C:\Users\Rinaltra\.gemini\antigravity\scratch\csp-kka-assignment\images\tugas1_constraint_graph.png"
    if os.path.exists(img1_path):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img1.paragraph_format.space_before = Pt(8)
        p_img1.paragraph_format.space_after = Pt(4)
        run_img1 = p_img1.add_run()
        run_img1.add_picture(img1_path, width=Inches(4.8))
        cap1 = doc.add_paragraph()
        cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap1.paragraph_format.space_after = Pt(12)
        r_cap1 = cap1.add_run("Gambar 1: Constraint Graph Permasalahan Menu Makanan")
        r_cap1.font.size = Pt(9.5)
        r_cap1.font.italic = True
        r_cap1.font.color.rgb = RGBColor(89, 89, 89)

    # Sub b
    h2_b = doc.add_heading(level=2)
    r2_b = h2_b.add_run("(b) Forward Checking saat Appetizer = escargot")
    r2_b.font.color.rgb = RGBColor(38, 38, 38)

    p_fc = doc.add_paragraph()
    p_fc.paragraph_format.space_after = Pt(6)
    p_fc.add_run("Forward checking (FC) mengecek constraint biner antara variabel yang baru saja di-assign (")
    p_fc.add_run("Appetizer = escargot").bold = True
    p_fc.add_run(") terhadap setiap variabel tetangganya yang belum di-assign (unassigned neighbors), lalu mengeliminasi nilai-nilai di domain variabel yang inkonsisten:")

    fc_steps = [
        ("Variabel Beverage (Tetangga Appetizer):", "Batasan (ii) menyatakan jika Appetizer = escargot, maka Beverage HANYA water. Nilai {soda, milk} langsung DIELIMINASI. Sisa domain: {water}."),
        ("Variabel Main_Course (Tetangga Appetizer):", "Batasan (i) menyatakan Appetizer harus sayuran (veggies) ATAU Main_Course harus pasta/fish. Karena Appetizer = escargot (bukan veggies), maka Main_Course WAJIB pasta atau fish. Nilai {beef} DIELIMINASI. Sisa domain: {fish, pasta}."),
        ("Variabel Dessert (Bukan Tetangga Langsung Appetizer):", "Appetizer tidak memiliki edge langsung ke Dessert. Forward Checking standar hanya menyaring unassigned variables yang terhubung langsung dengan variabel yang baru di-assign. Oleh karena itu, pada tahap ini tidak ada nilai yang dieliminasi pada Dessert. Sisa domain: {apple pie, ice cream, cheese}.")
    ]
    for f_var, f_desc in fc_steps:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        bp.add_run(f_var + " ").bold = True
        bp.add_run(f_desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    
    # Tabel Ringkasan FC
    table_fc = doc.add_table(rows=4, cols=4)
    headers_fc = ["Variabel", "Domain Awal", "Nilai yang Dieliminasi", "Sisa Domain"]
    data_fc = [
        ["Beverage", "{water, soda, milk}", "{soda, milk}", "{water}"],
        ["Main_Course", "{fish, beef, pasta}", "{beef}", "{fish, pasta}"],
        ["Dessert", "{apple pie, ice cream, cheese}", "Tidak ada (Ø)", "{apple pie, ice cream, cheese}"]
    ]
    style_table(table_fc, [Inches(1.3), Inches(1.8), Inches(1.8), Inches(1.8)], headers_fc, data_fc)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Sub c
    h2_c = doc.add_heading(level=2)
    r2_c = h2_c.add_run("(c) 3 Contoh Solusi Lengkap yang Memenuhi Semua Batasan")
    r2_c.font.color.rgb = RGBColor(38, 38, 38)

    p_sol_desc = doc.add_paragraph()
    p_sol_desc.paragraph_format.space_after = Pt(6)
    p_sol_desc.add_run("Dari total 2 x 3 x 3 x 3 = 54 kemungkinan kombinasi, algoritma CSP menemukan ")
    p_sol_desc.add_run("25 solusi valid").bold = True
    p_sol_desc.add_run(". Berikut adalah 3 contoh penugasan solusi lengkap:")

    table_sol = doc.add_table(rows=4, cols=5)
    headers_sol = ["Solusi Ke-", "Appetizer", "Beverage", "Main_Course", "Dessert"]
    data_sol = [
        ["Solusi 1", "veggies", "water", "fish", "ice cream"],
        ["Solusi 2", "escargot", "water", "pasta", "cheese"],
        ["Solusi 3", "veggies", "milk", "beef", "apple pie"]
    ]
    style_table(table_sol, [Inches(1.0), Inches(1.3), Inches(1.3), Inches(1.3), Inches(1.5)], headers_sol, data_sol)

    # Penjelasan singkat verifikasi 3 solusi
    p_verif = doc.add_paragraph()
    p_verif.paragraph_format.space_before = Pt(6)
    p_verif.paragraph_format.space_after = Pt(14)
    p_verif.add_run("Verifikasi Kepatuhan Batasan:\n").bold = True
    p_verif.add_run("• Solusi 1: Appetizer veggies (memenuhi Batasan i), Appetizer bukan escargot (Batasan ii terpenuhi otomatis), Dessert ice cream berkalsium (memenuhi Batasan iii).\n")
    p_verif.add_run("• Solusi 2: Appetizer escargot dipasangkan Beverage water (memenuhi Batasan ii), Main_Course pasta (memenuhi Batasan i), Dessert cheese berkalsium (memenuhi Batasan iii).\n")
    p_verif.add_run("• Solusi 3: Appetizer veggies (memenuhi Batasan i), Main_Course beef diperbolehkan karena Appetizer sudah veggies, Beverage milk berkalsium (memenuhi Batasan iii).")

    # =========================================================================
    # BAGIAN 2: TUGAS NO. 2
    # =========================================================================
    h1_2 = doc.add_heading(level=1)
    r1_2 = h1_2.add_run("2. TUGAS NO. 2: PENJADWALAN KELAS KULIAH (CLASS SCHEDULING CSP)")
    r1_2.font.color.rgb = RGBColor(31, 73, 125)
    r1_2.font.bold = True

    p_intro2 = doc.add_paragraph()
    p_intro2.paragraph_format.space_after = Pt(6)
    p_intro2.add_run("Diberikan penjadwalan 5 kelas pada hari Senin, Rabu, dan Jumat yang diampu oleh 3 profesor (A, B, C). ")
    p_intro2.add_run("Batasan utama: Setiap profesor hanya dapat mengajar satu kelas pada waktu yang sama (no overlapping classes for the same professor).").bold = True

    # Daftar Kelas & Profesor
    table_kls = doc.add_table(rows=6, cols=3)
    headers_kls = ["Kelas", "Nama Mata Kuliah", "Waktu Pelaksanaan"]
    data_kls = [
        ["Class 1", "Intro to Programming", "08:00 - 09:00 AM"],
        ["Class 2", "Intro to Artificial Intelligence", "08:30 - 09:30 AM"],
        ["Class 3", "Natural Language Processing", "09:00 - 10:00 AM"],
        ["Class 4", "Computer Vision", "09:00 - 10:00 AM"],
        ["Class 5", "Machine Learning", "09:30 - 10:30 AM"]
    ]
    style_table(table_kls, [Inches(1.2), Inches(3.0), Inches(2.2)], headers_kls, data_kls)

    p_prof = doc.add_paragraph()
    p_prof.paragraph_format.space_before = Pt(6)
    p_prof.paragraph_format.space_after = Pt(6)
    p_prof.add_run("Ketersediaan Pengampu (Availability):\n").bold = True
    p_prof.add_run("• Profesor A bersedia mengajar: Class 3, Class 4\n")
    p_prof.add_run("• Profesor B bersedia mengajar: Class 2, Class 3, Class 4, Class 5\n")
    p_prof.add_run("• Profesor C bersedia mengajar: Class 1, Class 2, Class 3, Class 4, Class 5")

    # Sub a
    h2_2a = doc.add_heading(level=2)
    r2_2a = h2_2a.add_run("a. Formulasi Masalah sebagai CSP (Variables, Domains, Constraints)")
    r2_2a.font.color.rgb = RGBColor(38, 38, 38)

    form_pts = [
        ("1. Variabel (Variables):", "X = {C1, C2, C3, C4, C5}, di mana setiap variabel merepresentasikan kelas yang harus dijadwalkan pengampunya."),
        ("2. Domain (Domains):", "Himpunan profesor yang bersedia mengajar masing-masing kelas:\n"
         "  • D(C1) = {C}\n"
         "  • D(C2) = {B, C}\n"
         "  • D(C3) = {A, B, C}\n"
         "  • D(C4) = {A, B, C}\n"
         "  • D(C5) = {B, C}"),
        ("3. Batasan Waktu Tumpang Tindih (Time Overlap Conflicts):", "Dua kelas yang memiliki irisan waktu tidak boleh memiliki pengampu yang sama (jika overlap(Ci, Cj), maka Ci ≠ Cj):\n"
         "  • Overlap C1 (08:00-09:00) & C2 (08:30-09:30) pada 08:30-09:00 ⇒ C1 ≠ C2\n"
         "  • Overlap C2 (08:30-09:30) & C3 (09:00-10:00) pada 09:00-09:30 ⇒ C2 ≠ C3\n"
         "  • Overlap C2 (08:30-09:30) & C4 (09:00-10:00) pada 09:00-09:30 ⇒ C2 ≠ C4\n"
         "  • Overlap C3 (09:00-10:00) & C4 (09:00-10:00) pada 09:00-10:00 ⇒ C3 ≠ C4\n"
         "  • Overlap C3 (09:00-10:00) & C5 (09:30-10:30) pada 09:30-10:00 ⇒ C3 ≠ C5\n"
         "  • Overlap C4 (09:00-10:00) & C5 (09:30-10:30) pada 09:30-10:00 ⇒ C4 ≠ C5")
    ]
    for ft, fd in form_pts:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        bp.add_run(ft + " ").bold = True
        bp.add_run(fd)

    # Insert Image 2
    img2_path = r"C:\Users\Rinaltra\.gemini\antigravity\scratch\csp-kka-assignment\images\tugas2_constraint_graph.png"
    if os.path.exists(img2_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_before = Pt(8)
        p_img2.paragraph_format.space_after = Pt(4)
        run_img2 = p_img2.add_run()
        run_img2.add_picture(img2_path, width=Inches(4.8))
        cap2 = doc.add_paragraph()
        cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap2.paragraph_format.space_after = Pt(12)
        r_cap2 = cap2.add_run("Gambar 2: Constraint Graph Penjadwalan Kelas (Konflik Waktu)")
        r_cap2.font.size = Pt(9.5)
        r_cap2.font.italic = True
        r_cap2.font.color.rgb = RGBColor(89, 89, 89)

    # Sub b
    h2_2b = doc.add_heading(level=2)
    r2_2b = h2_2b.add_run("b. Penyelesaian Masalah Menggunakan CSP (Step-by-Step Backtracking + FC/Inference)")
    r2_2b.font.color.rgb = RGBColor(38, 38, 38)

    p_solve_steps = doc.add_paragraph()
    p_solve_steps.paragraph_format.space_after = Pt(6)
    p_solve_steps.add_run("Langkah-langkah pencarian solusi CSP menggunakan heuristik MRV (Minimum Remaining Values) dan Forward Checking:\n\n")
    p_solve_steps.add_run("Langkah 1: Penugasan C1 (Variabel paling terikat, |D(C1)| = 1)\n").bold = True
    p_solve_steps.add_run("  • D(C1) hanya memiliki 1 nilai, yaitu C. Maka tetapkan C1 = C.\n")
    p_solve_steps.add_run("  • Forward Checking ke tetangganya C2 (C1 ≠ C2): eliminasi nilai 'C' dari D(C2).\n")
    p_solve_steps.add_run("  • Hasil pangkas domain: D(C2) tersisa {B}.\n\n")

    p_solve_steps.add_run("Langkah 2: Penugasan C2 (Sisa domain terkecil, |D(C2)| = 1)\n").bold = True
    p_solve_steps.add_run("  • Karena D(C2) = {B}, maka tetapkan C2 = B.\n")
    p_solve_steps.add_run("  • Forward Checking ke tetangganya (C3 dan C4, di mana C2 ≠ C3 dan C2 ≠ C4):\n")
    p_solve_steps.add_run("    - Eliminasi 'B' dari D(C3) ⇒ D(C3) tersisa {A, C}.\n")
    p_solve_steps.add_run("    - Eliminasi 'B' dari D(C4) ⇒ D(C4) tersisa {A, C}.\n\n")

    p_solve_steps.add_run("Langkah 3: Penugasan C5 dan Analisis Relasi Tiga Serangkai (C3, C4, C5)\n").bold = True
    p_solve_steps.add_run("  • Perhatikan batasan antara C3, C4, dan C5: ketiganya saling bertetangga membentuk graf klik segitiga K3 (semuanya overlap satu sama lain pada 09:30-10:00):\n")
    p_solve_steps.add_run("    C3 ≠ C4, C3 ≠ C5, dan C4 ≠ C5 (ketiganya harus memiliki profesor berbeda!).\n")
    p_solve_steps.add_run("  • Himpunan domain saat ini:\n")
    p_solve_steps.add_run("    D(C3) = {A, C}, D(C4) = {A, C}, dan D(C5) = {B, C}.\n")
    p_solve_steps.add_run("  • Karena {C3, C4} hanya bisa diisi oleh subset {A, C}, maka salah satu dari {C3, C4} PASTI bernilai 'C' dan satunya lagi PASTI bernilai 'A'.\n")
    p_solve_steps.add_run("  • Akibatnya, nilai 'C' SUDAH TERPAKAI oleh salah satu antara C3 atau C4. Karena C5 bertetangga dengan C3 dan C4, maka C5 TIDAK BOLEH bernilai 'C'.\n")
    p_solve_steps.add_run("  • Nilai tersisa untuk C5 HANYA: C5 = B. (C5 dan C2 sama-sama diajar Prof B, dan ini VALID karena waktu C2 08:30-09:30 tidak bertabrakan dengan C5 09:30-10:30).\n\n")

    p_solve_steps.add_run("Langkah 4: Percabangan Pasangan (C3, C4)\n").bold = True
    p_solve_steps.add_run("  Karena C3 ≠ C4 dan domainnya {A, C}, terdapat tepat 2 cabang solusi:\n")
    p_solve_steps.add_run("  • Cabang 1: C3 = A, sehingga C4 = C.\n")
    p_solve_steps.add_run("  • Cabang 2: C3 = C, sehingga C4 = A.\n")

    # Tabel Solusi Tugas 2
    table_sol2 = doc.add_table(rows=3, cols=6)
    headers_sol2 = ["Solusi", "Class 1", "Class 2", "Class 3", "Class 4", "Class 5"]
    data_sol2 = [
        ["Solusi 1", "Professor C", "Professor B", "Professor A", "Professor C", "Professor B"],
        ["Solusi 2", "Professor C", "Professor B", "Professor C", "Professor A", "Professor B"]
    ]
    style_table(table_sol2, [Inches(1.0), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1)], headers_sol2, data_sol2)

    p_summary = doc.add_paragraph()
    p_summary.paragraph_format.space_before = Pt(8)
    p_summary.paragraph_format.space_after = Pt(8)
    p_summary.add_run("Kesimpulan Tugas 2: ").bold = True
    p_summary.add_run("Terdapat tepat 2 solusi optimal yang valid dan konsisten secara global untuk permasalahan penjadwalan kelas ini.")

    # Save document
    downloads_path = r"C:\Users\Rinaltra\Downloads\Laporan_Solusi_CSP_Tugas_1_dan_2.docx"
    doc.save(downloads_path)
    print(f"Laporan Word berhasil disimpan di: {downloads_path}")

    # Simpan juga di folder project
    proj_docx_path = r"C:\Users\Rinaltra\.gemini\antigravity\scratch\csp-kka-assignment\Laporan_Solusi_CSP_Tugas_1_dan_2.docx"
    doc.save(proj_docx_path)
    print(f"Laporan Word berhasil disalin ke: {proj_docx_path}")

if __name__ == "__main__":
    generate_report()
