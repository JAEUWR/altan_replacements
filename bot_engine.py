import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore

class AltanBot:
    def __init__(self, brave_path, user, password):
        self.brave_path = brave_path
        self.user = user
        self.password = password
        self.driver = None

    def start(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = self.brave_path
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

    def login(self, url):
        while True:
            self.driver.get(url)
            try:
                wait = WebDriverWait(self.driver, 20)
                wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(self.user)
                wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(self.password)
                wait.until(EC.element_to_be_clickable((By.ID, "consulta"))).click()
                wait.until(EC.presence_of_element_located((By.ID, "toggle_mobile_nav")))
                print(Fore.GREEN + "[SUCCESS] Sesión iniciada en Altán.")
                return
            except Exception:
                print(Fore.RED + "[ERROR] Error en login, reintentando...")
                time.sleep(5)

    def check_session(self):
        try:
            self.driver.find_element(By.ID, "toggle_mobile_nav")
        except:
            print(Fore.YELLOW + "[WARN] Sesión perdida, re-logueando...")
            self.login("https://360.altanredes.com")

    def process_replacement(self, sheet, index, row, master_dns, target_url, validate=True):
        dn = str(row["DN"]).strip()
        icc = str(row["ICC"]).strip()

        # Validaciones Previas
        if len(dn) != 10 or not dn.isdigit():
            self._update_sheet(sheet, index, "Fallido", "DN debe tener 10 dígitos")
            return

        if validate and dn not in master_dns:
            self._update_sheet(sheet, index, "Fallido", "DN NO ENCONTRADO EN MAESTRO")
            return

        # Flujo Selenium
        try:
            self.driver.get(target_url)
            self.check_session()
            wait = WebDriverWait(self.driver, 25)

            # Paso 1: DN
            wait.until(EC.presence_of_element_located((By.ID, "inputData"))).send_keys(dn)
            wait.until(EC.element_to_be_clickable((By.ID, "next"))).click()
            time.sleep(5)

            # Validar errores del portal
            try:
                err = self.driver.find_element(By.ID, "message_error").text.strip()
                if err:
                    self._update_sheet(sheet, index, "Fallido", err)
                    return
            except: pass

            # Validar si ya existe
            try:
                curr_icc = wait.until(EC.presence_of_element_located((By.ID, "seticc"))).text.strip()
                if curr_icc.lower() == icc.lower():
                    self._update_sheet(sheet, index, "Exitoso", "Trámite ya realizado previamente")
                    return
            except: pass

            # Paso 2: Nuevo ICC
            wait.until(EC.presence_of_element_located((By.ID, "secondstep"))).send_keys(icc)
            finish_btn = wait.until(EC.element_to_be_clickable((By.ID, "finish")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", finish_btn)
            finish_btn.click()
            time.sleep(15)

            # Captura de Resultado Final
            msg = wait.until(EC.presence_of_element_located((By.ID, "message"))).text
            if "Id :" in msg:
                folio = msg.split("Id : ")[1].strip()
                sheet.update_cell(index, 5, "Exitoso")
                sheet.update_cell(index, 6, folio)
                sheet.update_cell(index, 7, "Trámite Exitoso")
                print(Fore.GREEN + f"[OK] Fila {index} procesada. Folio: {folio}")
            else:
                self._update_sheet(sheet, index, "Fallido", msg)

        except Exception as e:
            self._update_sheet(sheet, index, "Fallido", str(e)[:50])

    def _update_sheet(self, sheet, row, status, msg):
        sheet.update_cell(row, 5, status)
        sheet.update_cell(row, 7, msg)
        print(Fore.RED + f"[X] Fila {row}: {msg}")