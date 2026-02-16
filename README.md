# Altan Replacements Automation 

### Descripción
Sistema RPA desarrollado en Python para automatizar el proceso de reemplazo de tarjetas SIM en el portal de Altan Redes. Este bot elimina el error humano en la captura masiva y reduce los tiempos de operación en un 80%.

### Key Features
- **Navegación Robusta:** Implementación de Selenium con esperas explícitas para manejo de UI asíncrona.
- **Data Integration:** Conexión bidireccional con Google Sheets API para lectura de folios y actualización de estatus.
- **Seguridad:** Arquitectura basada en variables de entorno (`.env`) para protección de credenciales corporativas.

### Stack
- Python 3.x
- Selenium WebDriver
- Gspread (Google Sheets API)
- Colorama (Logs visuales en consola)