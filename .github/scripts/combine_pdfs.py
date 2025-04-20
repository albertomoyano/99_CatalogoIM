import os
import re
import PyPDF2
import glob

# Directorio donde se encuentra el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Directorio raíz del repositorio (sube dos niveles desde script_dir)
repo_dir = os.path.abspath(os.path.join(script_dir, "../.."))

# Directorio de salida para el PDF combinado
output_dir = os.path.join(repo_dir, "docs")
output_file = os.path.join(output_dir, "catalogo_ediciones_imago_mundi.pdf")

# Asegurar que el directorio de salida existe
os.makedirs(output_dir, exist_ok=True)

# Función para extraer prefijo y fecha del nombre del archivo
def extract_sort_key(filename):
    base = os.path.basename(filename)
    match = re.match(r'(\d{4})-(\d{8})', base)  # Formato: 0425-20240921SOLIS.pdf
    if match:
        return (int(match.group(1)), int(match.group(2)))  # Tupla (prefijo, fecha)
    return (0, 0)  # Valor por defecto si no coincide

# Encontrar y ordenar archivos PDF
pdf_files = [
    file for file in glob.glob(os.path.join(repo_dir, "**/*.pdf"), recursive=True)
    if not file.startswith(output_dir) and not ".github" in file
]

# Ordenar por: 1) prefijo (descendente), 2) fecha (descendente)
pdf_files.sort(key=extract_sort_key, reverse=True)

# Combinar los PDFs
merger = PyPDF2.PdfMerger()
for pdf in pdf_files:
    try:
        merger.append(pdf)
        print(f"✅ Añadido: {os.path.basename(pdf)}")
    except Exception as e:
        print(f"❌ Error al añadir {pdf}: {str(e)}")

# Guardar el PDF combinado
merger.write(output_file)
merger.close()

print(f"\n📄 Se combinaron {len(pdf_files)} archivos en: {output_file}")
print("Orden de combinación:")
for i, pdf in enumerate(pdf_files, 1):
    print(f"{i}. {os.path.basename(pdf)}")