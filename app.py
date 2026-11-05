"""Punto de entrada.

Desarrollo:   python app.py
Producción:   APP_ENV=production python app.py   (sirve con Waitress, sin nginx)
"""
import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    if os.getenv("APP_ENV", "development") == "production":
        from waitress import serve
        serve(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)), threads=8)
    else:
        app.run(debug=True)
