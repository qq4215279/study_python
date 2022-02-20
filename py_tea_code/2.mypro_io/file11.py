#测试CSV文件的读取和写入
import csv

with open("dd.csv","r") as f:
    a_csv = csv.reader(f)
#    print(list(a_csv))
    for row in a_csv:
        print(row)

with open("ee.csv","w") as f:
    b_csv = csv.writer(f)
    b_csv.writerow(["ID","姓名","年龄"])
    b_csv.writerow(["1001","高淇","18"])

    c = [["1002","希希","3"],["1003","东东","4"]]
    b_csv.writerows(c)
