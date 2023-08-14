from openpyxl.styles import Font, Alignment, NamedStyle

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
bold_font = Font(bold=True)
left_alignment = Alignment(horizontal='left')
currency_style = NamedStyle(name='currency_style', number_format='"$"#,##0')
center_alignment = Alignment(horizontal="center", vertical="center")