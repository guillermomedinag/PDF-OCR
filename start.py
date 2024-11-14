import os
import sys
import subprocess
import platform

def run_command(command, error_message=None, shell=False):
    """
    Run a shell command and handle potential errors
    """
    try:
        if shell:
            # Use subprocess.Popen for shell commands to handle complex commands
            process = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                universal_newlines=True
            )
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"Error: {error_message or 'Command failed'}")
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                sys.exit(1)
            
            print(stdout)
        else:
            # Use subprocess.run for simple commands
            result = subprocess.run(
                command, 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            print(result.stdout)
        
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

def install_system_dependencies(os_name):
    """
    Install system dependencies based on the operating system
    """
    print("🛠️ Instalando dependencias del sistema...")
    
    try:
        if os_name == 'linux':
            # Linux (Ubuntu/Debian) dependencies
            run_command(
                "sudo apt-get update && sudo apt-get install -y python3-venv python3-pip tesseract-ocr poppler-utils nodejs npm",
                "Error instalando dependencias en Linux",
                shell=True
            )
        
        elif os_name == 'darwin':  # macOS
            # macOS dependencies using Homebrew
            run_command(
                "brew update && brew install python tesseract poppler node",
                "Error instalando dependencias en macOS",
                shell=True
            )
        
        elif os_name == 'windows':
            # Windows dependencies using PowerShell
            run_command(
                "powershell -Command \"" +
                "Set-ExecutionPolicy Bypass -Scope Process -Force; " +
                "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; " +
                "if (!(Get-Command choco -ErrorAction SilentlyContinue)) { " +
                "Set-ExecutionPolicy Bypass -Scope Process -Force; " +
                "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')) " +
                "}; " +
                "choco install python nodejs tesseract -y\"",
                "Error instalando dependencias en Windows",
                shell=True
            )
        
        else:
            print(f"⚠️ Sistema operativo no soportado: {os_name}")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error instalando dependencias: {e}")
        sys.exit(1)

def create_virtual_environment(os_name):
    """
    Create Python virtual environment
    """
    print("🐍 Creando entorno virtual de Python...")
    
    try:
        if os_name in ['linux', 'darwin']:
            run_command(
                ["python3", "-m", "venv", "pdfvenv"],
                "No se pudo crear el entorno virtual"
            )
        elif os_name == 'windows':
            run_command(
                ["python", "-m", "venv", "pdfvenv"],
                "No se pudo crear el entorno virtual en Windows"
            )
    
    except Exception as e:
        print(f"❌ Error creando entorno virtual: {e}")
        sys.exit(1)

def activate_virtual_environment(os_name):
    """
    Activate virtual environment based on OS
    """
    print("🔓 Activando entorno virtual...")
    
    activate_cmd = ""
    try:
        if os_name in ['linux', 'darwin']:
            activate_cmd = "source pdfvenv/bin/activate"
        elif os_name == 'windows':
            activate_cmd = ".\\pdfvenv\\Scripts\\Activate"
        else:
            print(f"⚠️ Sistema operativo no soportado: {os_name}")
            sys.exit(1)
        
        return activate_cmd
    
    except Exception as e:
        print(f"❌ Error activando entorno virtual: {e}")
        sys.exit(1)

def install_python_dependencies(activate_cmd):
    """
    Install Python dependencies in virtual environment
    """
    print("📦 Instalando dependencias de Python...")
    
    try:
        run_command(
            f"{activate_cmd} && pip install flask flask-cors ocrmypdf",
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
        run_command(
            ["npm", "install"],
            "No se pudieron instalar las dependencias de Node.js"
        )
    
    except Exception as e:
        print(f"❌ Error instalando dependencias de Node.js: {e}")
        sys.exit(1)

def start_backend_frontend(activate_cmd):
    """
    Start backend and frontend processes
    """
    print("🚀 Iniciando aplicación...")
    
    try:
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
    # Default to an empty string to satisfy Pylint
    activate_cmd = ""
    
    try:
        # Detect operating system
        os_name = detect_os()
        
        # Install system dependencies
        install_system_dependencies(os_name)
        
        # Create virtual environment
        create_virtual_environment(os_name)
        
        # Activate virtual environment
        activate_cmd = activate_virtual_environment(os_name)
        
        # Install Python dependencies
        install_python_dependencies(activate_cmd)
        
        # Install Node.js dependencies
        install_node_dependencies()
        
        # Start backend and frontend
        start_backend_frontend(activate_cmd)
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
