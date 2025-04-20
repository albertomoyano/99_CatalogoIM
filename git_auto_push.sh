#!/bin/bash

# Configuración de colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Función para verificar cambios
verificar_cambios() {
    git status --porcelain
}

main() {
    echo -e "\n${YELLOW}=== GitHub Push Automático ===${NC}"
    
    # Configurar estrategia de pull
    git config pull.rebase false || {
        echo -e "${RED}✗ Error al configurar pull.rebase${NC}"
        exit 1
    }

    # Eliminar docs/ del seguimiento
    echo -e "\n${GREEN}» Limpiando carpeta docs/ local...${NC}"
    git rm -r --cached docs/ 2>/dev/null || echo -e "${YELLOW}ℹ No hay docs/ en el índice${NC}"

    # Verificar cambios
    cambios=$(verificar_cambios)
    if [ -z "$cambios" ]; then
        echo -e "\n${YELLOW}No hay cambios pendientes.${NC}"
        exit 0
    fi

    # Mostrar cambios
    echo -e "\n${GREEN}» Cambios detectados:${NC}"
    echo "$cambios"
    echo -e "\n----------------------------------------"
    
    # Solicitar mensaje de commit
    mensaje_predeterminado="Actualización automática de PDFs"
    read -p $"Mensaje de commit [$mensaje_predeterminado]: " mensaje
    mensaje=${mensaje:-$mensaje_predeterminado}

    # Confirmación
    echo -e "\n${YELLOW}» Resumen:${NC}"
    echo -e "Commit: ${mensaje}"
    echo -e "Cambios:"
    echo "$cambios"
    
    read -p $"\n¿Continuar? (s/n): " confirmacion
    [[ "$confirmacion" =~ ^[sS]$ ]] || {
        echo -e "\n${YELLOW}Operación cancelada.${NC}"
        exit 0
    }

    # Ejecutar Git commands
    echo -e "\n${GREEN}» Añadiendo cambios...${NC}"
    git add . || {
        echo -e "${RED}✗ Error en git add${NC}"
        exit 1
    }

    echo -e "\n${GREEN}» Creando commit...${NC}"
    git commit -m "$mensaje" || {
        echo -e "${RED}✗ Error en git commit${NC}"
        exit 1
    }

    # Sincronizar con remoto
    echo -e "\n${GREEN}» Sincronizando con GitHub...${NC}"
    git pull origin main || {
        echo -e "${RED}✗ Error en git pull${NC}"
        echo -e "${YELLOW}Resuelve conflictos manualmente y vuelve a intentar.${NC}"
        exit 1
    }

    git push origin main && {
        echo -e "\n${GREEN}✓ Push completado!${NC}"
        echo -e "El PDF combinado se generará automáticamente en GitHub."
    } || {
        echo -e "\n${RED}✗ Error en git push${NC}"
        echo -e "Intenta manualmente con: git push origin main"
        exit 1
    }
}

main