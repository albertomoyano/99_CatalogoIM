import os
import re
import PyPDF2
import glob

# Configuración de directorios
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_dir = os.path.abspath(os.path.join(script_dir, "../.."))
output_dir = os.path.join(repo_dir, "docs")
output_file = os.path.join(output_dir, "catalogo_ediciones_imago_mundi.pdf")

# Crear directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Función para extraer clave de ordenamiento
def extract_sort_key(filename):
    base = os.path.basename(filename)
    match = re.match(r'(\d{4})-(\d{8})', base)
    if match:
        return (int(match.group(1)), int(match.group(2)))
    return (0, 0)

# Buscar y filtrar archivos PDF
pdf_files = [
    file for file in glob.glob(os.path.join(repo_dir, "**/*.pdf"), recursive=True)
    if not file.startswith(output_dir) 
    and not ".github" in file
    and not os.path.dirname(file).endswith("/docs")  # Ignorar /docs local
]

# Ordenar archivos
pdf_files.sort(key=extract_sort_key, reverse=True)

# Combinar PDFs
merger = PyPDF2.PdfMerger()
for pdf in pdf_files:
    try:
        merger.append(pdf)
        print(f"✓ Añadido: {os.path.basename(pdf)}")
    except Exception as e:
        print(f"✗ Error en {os.path.basename(pdf)}: {str(e)}")

# Guardar resultado
merger.write(output_file)
merger.close()

print(f"\n► PDF combinado generado en: {output_file}")
print("Orden de combinación:")
for i, pdf in enumerate(pdf_files, 1):
    print(f"{i}. {os.path.basename(pdf)}")