from .constants import *

def copy_data_from_existing_sheet(source_sheet, target_sheet):
    row_index = 1
    # Read the data from the original sheet and copy it to the new sheet
    for row in source_sheet.iter_rows(values_only=True):
        target_sheet.append(row)
        for col_index, cell_value in enumerate(row, start=1):
            target_cell = target_sheet.cell(row=row_index, column=col_index, value=cell_value)
            target_cell.font = bold_font  
        
        row_index += 1