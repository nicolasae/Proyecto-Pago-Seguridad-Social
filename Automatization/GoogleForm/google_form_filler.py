import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
import time

# Obtiene la ruta absoluta del directorio actual
current_directory = os.path.dirname(os.path.abspath(__file__))

# Configuración del controlador del navegador
options = Options()
options.add_argument("--start-maximized")  # Maximizar la ventana del navegador

# Construir la ruta del archivo de Excel relativa al directorio actual
excel_file_path = os.path.join(current_directory, 'datos de prueba.xlsx')

# Abrir el archivo de Excel
wb = openpyxl.load_workbook(excel_file_path)
# Nombre de la hoja 
sheet = wb['data']

# Recorrer las filas del archivo Excel
for row in sheet.iter_rows(min_row=2, values_only=True):  # Ignorar la primera fila de encabezados
    # Crear instancia del navegador
    driver = webdriver.Chrome(options=options)

    url = "https://docs.google.com/forms/d/e/1FAIpQLScWjMdENNLkN0sSnwJNgshG-mXwwYOyvenfu2No3yipTS72qA/viewform"

    # Abrir el formulario de Google
    driver.get(url)

    # Esperar hasta que el div sea visible (aumentar el tiempo de espera a 30 segundos)
    wait = WebDriverWait(driver, 30)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.geS5n')))

    # Encontrar los campos de entrada dentro del div
    input_elements = driver.find_elements(By.CSS_SELECTOR, 'div.geS5n input')

    # Verificar que haya suficientes campos de entrada para llenar con las respuestas
    if len(input_elements) < len(row):
        print("No hay suficientes campos de entrada para llenar con las respuestas.")
        driver.quit()
        break

    # Llenar los campos de entrada con las respuestas de la fila actual
    for i, respuesta in enumerate(row):
        input_elements[i].send_keys(str(respuesta))
        time.sleep(1)  # Agregar un pequeño retardo entre cada respuesta para evitar problemas de velocidad

    # Hacer clic en el botón de envío (ajusta el selector CSS según corresponda)
    submit_button = driver.find_element(By.CSS_SELECTOR, 'div[jsname="M2UYVd"]')
    submit_button.click()

    # Esperar un momento antes de pasar a la siguiente fila (ajusta el tiempo según sea necesario)
    time.sleep(1)

    # Cerrar el navegador
    driver.quit()
