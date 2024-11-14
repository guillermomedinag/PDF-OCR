@echo off
REM Batch script for starting PDF OCR application on Windows

REM Check if virtual environment exists, create if not
if not exist "pdfvenv" (
    python -m venv pdfvenv
)

REM Activate virtual environment
call pdfvenv\Scripts\activate

REM Install Python dependencies
pip install flask flask-cors ocrmypdf

REM Start backend in a new command prompt
start cmd /k "python app.py"

REM Start frontend in another command prompt
start cmd /k "npm run dev"

echo Application started. Close command prompts to stop.
