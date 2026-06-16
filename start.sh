#!/bin/bash
if ! command -v python3 &> /dev/null; then
    echo "Python 3 wurde nicht gefunden."
    echo "Bitte Python von https://www.python.org installieren."
    exit 1
fi

python3 main.py
