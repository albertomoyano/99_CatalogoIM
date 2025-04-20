# Repositorio del Catálogo de Ediciones Imago Mundi

Este repositorio contiene los archivos PDF individuales de cada página que compone el catálogo digital. 

## Funcionamiento Automatizado

El sistema cuenta con un flujo de trabajo automatizado:

1. **Almacenamiento**: Cada página del catálogo se guarda como un PDF individual en este repositorio
2. **Procesamiento**: Mediante GitHub Actions, se genera automáticamente:
   - Ordenación de los PDFs de más reciente a más antiguo
   - Unión de todos los archivos en un solo PDF completo
3. **Publicación**: El archivo consolidado se publica automáticamente en los Releases del proyecto


## Frecuencia de actualización

El proceso de generación se ejecuta cada vez que se añade o modifica un PDF.

