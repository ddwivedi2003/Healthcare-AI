#!/bin/bash

# Update package lists
sudo apt-get update

# Install distutils
sudo apt-get install -y python3-distutils

# Install Tesseract OCR
sudo apt-get install -y tesseract-ocr

# Install Python dependencies
pip install -r requirements.txt
