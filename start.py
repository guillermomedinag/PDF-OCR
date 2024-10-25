import subprocess
import os
import sys

# Define las rutas a tu servidor y frontend
backend_script = 'backend/app.py' 
frontend_dir = os.path.join(os.path.dirname(__file__),'frontend')
# Inicia el servidor backend
def start_backend():
    return subprocess.Popen([sys.executable, backend_script])

# Inicia el frontend
def start_frontend():
    os.chdir(frontend_dir)  
    return subprocess.Popen(['npm', 'run', 'dev'])

if __name__ == '__main__':
    backend_process = start_backend()
    frontend_process = start_frontend()

    try:
        # Espera a que ambos procesos terminen
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        # Si se interrumpe, cierra ambos procesos
        backend_process.terminate()
        frontend_process.terminate()