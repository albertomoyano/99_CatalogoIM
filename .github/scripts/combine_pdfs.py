import os
import re
import PyPDF2
import glob

# Configuración de directorios
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_dir = os.path.abspath(os.path.join(script_dir, "../.."))
output_file = os.path.join(repo_dir, "catalogo_completo.pdf")  # Cambiado para coincidir con el workflow

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
    if not ".github" in file
    and not file.endswith("catalogo_completo.pdf")  # Evitar recursión
    and os.path.isfile(file)  # Verificar que el archivo existe
]

# Verificar que se encontraron archivos
if not pdf_files:
    print("⚠️ No se encontraron archivos PDF para combinar")
    # Crear un PDF vacío para evitar errores
    with open(output_file, 'wb') as f:
        merger = PyPDF2.PdfMerger()
        merger.write(f)
    print(f"► Se ha creado un PDF vacío en: {output_file}")
    exit(0)

# Ordenar archivos
pdf_files.sort(key=extract_sort_key, reverse=True)

# Mostrar lista de archivos combinados
print("\nArchivos que se van a combinar:")
for f in pdf_files:
    print(f)

# Combinar PDFs
merger = PyPDF2.PdfMerger()
for pdf in pdf_files:
    try:
        merger.append(pdf)
        print(f"✓ Añadido: {os.path.basename(pdf)}")
    except Exception as e:
        print(f"✗ Error en {os.path.basename(pdf)}: {str(e)}")

# Guardar resultado
try:
    merger.write(output_file)
    merger.close()
    print(f"\n► PDF combinado generado en: {output_file}")
    print("Orden de combinación:")
    for i, pdf in enumerate(pdf_files, 1):
        print(f"{i}. {os.path.basename(pdf)}")
except Exception as e:
    print(f"Error al guardar el PDF combinado: {str(e)}")