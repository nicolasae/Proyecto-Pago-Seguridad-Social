import openpyxl

# Nombre del archivo Excel
nombre_archivo = 'COMPARATIVO PCL Y EKOGUI.xlsx'

# Nombre de la hoja en la que quieres leer los datos
nombre_hoja = 'Hoja1'

# Inicializa los arreglos para almacenar los valores de las columnas A y C
valores_columna_A = []
valores_columna_C = []

try:
    # Abre el archivo Excel
    libro = openpyxl.load_workbook(nombre_archivo)
    
    # Selecciona la hoja especificada
    hoja = libro[nombre_hoja]

    # Itera sobre las filas desde la fila 2 hasta la fila 439
    for fila in hoja.iter_rows(min_row=2, max_row=439, min_col=1, max_col=3):
        valor_A = fila[0].value  # Obtiene el valor de la celda en la columna A
        valor_C = fila[2].value  # Obtiene el valor de la celda en la columna C

        # Comprueba si los valores son None o contienen caracteres especiales
        if valor_A is not None:
            valor_A = str(valor_A).replace('\xa0', '')
            valores_columna_A.append(valor_A)  # Agrega el valor de la columna A al arreglo correspondiente

        if valor_C is not None:
            valor_C = str(valor_C).replace('\xa0', '')
            valores_columna_C.append(valor_C)  # Agrega el valor de la columna C al arreglo correspondiente

    # Cierra el archivo Excel
    libro.close()

    # Imprime los valores almacenados en los arreglos
    print("Valores de la columna A:", valores_columna_A)
    print("Valores de la columna C:", valores_columna_C)

    # Convierte los arreglos en conjuntos para facilitar el cálculo de la diferencia simétrica
    conjunto_A = set(valores_columna_A)
    conjunto_C = set(valores_columna_C)

    # Calcula la diferencia simétrica para encontrar los valores únicos en ambos arreglos
    valores_unicos = list(conjunto_A.symmetric_difference(conjunto_C))


    # Imprime los valores únicos
    print("Valores únicos que no se repiten en ninguno de los dos arreglos:", valores_unicos)

except FileNotFoundError:
    print(f"El archivo '{nombre_archivo}' no fue encontrado.")
except Exception as e:
    print(f"Ocurrió un error: {str(e)}")
