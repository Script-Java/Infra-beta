#!/bin/bash
# Simple setup script to install backend and frontend dependencies

# Install Python dependencies
if [ -f backend/requirements.txt ]; then
    echo "Installing Python packages..."
    pip install -r backend/requirements.txt || exit 1
fi

# Install Node.js dependencies
if [ -f frontend/infra-beta/package.json ]; then
    echo "Installing frontend packages..."
    npm install --prefix frontend/infra-beta || exit 1
fi

echo "Setup complete."
