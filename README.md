# PDF OCR Application - Multiplataforma

## Descripción General

Aplicación de Procesamiento OCR de Documentos PDF compatible con Linux, macOS y Windows:

- Frontend: React, TypeScript, Tailwind CSS
- Backend: Flask (Python)
- Procesamiento OCR: ocrmypdf

## Requisitos Previos

### Todas las Plataformas

- Python 3.10+
- Node.js 18+
- npm o yarn
- Git

### Dependencias Específicas por Plataforma

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y \
  python3-venv \
  python3-pip \
  tesseract-ocr \
  poppler-utils \
  nodejs \
  npm
```

#### macOS (con Homebrew)

```bash
# Instalar Homebrew si no está instalado
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependencias
brew install \
  python \
  tesseract \
  poppler \
  node
```

#### Windows

1. Descargar e instalar:
   - Python 3.10+ desde python.org
   - Node.js 18+ desde nodejs.org
   - Git desde git-scm.com

2. Instalar Tesseract OCR:
   - Descargar desde: <https://github.com/UB-Mannheim/tesseract/wiki>
   - Añadir al PATH del sistema

## Configuración del Proyecto

### Método Automático (Todas las Plataformas)

```bash
# Clonar repositorio
git clone <url-del-repositorio>
cd pdf-ocr-application

# Ejecutar script de configuración
python start.py
```

### Método Manual

#### 1. Crear Entorno Virtual

```bash
# Linux/macOS
python3 -m venv pdfvenv
source pdfvenv/bin/activate

# Windows (PowerShell)
python -m venv pdfvenv
.\pdfvenv\Scripts\Activate
```

#### 2. Instalar Dependencias de Python

```bash
# Todas las plataformas
pip install flask flask-cors ocrmypdf
```

#### 3. Instalar Dependencias de Node.js

```bash
# Todas las plataformas
npm install
```

## Ejecución de la Aplicación

### Iniciar Backend

```bash
# Linux/macOS
source pdfvenv/bin/activate
python app.py

# Windows (PowerShell)
.\pdfvenv\Scripts\Activate
python app.py
```

### Iniciar Frontend

```bash
# Todas las plataformas
npm run dev
```

## Solución de Problemas

### Verificación de Instalación

```bash
# Verificar versiones
python --version
node --version
ocrmypdf --version
```

### Errores Comunes

- Asegúrate de usar la versión correcta de Python
- Activa el entorno virtual antes de instalar dependencias
- Verifica que Tesseract OCR esté correctamente instalado
- Comprueba que todas las dependencias estén instaladas

### Soporte Específico por Plataforma

#### Linux

- Usar `sudo` para instalaciones del sistema
- Verificar permisos de archivos

#### macOS

- Usar Homebrew para gestionar dependencias
- Verificar configuración de Python del sistema

#### Windows

- Usar PowerShell o CMD como administrador
- Verificar configuración de variables de entorno
- Usar Windows Subsystem for Linux (WSL) si hay problemas

## Contribuciones

1. Haz un fork del repositorio
2. Crea una rama para tu característica
3. Commit de tus cambios
4. Push a la rama
5. Abre un Pull Request

## Licencia

Operaciones bajo la licencia MIT.

## Contacto

gh.medinag@gmail.com
