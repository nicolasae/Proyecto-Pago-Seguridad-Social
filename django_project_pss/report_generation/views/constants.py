from openpyxl.styles import Font, Alignment, NamedStyle, Border, Side

PERSONALIZED_ORDER = [
    'PENSION',
    'SALUD',
    'RIESGOS PROFESIONALES',
    'CAJA DE COMPENSACION FAMILIAR',
    'ICBF',
    'SENA',
    'ESAP',
    'MEN',
]

# Styles
header_style = Font(name='Arial Nova Cond Light', size=11, bold=True) 
font_style = Font(name='Arial Nova Cond Light', size=11)
bold_font = Font(bold=True)
left_alignment = Alignment(horizontal='left')
currency_style = NamedStyle(name='currency_style', number_format='"$"#,##0')
center_alignment = Alignment(horizontal="center", vertical="center")

# Crear un estilo de borde
border_style = Border(left=Side(style='thin'),
                      right=Side(style='thin'),
                      top=Side(style='thin'),
                      bottom=Side(style='thin'))