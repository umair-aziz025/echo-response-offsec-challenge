import zipfile
import xml.etree.ElementTree as ET

# Read the Excel file as a zip
xlsx_file = 'echo_trail/InteractiveSignIns_2025-08-14_2025-08-15.xlsx'
with zipfile.ZipFile(xlsx_file) as z:
    # Read shared strings
    strings_xml = z.read('xl/sharedStrings.xml')
    root = ET.fromstring(strings_xml)
    
    # Extract all strings
    strings = []
    for si in root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'):
        strings.append(si.text if si.text else '')
    
    # Read sheet data
    sheet_xml = z.read('xl/worksheets/sheet1.xml')
    sheet_root = ET.fromstring(sheet_xml)
    
    # Find rows
    rows = []
    for row in sheet_root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
        row_data = []
        for cell in row.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
            value = cell.find('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
            if value is not None and value.text:
                # If it's a string reference (type 's'), look it up
                if cell.get('t') == 's':
                    idx = int(value.text)
                    row_data.append(strings[idx])
                else:
                    row_data.append(value.text)
            else:
                row_data.append('')
        rows.append(row_data)
    
    # Print header
    if rows:
        print("Number of columns:", len(rows[0]))
        for i, h in enumerate(rows[0][:35]):
            print(f"  Col {i}: {h}")
        print("\n" + "="*80 + "\n")
        
        # Look for enygaard entries with Success status
        for i, row in enumerate(rows[1:], 1):
            if len(row) > 6:
                # Check if enygaard appears in the row
                row_str = ' '.join(str(x) for x in row).lower()
                if 'nygaard' in row_str:
                    print(f"Row {i}:")
                    for j in range(min(35, len(row))):
                        if row[j]:
                            print(f"  [{j}] {rows[0][j] if j < len(rows[0]) else 'Col'+str(j)}: {row[j]}")
                    print("\n" + "-"*80 + "\n")
