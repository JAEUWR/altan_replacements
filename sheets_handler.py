import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
from colorama import Fore

class SheetsManager:
    def __init__(self, creds_path, scope):
        self.creds_path = creds_path
        self.scope = scope
        self.client = self._authenticate()

    def _authenticate(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_path, self.scope)
        return gspread.authorize(creds)

    def connect(self, master_name, crm_name):
        """Establece conexión con las hojas necesarias."""
        spreadsheet_remplazos = self.client.open(crm_name)
        spreadsheet_master = self.client.open(master_name)
        
        return {
            "esperanza": spreadsheet_remplazos.worksheet("La Esperanza"),
            "normal": spreadsheet_remplazos.worksheet("Respuestas de formulario 1"),
            "master": spreadsheet_master.worksheet("ABR25-MAY25")
        }

    def load_master_dns(self, master_sheet):
        """Carga DNs en un set para búsqueda O(1)."""
        while True:
            try:
                print(Fore.CYAN + "[INFO] Sincronizando base maestra...")
                dns_list = master_sheet.col_values(1)
                return set(str(dn) for dn in dns_list)
            except Exception as e:
                print(Fore.RED + f"[ERROR] Reintentando carga de maestro: {e}")
                time.sleep(15)

    def mark_rows(self, sheet, queue_name):
        """Marca filas vacías para procesamiento."""
        data = sheet.get_all_records()
        counter = 1
        for index, row in enumerate(data, start=2):
            if not row.get("ESTATUS"):
                sheet.update_cell(index, 5, f"{queue_name} #{counter}")
                counter += 1
        return data