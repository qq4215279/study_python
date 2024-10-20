# encoding: utf-8


line = "  map<string, string> map = 1;"


def parseMapLine(line: str) -> (str, str, str):
    pre = line.split("=")[0].strip()
    print("pre: ", pre) #   map<string, string> map
    str1 = pre.split("map<")[1]
    print(str1)
    arr = str1.split(">")
    print("arr: ", arr)
    kv_str = arr[0]
    kv = parse_kv_str(kv_str)
    print("kv: ", kv)

    field_name = arr[1].strip()
    print("field_name:", field_name)
    return field_name, kv[0], kv[1]

#
def parse_kv_str(kv_str: str) -> (str, str):
    arr = kv_str.split(",")
    return arr[0].strip(), arr[1].strip()


res = parseMapLine(line)
print("res: ", res)

print("------------>")
def re():
    str = "  /** 响应游戏桌子信息 */\n"
    res = str.replace("\n", "").replace(" ", "").replace("//", "").replace(
    "/**", "").replace("/*", "").replace(
      "*/", "")
    print(res)

re()

