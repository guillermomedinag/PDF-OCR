from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import logging
import traceback
import sys
import tempfile

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

        # Usar tempfile para manejar archivos temporales de manera segura
        with tempfile.NamedTemporaryFile(delete=False, suffix='_input.pdf') as temp_input, \
             tempfile.NamedTemporaryFile(delete=False, suffix='_ocr.pdf') as temp_output:
            
            # Guardar el archivo de entrada
            file.save(temp_input.name)
            temp_input.close()
            temp_output.close()

            try:
                # Ejecutar ocrmypdf con forzado de OCR
                result = subprocess.run(
                    ['ocrmypdf', 
                     '--force-ocr',  # Forzar OCR incluso si ya tiene texto
                     temp_input.name, 
                     temp_output.name
                    ], 
                    check=True, 
                    capture_output=True, 
                    text=True
                )
                logger.info(f"OCR processing successful: {result.stdout}")

                # Leer el archivo de salida
                with open(temp_output.name, 'rb') as output_file:
                    response = output_file.read()

                return response, 200, {'Content-Type': 'application/pdf'}

            except subprocess.CalledProcessError as e:
                logger.error(f"OCR processing failed: {e}")
                logger.error(f"STDOUT: {e.stdout}")
                logger.error(f"STDERR: {e.stderr}")
                
                return jsonify({
                    "error": "Error procesando el PDF",
                    "details": str(e),
                    "stdout": e.stdout,
                    "stderr": e.stderr
                }), 500

            finally:
                # Limpiar archivos temporales
                for temp_path in [temp_input.name, temp_output.name]:
                    try:
                        os.unlink(temp_path)
                    except Exception as cleanup_error:
                        logger.error(f"Error eliminando archivo temporal {temp_path}: {cleanup_error}")

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
