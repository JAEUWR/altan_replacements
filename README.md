# Altan Replacements Automation

### Descripción
Sistema RPA desarrollado en Python diseñado para la automatización integral del proceso de reemplazo de tarjetas SIM en el portal mayorista de Altan Redes. La solución aborda la problemática de la captura masiva de datos mediante un motor de navegación robusto que garantiza la precisión operativa y la integridad de la información procesada.

### Key Features
- **Navegación Robusta:** Implementación de Selenium WebDriver con estrategias de esperas explícitas y condiciones esperadas para la gestión de interfaces web asíncronas.
- **Integración de Datos:** Conexión bidireccional con Google Sheets API a través de la librería Gspread, permitiendo la lectura de entradas y la actualización de estados de ejecución en tiempo real.
- **Seguridad Corporativa:** Arquitectura desacoplada mediante el uso de variables de entorno (.env) para la protección de credenciales y llaves de acceso.
- **Arquitectura Modular:** Estructura de código organizada en módulos independientes para el motor de navegación, gestión de hojas de cálculo y orquestador principal.

### Stack
- Python 3.x
- Selenium WebDriver
- Google Sheets API / OAuth2
- Python-dotenv
- Colorama (Logs de consola)