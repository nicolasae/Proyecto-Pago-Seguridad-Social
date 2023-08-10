from openpyxl.styles import Font, Alignment, NamedStyle

PERSONALIZED_ORDER = [
    'SALUD',
    'RIESGOS PROFESIONALES',
    'PENSION',
    'MEN',
    'SENA',
    'ESAP',
    'ICBF',
    'CAJA DE COMPENSACION FAMILIAR',
]

# Styles
bold_font = Font(bold=True)
left_alignment = Alignment(horizontal='left')
currency_style = NamedStyle(name='currency_style', number_format='"$"#,##0')
center_alignment = Alignment(horizontal="center", vertical="center")