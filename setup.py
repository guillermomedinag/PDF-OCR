from setuptools import setup, find_packages

setup(
    name='pdfocr',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-cors',
        'ocrmypdf'
    ],
    entry_points={
        'console_scripts': [
            'pdfocr=start:main'
        ]
    },
    author='guimed',
    description='PDF OCR Processing Application',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
