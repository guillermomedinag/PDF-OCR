from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import logging
import traceback
import sys

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('ocr_processing.log')
    ]
)
logger = logging.getLogger(__name__)

# Asegurar que existe el directorio temporal
TEMP_DIR = '/tmp'
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    try:
        # Verificar si se ha enviado un archivo PDF
        if 'file' not in request.files:
            logger.error("No file part in the request")
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        # Verificar si el archivo tiene un nombre
        if file.filename == '':
            logger.error("No selected file")
            return jsonify({"error": "No selected file"}), 400

        # Verificar si es un PDF
        if not file.filename.lower().endswith('.pdf'):
            logger.error(f"Invalid file type: {file.filename}")
            return jsonify({"error": "Solo se permiten archivos PDF"}), 400

        # Obtener el nombre base y la extensión del archivo
        filename_without_ext = os.path.splitext(file.filename)[0]
        output_filename = f"{filename_without_ext}_ocr.pdf"

        # Guardar el archivo temporalmente
        temp_file_path = os.path.join(TEMP_DIR, file.filename)
        output_file_path = os.path.join(TEMP_DIR, output_filename)

        file.save(temp_file_path)

        # Verificar si el archivo se guardó correctamente
        if not os.path.exists(temp_file_path):
            logger.error(f"Failed to save temporary file: {temp_file_path}")
            return jsonify({"error": "No se pudo guardar el archivo temporalmente"}), 500

        try:
            # Verificar dependencias de ocrmypdf
            subprocess.run(['which', 'ocrmypdf'], check=True)

            # Ejecutar el comando ocrmypdf con verificaciones adicionales
            result = subprocess.run(
                ['ocrmypdf', 
                 '--skip-text',  # Skip OCR if PDF already has text
                 '--clean',      # Clean up temporary files
                 temp_file_path, 
                 output_file_path
                ], 
                check=True, 
                capture_output=True, 
                text=True
            )
            logger.info(f"OCR processing successful: {result.stdout}")

        except subprocess.CalledProcessError as e:
            logger.error(f"OCR processing failed: {e}")
            logger.error(f"STDOUT: {e.stdout}")
            logger.error(f"STDERR: {e.stderr}")
            
            # Intentar eliminar archivos temporales
            for path in [temp_file_path, output_file_path]:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except Exception as cleanup_error:
                        logger.error(f"Error cleaning up file {path}: {cleanup_error}")
            
            return jsonify({
                "error": "Error procesando el PDF",
                "details": str(e),
                "stdout": e.stdout,
                "stderr": e.stderr
            }), 500

        # Verificar si el archivo de salida existe
        if not os.path.exists(output_file_path):
            logger.error(f"Output file not created: {output_file_path}")
            return jsonify({"error": "No se pudo generar el archivo OCR"}), 500

        # Leer el archivo de salida y devolverlo como respuesta
        with open(output_file_path, 'rb') as output_file:
            response = output_file.read()

        # Eliminar los archivos temporales
        os.remove(temp_file_path)
        os.remove(output_file_path)

        # Devolver el archivo procesado como respuesta
        return response, 200, {'Content-Type': 'application/pdf'}

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": "Error inesperado al procesar el documento",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    # Verificar dependencias antes de iniciar
    try:
        subprocess.run(['which', 'ocrmypdf'], check=True)
        logger.info("ocrmypdf is installed and accessible")
    except subprocess.CalledProcessError:
        logger.error("ocrmypdf is not installed or not in PATH")
        sys.exit(1)

    app.run(debug=True, host='0.0.0.0', port=5000)
