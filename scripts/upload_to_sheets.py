#!/usr/bin/env python3
"""
Sube un archivo Excel (.xlsx) a Google Drive y lo convierte automáticamente a Google Sheets.
Usa OAuth 2.0 para autenticarse con la cuenta de Google del usuario.
"""

import os
import sys
import argparse
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scope necesario: drive.file permite crear y gestionar archivos creados por esta app
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_credentials(credentials_path: Path, token_path: Path):
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                print(f"Error: No se encontró el archivo de credenciales en:\n  {credentials_path}")
                print("\nPara obtenerlo:")
                print("1. Ve a https://console.cloud.google.com/")
                print("2. Habilita la 'Google Drive API'.")
                print("3. En 'Pantalla de consentimiento de OAuth', pon modo 'Externo' y añade tu email como usuario de prueba.")
                print("4. En 'Credenciales', crea 'ID de cliente de OAuth' -> Tipo: 'App de escritorio'.")
                print(f"5. Descarga el JSON y colócalo en: {credentials_path}\n")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds

def upload_xlsx_to_sheets(file_path: str, title: str = None, credentials_path: str = None):
    source_file = Path(file_path).expanduser().resolve()
    if not source_file.exists():
        print(f"Error: El archivo {source_file} no existe.")
        sys.exit(1)

    base_dir = Path(__file__).parent.resolve()

    if credentials_path:
        cred_p = Path(credentials_path).expanduser().resolve()
    else:
        possible_paths = [
            base_dir / "credentials.json",
            Path("/home/mass/Projects/muebles-liquidacion/credentials.json"),
            Path.home() / "Downloads" / "credentials.json",
        ]
        # También buscar cualquier client_secret*.json o credentials*.json descargado en Downloads
        downloads_dir = Path.home() / "Downloads"
        if downloads_dir.exists():
            possible_paths.extend(downloads_dir.glob("client_secret*.json"))
            possible_paths.extend(downloads_dir.glob("credentials*.json"))

        cred_p = next((p for p in possible_paths if p.exists()), base_dir / "credentials.json")

    token_p = base_dir / "token.json"

    print("Autenticando con Google Drive API...")
    creds = get_credentials(cred_p, token_p)
    service = build('drive', 'v3', credentials=creds)

    sheet_title = title or source_file.stem
    print(f"Subiendo '{source_file.name}' como Google Spreadsheet '{sheet_title}'...")

    file_metadata = {
        'name': sheet_title,
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }
    media = MediaFileUpload(
        str(source_file),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        resumable=True
    )

    request = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Progreso: {int(status.progress() * 100)}%")

    print("\n¡Subida completada con éxito!")
    print(f"Título: {response.get('name')}")
    print(f"ID: {response.get('id')}")
    print(f"Enlace de Google Sheets: {response.get('webViewLink')}")
    return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Subir archivo Excel a Google Sheets")
    parser.add_argument("file", help="Ruta al archivo .xlsx")
    parser.add_argument("--name", "-n", help="Título del Google Sheet (opcional)")
    parser.add_argument("--credentials", "-c", help="Ruta a credentials.json (opcional)")
    args = parser.parse_args()

    upload_xlsx_to_sheets(args.file, args.name, args.credentials)
