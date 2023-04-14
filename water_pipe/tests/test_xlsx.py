from openpyxl import Workbook, load_workbook

wb = load_workbook("e:/Codes/Python/water-pipe/water_pipe/tests/data.xlsx")
ws = wb.active

print(ws.columns)
for col in ws.values:
    print(col)

print(list(ws.values.__next__()))
