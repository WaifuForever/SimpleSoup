import xlsxwriter
from extract import Extract


workbook = xlsxwriter.Workbook('Articles.xlsx')
worksheet = workbook.add_worksheet()

 
worksheet.write(0, 0, "Title")
worksheet.write(0, 1, "Abstract")
worksheet.write(0, 2, "Date")
worksheet.write(0, 3, "Authors")


print("starting...")
ext = Extract(workbook, worksheet)

#ext.search("sciencedirect")
ext.search("arxiv")
workbook.close()