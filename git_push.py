import subprocess
import sys
import os

def verificar_cambios():
    """Verifica si hay cambios pendientes en el repositorio."""
    resultado = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    return resultado.stdout.strip()

def ejecutar_git(mensaje_commit):
    """Ejecuta los comandos de git para añadir, hacer commit y push."""
    try:
        # Verificar si hay cambios
        cambios = verificar_cambios()
        if not cambios:
            print("No hay cambios para subir.")
            return False
        
        print("Cambios pendientes:")
        print(cambios)
        print("-" * 50)
        
        # Ejecutar git add
        print("Ejecutando git add...")
        add_proceso = subprocess.run(["git", "add", "."], capture_output=True, text=True, check=True)
        if add_proceso.stdout:
            print(add_proceso.stdout)
        
        # Ejecutar git commit
        if not mensaje_commit.strip():
            mensaje_commit = "Actualización automática"
        
        print(f"Ejecutando git commit con mensaje: '{mensaje_commit}'...")
        commit_proceso = subprocess.run(["git", "commit", "-m", mensaje_commit], 
                                        capture_output=True, text=True, check=True)
        print(commit_proceso.stdout)
        
        # Ejecutar git push
        print("Ejecutando git push...")
        push_proceso = subprocess.run(["git", "push", "-u", "origin", "main"], 
                                      capture_output=True, text=True, check=True)
        print(push_proceso.stdout)
        
        print("¡Proceso completado con éxito!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Salida del error: {e.stderr}")
        return False

def main():
    """Función principal que maneja el flujo del programa."""
    print("=== GitHub Push Automático ===")
    
    # Verificar si hay cambios
    cambios = verificar_cambios()
    
    if not cambios:
        print("No hay cambios pendientes para subir a GitHub.")
        return
    
    # Solicitar mensaje de commit
    mensaje_predeterminado = "Actualización de archivos PDF"
    mensaje = input(f"Mensaje de commit [{mensaje_predeterminado}]: ")
    
    if not mensaje.strip():
        mensaje = mensaje_predeterminado
    
    # Confirmar acción
    print("\nEstá a punto de hacer push con los siguientes cambios:")
    print(cambios)
    print(f"Mensaje de commit: '{mensaje}'")
    
    confirmacion = input("\n¿Desea continuar? (s/n): ").lower()
    
    if confirmacion == 's':
        ejecutar_git(mensaje)
    else:
        print("Operación cancelada.")

if __name__ == "__main__":
    main()