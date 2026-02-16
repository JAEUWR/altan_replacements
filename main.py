import os
import time
from dotenv import load_dotenv
from colorama import Fore, Style, init
from sheets_handler import SheetsManager
from bot_engine import AltanBot

init(autoreset=True)
load_dotenv()

def main():
    # 1. Configuración de recursos
    sm = SheetsManager(
        os.getenv('GOOGLE_CREDS_PATH'),
        ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    )
    
    bot = AltanBot(
        os.getenv('BRAVE_PATH'),
        os.getenv('ALTAN_USER'),
        os.getenv('ALTAN_PASS')
    )

    bot.start()
    bot.login(os.getenv('ALTAN_URL'))

    while True:
        try:
            # 2. Conexión y carga de datos
            conn = sm.connect(os.getenv('MASTER_SHEET'), os.getenv('CRM_SHEET'))
            master_dns = sm.load_master_dns(conn['master'])

            # 3. Procesamiento de Doble Cola
            # --- COLA PRIORITARIA ---
            print(Fore.MAGENTA + Style.BRIGHT + "\n>>> REVISANDO COLA PRIORITARIA: LA ESPERANZA")
            data_prio = sm.mark_rows(conn['esperanza'], "En Cola Prioritaria")
            for i, row in enumerate(data_prio, start=2):
                if "En Cola" in str(row.get("ESTATUS")):
                    bot.process_replacement(conn['esperanza'], i, row, master_dns, os.getenv('TARGET_URL'), validate=False)

            # --- COLA NORMAL ---
            print(Fore.MAGENTA + Style.BRIGHT + "\n>>> REVISANDO COLA NORMAL: FORMULARIO 1")
            data_norm = sm.mark_rows(conn['normal'], "En Cola")
            for i, row in enumerate(data_norm, start=2):
                if "En Cola" in str(row.get("ESTATUS")):
                    bot.process_replacement(conn['normal'], i, row, master_dns, os.getenv('TARGET_URL'), validate=True)

            print(Fore.YELLOW + "\n[INFO] Ciclo finalizado. Durmiendo 60s...")
            time.sleep(60)

        except Exception as e:
            print(Fore.RED + f"[CRITICAL] Error en bucle principal: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()