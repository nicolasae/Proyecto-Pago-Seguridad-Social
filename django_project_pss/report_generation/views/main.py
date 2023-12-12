import os
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from document_upload.models import *
import zipfile

from .report_planilla import *
from .report_patronales import *
from .report_deducciones import *
from .consolidado.main import *

def download_view(request):
    if request.method == 'POST':
        selected_year = request.POST.get('selectYear')
        selected_month = request.POST.get('selectMonth')

        if 'btn_resumen_planilla' in request.POST:
            return create_report_planilla(request, selected_year, selected_month)
           
        if 'btn_resumen_patronales' in request.POST:
            return create_report_patronales(request, selected_year, selected_month)
        
        if 'btn_resumen_deducciones' in request.POST:
            return create_report_deducciones(request, selected_year, selected_month)                                
        
        if 'btn_consolidado' in request.POST:
            return create_report_consolidado(request, selected_year, selected_month)
        
        if 'btn_descargar' in request.POST:
            return download_documents(request, selected_year, selected_month)             
    
    return render(request, 'reports.html')

def create_report_planilla(request,year,month):
    date = year + '/' + month
    info_planilla = get_info_planilla(date)

    if info_planilla.exists():       
        values_planilla = get_values_planilla(date)   
        response = generate_excel_report_planilla(info_planilla, values_planilla, year, month)
    
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
        return generate_excel_report(data,year,month)
    else:
        context = {
            'show_alert': True,
            'alert_type':"danger",
            'message':f'No hay información disponible para realizar un informe consolidado del periodo: {date}.',
        }        
        return render(request, 'reports.html', context)
    
def download_documents(request,year,month):
    folder_path = os.path.join(settings.MEDIA_ROOT, 'xlsx', year, month)
    
    context = {
        'show_alert': True,
        'alert_type':"danger",
        'message':f'No hay documentos disponibles para descargar del periodo: {year}/{month}.',
    }        
    if not os.path.exists(folder_path):
        return render(request, 'reports.html', context)
    
    # Get file list by directory 
    files_in_folder = os.listdir(folder_path)

    # Check if the folder is empty 
    if not files_in_folder:     
        return render(request, 'reports.html', context)

    filename = f"documentos_subidos-{year}/{month}"
    # Create a ZIP file in memory
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={filename}.zip'

    memory_zip = zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED)

    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            arcname = os.path.relpath(filepath, folder_path)
            memory_zip.write(filepath, arcname)

    # Close the ZIP file
    memory_zip.close()

    return response
