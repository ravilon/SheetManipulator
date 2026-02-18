import sys
import csv
import math
import os
import zipfile
from pathlib import Path
from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, filedialog, messagebox, Frame, Radiobutton, ttk
from tkinter import font as tkfont
import threading

# Aumenta o limite para campos gigantes (evita o erro de field limit)
csv.field_size_limit(sys.maxsize)

XLSX_MAX_ROWS = 1_048_576

def detect_delimiter(csv_path, encoding="utf-8"):
    """Detecta se o separador é vírgula ou ponto e vírgula."""
    with open(csv_path, "r", encoding=encoding) as f:
        first_line = f.readline()
        if ";" in first_line and "," not in first_line:
            return ";"
        if "," in first_line and ";" not in first_line:
            return ","
        # Se tiver ambos, tenta contar qual aparece mais
        return ";" if first_line.count(";") > first_line.count(",") else ","

def count_data_rows(csv_path, encoding="utf-8", delimiter=","):
    """Conta as linhas de dados."""
    with open(csv_path, "r", encoding=encoding, newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        next(reader, None)  # pula cabeçalho
        return sum(1 for _ in reader)

def split_csv(
    input_csv,
    output_dir,
    output_format="csv",
    num_files=None,
    rows_per_file=None,
    encoding="utf-8",
    base_name=None,
    progress_callback=None,
):
    # 1. Detectar o delimitador correto do arquivo de entrada
    delimiter = detect_delimiter(input_csv, encoding)
    
    if (num_files is None) == (rows_per_file is None):
        raise ValueError("Forneça exatamente num_files ou rows_per_file")

    output_format = output_format.lower().strip()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if base_name is None:
        base_name = Path(input_csv).stem

    if num_files is not None:
        if progress_callback: progress_callback("Contando linhas...")
        total_rows = count_data_rows(input_csv, encoding, delimiter)
        rows_per_file = math.ceil(total_rows / num_files)

    if output_format == "xlsx":
        from openpyxl import Workbook

    part_idx = 1
    row_in_part = 0
    out_writer = None
    out_file_handle = None
    wb = None
    ws = None

    def open_new_part(header_row):
        nonlocal part_idx, row_in_part, out_writer, out_file_handle, wb, ws
        row_in_part = 0
        suffix = f"{part_idx:04d}"

        if output_format == "csv":
            out_path = output_dir / f"{base_name}_part{suffix}.csv"
            # Escrevemos o output CSV com ponto e vírgula para manter o padrão Excel Brasil
            out_file_handle = open(out_path, "w", encoding=encoding, newline="")
            out_writer = csv.writer(out_file_handle, delimiter=";") 
            out_writer.writerow(header_row)
        else:
            out_path = output_dir / f"{base_name}_part{suffix}.xlsx"
            wb = Workbook()
            ws = wb.active
            ws.append(header_row)
        return out_path

    def close_part(last_out_path):
        nonlocal out_file_handle, out_writer, wb, ws, part_idx
        if output_format == "csv":
            if out_file_handle: out_file_handle.close()
        else:
            if wb: wb.save(last_out_path)
        part_idx += 1

    created_files = []

    with open(input_csv, "r", encoding=encoding, newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        header = next(reader, None)
        
        current_out_path = open_new_part(header)
        created_files.append(str(current_out_path))

        for row in reader:
            if row_in_part >= rows_per_file:
                close_part(current_out_path)
                current_out_path = open_new_part(header)
                created_files.append(str(current_out_path))
                if progress_callback: progress_callback(f"Criando arquivo {part_idx}...")

            if output_format == "csv":
                out_writer.writerow(row)
            else:
                ws.append(row)
            row_in_part += 1

        close_part(current_out_path)
    return created_files

class CSVSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SheetManager - Splitter")
        self.root.geometry("600x550")
        
        self.input_file = StringVar()
        self.output_dir = StringVar()
        self.split_mode = IntVar(value=1)
        self.num_files = IntVar(value=10)
        self.rows_per_file = IntVar(value=100000)
        self.output_format = StringVar(value="xlsx") # Padrão agora é XLSX
        
        title_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        label_font = tkfont.Font(family="Segoe UI", size=10)
        
        Label(root, text="📊 SheetManager Splitter", font=title_font, fg="#2c3e50").pack(pady=20)
        
        # Frame Input
        f1 = Frame(root, bg="#ecf0f1", bd=2, relief="groove")
        f1.pack(padx=20, pady=10, fill="x")
        Label(f1, text="Arquivo CSV:", bg="#ecf0f1").grid(row=0, column=0, padx=5)
        Entry(f1, textvariable=self.input_file, width=40).grid(row=0, column=1, padx=5)
        Button(f1, text="Abrir", command=self.browse_input).grid(row=0, column=2, padx=5, pady=10)
        
        # Frame Output
        f2 = Frame(root, bg="#ecf0f1", bd=2, relief="groove")
        f2.pack(padx=20, pady=10, fill="x")
        Label(f2, text="Pasta Destino:", bg="#ecf0f1").grid(row=0, column=0, padx=5)
        Entry(f2, textvariable=self.output_dir, width=40).grid(row=0, column=1, padx=5)
        Button(f2, text="Pasta", command=self.browse_output).grid(row=0, column=2, padx=5, pady=10)
        
        # Opções
        f3 = Frame(root, bg="#ecf0f1", bd=2, relief="groove")
        f3.pack(padx=20, pady=10, fill="x")
        Radiobutton(f3, text="Qtd de Arquivos", variable=self.split_mode, value=1, bg="#ecf0f1").grid(row=0, column=0, sticky="w")
        Entry(f3, textvariable=self.num_files).grid(row=0, column=1)
        
        Radiobutton(f3, text="Linhas por Arquivo", variable=self.split_mode, value=2, bg="#ecf0f1").grid(row=1, column=0, sticky="w")
        Entry(f3, textvariable=self.rows_per_file).grid(row=1, column=1)
        
        Label(f3, text="Formato Saída:", bg="#ecf0f1").grid(row=2, column=0)
        ttk.Combobox(f3, textvariable=self.output_format, values=["csv", "xlsx"]).grid(row=2, column=1, pady=10)

        self.progress_label = Label(root, text="")
        self.progress_label.pack()
        
        self.btn = Button(root, text="PROCESSAR", command=self.start, bg="#27ae60", fg="white", font=("Segoe UI", 12, "bold"), height=2, width=20)
        self.btn.pack(pady=20)

    def browse_input(self):
        f = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if f: self.input_file.set(f)

    def browse_output(self):
        d = filedialog.askdirectory()
        if d: self.output_dir.set(d)

    def start(self):
        if not self.input_file.get() or not self.output_dir.get():
            return messagebox.showerror("Erro", "Selecione arquivo e pasta!")
        self.btn.config(state="disabled")
        threading.Thread(target=self.run).start()

    def run(self):
        try:
            res = split_csv(
                input_csv=self.input_file.get(),
                output_dir=self.output_dir.get(),
                output_format=self.output_format.get(),
                num_files=self.num_files.get() if self.split_mode.get()==1 else None,
                rows_per_file=self.rows_per_file.get() if self.split_mode.get()==2 else None,
                progress_callback=lambda m: self.progress_label.config(text=m)
            )
            
            # Criar ZIP
            zip_path = Path(self.output_dir.get()) / "resultado_split.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for f in res: zipf.write(f, arcname=Path(f).name)
                
            messagebox.showinfo("Sucesso", f"Processado! ZIP criado em:\n{zip_path}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            self.btn.config(state="normal")
            self.progress_label.config(text="")

if __name__ == "__main__":
    root = Tk()
    CSVSplitterApp(root)
    root.mainloop()