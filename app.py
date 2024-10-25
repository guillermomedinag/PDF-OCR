from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

# Asegurar que existe el directorio temporal
TEMP_DIR = '/tmp'
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    # Verificar si se ha enviado un archivo PDF
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # Verificar si el archivo tiene un nombre
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Guardar el archivo temporalmente
    temp_file_path = os.path.join(TEMP_DIR, file.filename)
    file.save(temp_file_path)

    # Ruta del archivo de salida
    output_file_path = os.path.join(TEMP_DIR, f"ocr_{file.filename}")

    try:
        # Ejecutar el comando ocrmypdf
        subprocess.run(['ocrmypdf', temp_file_path, output_file_path], check=True)

        # Leer el archivo de salida y devolverlo como respuesta
        with open(output_file_path, 'rb') as output_file:
            response = output_file.read()

        # Eliminar los archivos temporales
        os.remove(temp_file_path)
        os.remove(output_file_path)

        # Devolver el archivo procesado como respuesta
        return response, 200, {'Content-Type': 'application/pdf'}

    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Asegurar que los archivos temporales se eliminan incluso si hay errores
        for file_path in [temp_file_path, output_file_path]:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass

if __name__ == '__main__':
    app.run(debug=True)