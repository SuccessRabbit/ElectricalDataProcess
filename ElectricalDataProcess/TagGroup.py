"""
功能：对分组后的文件进行随机选取随机运算，生成有标签数据集
输入文件格式： xlsx
输出文件格式： xlsx
"""

import xlrd, xlsxwriter, random, numpy


def function1(origin) -> numpy.ndarray:  # 对所有元素同时乘以一个随即小数 返回一个ndarray
    x = numpy.array(origin)
    y = x * random.randint(0, 100) / 10000
    return y


def function2(origin) -> list:  # 随机选中其中的一段随机长度的序列 将这段序列的值置为0 其余保持不变 返回一个列表
    choose = random.randint(0, 6)
    temp = origin[choose * 48:(choose + 1) * 48]  # 随机选择一段序列
    min_off_time = 8
    start_time = random.randint(0, 47 - min_off_time)
    duration = random.randint(min_off_time, 48)
    end_time = start_time + duration
    try:
        for _ in range(start_time, end_time):
            temp[_] = 0
    except:
        pass
    j = 0
    for i in range(choose * 48, (choose + 1) * 48):
        origin[i] = temp[j]
        j += 1
    return origin


def function3(origin) -> numpy.ndarray:  # 对所有元素分别乘以一个不同的随机小数 返回一个ndarray
    x = numpy.array(origin)
    col_vector = []
    for i in range(336):
        col_vector.append(random.randint(0, 100) / 10000)
    random_vector = numpy.array(col_vector)
    return x*random_vector


def function4(origin) -> list:  # 峰时段和平常时段的用电数据全部转移到谷时段
    average = 0
    size = len(origin)
    peak = []
    for i in range(7):
        for j in range(48):
            if 18 <= j <= 23 or 37 <= j <= 46:
                peak.append(origin[i*48 + j] - 0.001)
                origin[i * 48 + j] = 0.001
            elif 15 <= j <= 17 or 24 <= j <= 36:
                peak.append(origin[i * 48 + j] - 0.01)
                origin[i * 48 + j] = 0.01

    peak_all = 0
    for i in peak:
        peak_all += i
    for i in range(7):
        for j in range(48):
            if 1 <= j <= 14 or 47 <= j <= 48:
                origin[i*48 + j] += peak_all / len(peak)

    return origin


def function5(origin) -> list:  # 从某个时刻开始，后面的数据全是0
    split = random.randint(100, 180)
    for i in range(split, 336):
        origin[i] *= random.randint(0, 100) / 10000

    return origin


def function6(origin) ->list:  # 从某个时刻开始，前面的数据全是0
    split = random.randint(180, 300)
    for i in range(0, split):
        origin[i] *= random.randint(0, 100) / 10000
    return origin


def gen_random_samples(total_num, sample_num) -> list:  # 生成一个元素不重复的随机抽样序列
    return random.sample(range(total_num), sample_num)


if __name__ == "__main__":
    # 初始化excel对象
    data = xlrd.open_workbook("./group_output.xlsx")
    print("原始文件已经打开")
    data_sheet = data.sheets()[0]
    workbook = xlsxwriter.Workbook("tag_data_output.xlsx")  # 创建输出对象
    output_sheet = workbook.add_worksheet()

    total_col_number = len(data_sheet.row_values(0)) - 2
    total_row_number = len(data_sheet.col_values(0))

    contents1 = gen_random_samples(total_row_number, int(0.2 * total_row_number / 6))
    contents2 = gen_random_samples(total_row_number, int(0.2 * total_row_number / 6))
    contents3 = gen_random_samples(total_row_number, int(0.2 * total_row_number / 6))
    contents4 = gen_random_samples(total_row_number, int(0.2 * total_row_number / 6))
    contents5 = gen_random_samples(total_row_number, int(0.2 * total_row_number / 6))
    contents6 = gen_random_samples(total_row_number, int(0.2 * total_row_number / 6))

    row = 0
    for content in contents1:
        print("1完成度：",  contents1.index(content)+1, " / ", len(contents1))
        ### 将输入的字符串列表转换为浮点数列表
        llist = data_sheet.row_values(content)[2:]
        for _ in range(len(llist)):
            llist[_] = float(llist[_])
        output = function1(llist)
        output_sheet.write(row, 0, "00" + str(row))  # 写入用户名
        output_sheet.write(row, 1, "-1")  # 写入标签 1表示正常数据 -1表示异常数据
        for i in range(336):
            output_sheet.write(row, i+2, str(output[i]))
        row += 1

    for content in contents2:
        print("2完成度：",  contents2.index(content)+1, " / ", len(contents1))
        ### 将输入的字符串列表转换为浮点数列表
        llist = data_sheet.row_values(content)[2:]
        for _ in range(len(llist)):
            llist[_] = float(llist[_])
        output = function2(llist)
        output_sheet.write(row, 0, "00" + str(row))  # 写入用户名
        output_sheet.write(row, 1, "-1")  # 写入标签 1表示正常数据 -1表示异常数据
        for i in range(336):
            output_sheet.write(row, i + 2, str(output[i]))
        row += 1

    for content in contents3:
        print("3完成度：",  contents3.index(content)+1, " / ", len(contents1))
        ### 将输入的字符串列表转换为浮点数列表
        llist = data_sheet.row_values(content)[2:]
        for _ in range(len(llist)):
            llist[_] = float(llist[_])
        output = function3(llist)
        output_sheet.write(row, 0, "00" + str(row))  # 写入用户名
        output_sheet.write(row, 1, "-1")  # 写入标签 1表示正常数据 -1表示异常数据
        for i in range(336):
            output_sheet.write(row, i + 2, str(output[i]))
        row += 1

    for content in contents4:
        print("4完成度：",  contents4.index(content)+1, " / ", len(contents1))
        ### 将输入的字符串列表转换为浮点数列表
        llist = data_sheet.row_values(content)[2:]
        for _ in range(len(llist)):
            llist[_] = float(llist[_])
        output = function4(llist)
        output_sheet.write(row, 0, "00" + str(row))  # 写入用户名
        output_sheet.write(row, 1, "-1")  # 写入标签 1表示正常数据 -1表示异常数据
        for i in range(336):
            output_sheet.write(row, i + 2, str(output[i]))
        row += 1

    for content in contents5:
        print("5完成度：",  contents5.index(content)+1, " / ", len(contents1))
        ### 将输入的字符串列表转换为浮点数列表
        llist = data_sheet.row_values(content)[2:]
        for _ in range(len(llist)):
            llist[_] = float(llist[_])
        output = function5(llist)
        output_sheet.write(row, 0, "00" + str(row))  # 写入用户名
        output_sheet.write(row, 1, "-1")  # 写入标签 1表示正常数据 -1表示异常数据
        for i in range(336):
            output_sheet.write(row, i + 2, str(output[i]))
        row += 1

    for content in contents6:
        print("6完成度：",  contents6.index(content)+1, " / ", len(contents1))
        ### 将输入的字符串列表转换为浮点数列表
        llist = data_sheet.row_values(content)[2:]
        for _ in range(len(llist)):
            llist[_] = float(llist[_])
        output = function6(llist)
        output_sheet.write(row, 0, "00" + str(row))  # 写入用户名
        output_sheet.write(row, 1, "-1")  # 写入标签 1表示正常数据 -1表示异常数据
        for i in range(336):
            output_sheet.write(row, i + 2, str(output[i]))
        row += 1


    workbook.close()


