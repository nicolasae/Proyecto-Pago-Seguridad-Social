import requests

# URL del punto final del formulario de Google
form_url = 'https://docs.google.com/forms/u/0/d/e/1FAIpQLScM6_nEFm7IZbtLcpUipY9uHpN2G_8_5_Oxk9MOBi18X6qBng/formResponse'

# Datos de las respuestas
data = {
    'entry.760956106': 'adriana',
    'entry.177861697': 'exco@exco.com ',
}

# Realizar la solicitud HTTP POST
response = requests.post(form_url, data=data)

# Verificar el estado de la respuesta
if response.status_code == 200:
    print('Respuestas enviadas correctamente.')
else:
    print('Error al enviar las respuestas.')
