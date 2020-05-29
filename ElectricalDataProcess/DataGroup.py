"""
功能： 对输入文件进行分组 7*48为一个基本单元
输出文件格式：xlsx
第一列 用户名     第二列 窃电标签    第三列数据
"""

import xlrd, xlsxwriter


data = xlrd.open_workbook("../test1.xlsx")
print("原始文件已经打开")
data_sheet = data.sheets()[0]
workbook = xlsxwriter.Workbook("output_test.xlsx")  # 创建输出对象
output_sheet = workbook.add_worksheet()

total_col_number = len(data_sheet.row_values(0))-1
total_row_number = len(data_sheet.col_values(0))-1

col=0
row=0
for i in range(total_col_number):

    for j in range(21504):
        output_sheet.write(row, 0, "00" + str(row))  # 写入用户名
        output_sheet.write(row, 1, "1")  # 写入标签 1表示正常数据 -1表示异常数据

        output_sheet.write(row, col+2, str(data_sheet.cell_value(j+1, i+1)))

        if ((i * 21504)+j+1) % 336 == 0:
            row += 1
            col = 0
        else:
            col += 1

    print("完成度：", i+1, " / ", total_col_number)

workbook.close()
