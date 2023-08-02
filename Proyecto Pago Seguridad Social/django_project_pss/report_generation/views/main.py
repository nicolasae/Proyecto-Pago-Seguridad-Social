from django.shortcuts import render, redirect

from document_upload.models import *
from .report_planilla import *
from .report_patronales import *
from .report_temporales import *
from .report_permanentes import *

def download_view(request):
    if request.method == 'POST':
        selected_year = request.POST.get('selectYear')
        selected_month = request.POST.get('selectMonth')
        show_alert = False

        # try:
        #     context = {
        #         'show_alert': True,
        #         'alert_type':"success",
        #         'message':'El archivo se ha procesado correctamente.',
        #     }

        if 'btn_resumen_planilla' in request.POST:
            # Acción para generar el resumen de la planilla
            return create_report_planilla(selected_year,selected_month)
        
        if 'btn_resumen_patronales' in request.POST:
            # Acción para generar el resumen de la planilla
            return create_report_patronales(selected_year,selected_month)
        
        if 'btn_resumen_patronales_temporales' in request.POST:
            # Aquí puedes realizar la acción para generar el resumen de las patronales           
            return create_report_temporales(selected_year, selected_month)
        
        if 'btn_resumen_patronales_permanentes' in request.POST:
            # Aquí puedes realizar la acción para generar el resumen de las patronales           
            return create_report_permanentes(selected_year, selected_month)
            
        # except Exception as e:
        #     context = {
        #         'show_alert': True,
        #         'alert_type':"danger",
        #         'message':'Ocurrió un error al descargar el archivo.',
        #     }

        #     # Error handling if something goes wrong while processing the file
        #     print(f"Error processing the file: {str(e)}")

        #     # You can add an error message in the response or redirect to an error page
        #     return render(request, 'reports.html', context)  
    
    # return redirect('reportes')
    return render(request, 'reports.html')

def create_report_planilla(year,month):
    date = year + '/' + month
    info_planilla = get_info_planilla(date)
    values_planilla = get_values_planilla(date)
    return generate_excel_report(info_planilla,values_planilla, year, month)

def create_report_patronales(year,month):
    return generate_excel_report_patronales(year,month)


def create_report_temporales(year, month):
    date = year + '/' + month
    data_temporales = get_data_temporales(date)
    return generate_excel_report_temporales(data_temporales, year, month)

def create_report_permanentes(year, month):
    date = year + '/' + month
    data_permanentes = get_data_permanentes(date)
    return generate_excel_report_permanentes(data_permanentes, year, month)


