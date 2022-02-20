#a = ["我love u!\n","尚学堂\n","百战程序员\n"]
#b = enumerate(a)
#print(a)
#print(list(b))



with open("e.txt","r",encoding="utf-8") as f:
    lines = f.readlines()
    lines = [ line.rstrip()+" #"+str(index+1)+"\n" for index,line in enumerate(lines)]  #推导式生成列表

with open("e.txt","w",encoding="utf-8") as f:
    f.writelines(lines)