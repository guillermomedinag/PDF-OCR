import os
import sys
import subprocess
import platform
import shutil

def find_python_executable():
    """
    Find the appropriate Python executable for creating virtual environment
    """
    # List of potential Python executables for venv creation
    python_executables = [
        'python3',  # Primary check for Unix-like systems
        'python',   # Fallback for Windows and some Unix systems
        sys.executable  # Current Python interpreter
    ]
    
    for executable in python_executables:
        try:
            # Check if the executable can create a virtual environment
            result = subprocess.run(
                [executable, '-m', 'venv', '--help'], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                print(f"✅ Ejecutable de Python encontrado: {executable}")
                return executable
        except Exception:
            continue
    
    print("❌ No se encontró un ejecutable de Python válido para crear entorno virtual")
    print("Asegúrate de tener Python 3.7+ instalado y disponible en tu PATH")
    sys.exit(1)

def run_command(command, error_message=None, shell=False, env=None):
    """
    Run a shell command and handle potential errors
    """
    try:
        # Determine the shell based on the operating system
        if platform.system().lower() == 'windows':
            shell_cmd = ['cmd', '/c']
        else:
            shell_cmd = ['/bin/bash', '-c']

        full_command = shell_cmd + [command] if shell else command
        
        result = subprocess.run(
            full_command, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            env=env
        )
        print(result.stdout)
        return result
    
    except subprocess.CalledProcessError as e:
        print(f"Error: {error_message or 'Command failed'}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Command not found - {command}")
        sys.exit(1)

def detect_os():
    """
    Detect the current operating system
    """
    os_name = platform.system().lower()
    print(f"🖥️ Sistema Operativo Detectado: {os_name}")
    return os_name

def create_virtual_environment(os_name):
    """
    Create Python virtual environment
    """
    print("🐍 Creando entorno virtual de Python...")
    
    try:
        # Find the correct Python executable
        python_exec = find_python_executable()
        
        # Construct the venv creation command
        venv_command = [python_exec, '-m', 'venv', 'pdfvenv']
        
        # Run the venv creation command
        result = subprocess.run(
            venv_command, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            print("❌ Error creando entorno virtual:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            sys.exit(1)
        
        print("✅ Entorno virtual creado exitosamente")
    
    except Exception as e:
        print(f"❌ Error creando entorno virtual: {e}")
        sys.exit(1)

def get_virtual_env_activation_command(os_name):
    """
    Get the virtual environment activation command
    """
    print("🔓 Activando entorno virtual...")
    
    if os_name in ['linux', 'darwin']:
        return ". pdfvenv/bin/activate"
    elif os_name == 'windows':
        return "pdfvenv\\Scripts\\activate"
    else:
        print(f"⚠️ Sistema operativo no soportado: {os_name}")
        sys.exit(1)

def install_python_dependencies(os_name):
    """
    Install Python dependencies in virtual environment
    """
    print("📦 Instalando dependencias de Python...")
    
    try:
        # Get activation command
        activate_cmd = get_virtual_env_activation_command(os_name)
        
        # Prepare the full command to activate venv and install dependencies
        full_command = ""
        if os_name in ['linux', 'darwin']:
            full_command = f"{activate_cmd} && pip install flask flask-cors ocrmypdf"
        elif os_name == 'windows':
            full_command = f"{activate_cmd} && pip install flask flask-cors ocrmypdf"
        
        # Validate full_command before using
        if not full_command:
            print("❌ Error: No se pudo generar el comando de instalación")
            sys.exit(1)
        
        # Run the command
        run_command(
            full_command,
            "No se pudieron instalar las dependencias de Python",
            shell=True
        )
    
    except Exception as e:
        print(f"❌ Error instalando dependencias de Python: {e}")
        sys.exit(1)

def install_node_dependencies():
    """
    Install Node.js dependencies
    """
    print("📦 Instalando dependencias de Node.js...")
    
    try:
        # Install next-themes and other missing dependencies
        run_command(
            ["npm", "install", "next-themes", "sonner"],
            "No se pudieron instalar las dependencias de Node.js"
        )
    
    except Exception as e:
        print(f"❌ Error instalando dependencias de Node.js: {e}")
        sys.exit(1)

def start_backend_frontend(os_name):
    """
    Start backend and frontend processes
    """
    print("🚀 Iniciando aplicación...")
    
    try:
        # Get activation command
        activate_cmd = get_virtual_env_activation_command(os_name)
        
        # Subprocess to run backend
        backend_process = subprocess.Popen(
            f"{activate_cmd} && python app.py",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Subprocess to run frontend
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for processes
        try:
            backend_process.wait()
            frontend_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo procesos...")
            backend_process.terminate()
            frontend_process.terminate()
    
    except Exception as e:
        print(f"❌ Error iniciando procesos: {e}")
        sys.exit(1)

def main():
    """
    Main script to set up and start the application
    """
    try:
        # Detect operating system
        os_name = detect_os()
        
        # Create virtual environment
        create_virtual_environment(os_name)
        
        # Install Python dependencies
        install_python_dependencies(os_name)
        
        # Install Node.js dependencies
        install_node_dependencies()
        
        # Start backend and frontend
        start_backend_frontend(os_name)
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
