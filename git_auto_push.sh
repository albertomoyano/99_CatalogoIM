#!/bin/bash

# Colores para mejor visualización
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar cambios
verificar_cambios() {
    git status --porcelain
}

# Función principal
main() {
    echo -e "\n${YELLOW}=== GitHub Push Automático ===${NC}"
    
    # Verificar cambios
    cambios=$(verificar_cambios)
    if [ -z "$cambios" ]; then
        echo -e "\n${YELLOW}No hay cambios pendientes para subir.${NC}"
        exit 0
    fi

    # Mostrar cambios y pedir mensaje de commit
    echo -e "\n${GREEN}» Cambios pendientes:${NC}"
    echo "$cambios"
    echo -e "\n----------------------------------------"
    
    mensaje_predeterminado="Actualización de archivos PDF"
    read -p $"Mensaje de commit [$mensaje_predeterminado]: " mensaje
    mensaje=${mensaje:-$mensaje_predeterminado}

    # Confirmación
    echo -e "\n${YELLOW}» Resumen de acciones:${NC}"
    echo -e "Mensaje de commit: '${mensaje}'"
    echo -e "Cambios a subir:"
    echo "$cambios"
    
    read -p $"\n¿Continuar? (s/n): " confirmacion
    if [[ "$confirmacion" != "s" && "$confirmacion" != "S" ]]; then
        echo -e "\n${YELLOW}Operación cancelada.${NC}"
        exit 0
    fi

    # Ejecutar comandos Git
    echo -e "\n${GREEN}» Ejecutando git add...${NC}"
    git add . || { echo -e "${RED}✗ Error en git add${NC}"; exit 1; }

    echo -e "\n${GREEN}» Ejecutando git commit...${NC}"
    git commit -m "$mensaje" || { echo -e "${RED}✗ Error en git commit${NC}"; exit 1; }

    echo -e "\n${GREEN}» Ejecutando git push...${NC}"
    if git push origin main; then
        echo -e "\n${GREEN}✓ ¡Push completado con éxito!${NC}"
        echo -e "El catálogo se regenerará automáticamente con GitHub Actions."
    else
        echo -e "\n${RED}✗ Error en git push${NC}"
        echo -e "Intenta manualmente con:"
        echo -e "git push origin main"
        exit 1
    fi
}

# Ejecutar función principal
main