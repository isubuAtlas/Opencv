#!/bin/bash

# Update and install system dependencies (optional, for Linux/WSL environments)
if [ -f /etc/debian_version ]; then
    echo "Updating system and installing system dependencies for pyzbar..."
    sudo apt-get update
    sudo apt-get install -y libzbar0
fi

# Create a virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies from requirements.txt..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found!"
    exit 1
fi

echo "Installation complete."
