import os
import re
import PyPDF2
import glob

# Directorio donde se encuentra el script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Directorio raíz del repositorio
repo_dir = os.path.abspath(os.path.join(script_dir, "../.."))
# Directorio de salida para el PDF combinado
output_dir = os.path.join(repo_dir, "docs")
output_file = os.path.join(output_dir, "catalogo_ediciones_imago_mundi.pdf")

# Asegurar que el directorio de salida existe
os.makedirs(output_dir, exist_ok=True)

# Encontrar todos los archivos PDF en el repositorio
pdf_files = []
for file in glob.glob(os.path.join(repo_dir, "**/*.pdf"), recursive=True):
    # Excluir archivos en la carpeta docs/ y archivos en .github/
    if not file.startswith(output_dir) and not ".github" in file:
        pdf_files.append(file)

# Función para extraer la fecha del nombre del archivo
def extract_date(filename):
    base = os.path.basename(filename)
    match = re.match(r'(\d{4})_', base)
    if match:
        return match.group(1)
    return "0000"  # Default para archivos sin el formato correcto

# Ordenar archivos PDF por fecha de más reciente a más antiguo
pdf_files.sort(key=extract_date, reverse=True)

# Combinar los PDFs
merger = PyPDF2.PdfMerger()
for pdf in pdf_files:
    merger.append(pdf)

# Guardar el PDF combinado
merger.write(output_file)
merger.close()

print(f"Se han combinado {len(pdf_files)} archivos PDF en {output_file}")