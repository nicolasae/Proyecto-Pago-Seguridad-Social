from django.shortcuts import render
from django.contrib import messages

from document_upload.models import *
from .report_planilla import *
from .report_patronales import *
from .report_temporales import *
from .report_permanentes import *
from .report_deducciones import *
from .revision import *
from .consolidado import *

def download_view(request):
    if request.method == 'POST':
        selected_year = request.POST.get('selectYear')
        selected_month = request.POST.get('selectMonth')

        if 'btn_resumen_planilla' in request.POST:
            return create_report_planilla(request, selected_year, selected_month)
           
        if 'btn_resumen_patronales' in request.POST:
            return create_report_patronales(request, selected_year, selected_month)
        
        if 'btn_resumen_patronales_temporales' in request.POST:
            return create_report_temporales(request, selected_year, selected_month)
        
        if 'btn_resumen_patronales_permanentes' in request.POST:
            return create_report_permanentes(request, selected_year, selected_month)           
        
        if 'btn_resumen_deducciones' in request.POST:
            return create_report_deducciones(request, selected_year, selected_month)           
        
        if 'btn_revision' in request.POST:
            return create_revision(request, selected_year, selected_month)           
        
        if 'btn_consolidado' in request.POST:
            return create_report_consolidado(request, selected_year, selected_month)           
        
    
    return render(request, 'reports.html')

def create_report_planilla(request,year,month):
    date = year + '/' + month
    info_planilla = get_info_planilla(date)

    if info_planilla.exists():       
        values_planilla = get_values_planilla(date)   
        response = generate_excel_report(info_planilla, values_planilla, year, month)
    
        return response       
    else:
        context = {
            'show_alert': True,
            'alert_type':"danger",
            'message':f'No hay información disponible de la planilla del periodo: {date}.',
        }        
        return render(request, 'reports.html', context)
        
def create_report_patronales(request, year, month):
    date = year + '/' + month
    data = get_data_patronales(date)
    
    if len(data) > 0:
        return generate_excel_report_patronales(data,year,month)
    else:
        context = {
            'show_alert': True,
            'alert_type':"danger",
            'message':f'No hay información disponible de patronales para el periodo: {date}.',
        }        
        return render(request, 'reports.html', context)

def create_report_temporales(request,year,month):
    date = year + '/' + month
    data_temporales = get_data_temporales(date)

    if len(data_temporales) > 0:
        return generate_excel_report_temporales(data_temporales, year, month)
    else:
        context = {
            'show_alert': True,
            'alert_type':"danger",
            'message':f'No hay información disponible de patronales temporales para el periodo: {date}.',
        }        
        return render(request, 'reports.html', context)

def create_report_permanentes(request,year, month):
    date = year + '/' + month
    data_permanentes = get_data_permanentes(date)

    if (len(data_permanentes) > 0):
        return generate_excel_report_permanentes(data_permanentes, year, month)
    else:
        context = {
            'show_alert': True,
            'alert_type':"danger",
            'message':f'No hay información disponible de patronales permanentes para el periodo: {date}.',
        }        
        return render(request, 'reports.html', context)

def create_revision(request, year, month):
    return revision(request,year,month)

def create_report_deducciones(request, year, month):
    date = year + '/' + month
    data = get_data_deducciones(date)
   
    if len(data) > 0:
        return generate_excel_report_deducciones(data,year,month)
    else:
        context = {
            'show_alert': True,
            'alert_type':"danger",
            'message':f'No hay información disponible de deducciones para el periodo: {date}.',
        }        
        return render(request, 'reports.html', context)

def create_report_consolidado(request, year, month):
    date = year + '/' + month
    data = get_data_values(date)
    
    if data is not None and all(data.values()):
        return generate_excel_report_consolidado(data,year,month)
    else:
        context = {
            'show_alert': True,
            'alert_type':"danger",
            'message':f'No hay información disponible para realizar un informe consolidado del periodo: {date}.',
        }        
        return render(request, 'reports.html', context)