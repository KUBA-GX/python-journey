# 第 1 周 · 题 1：温度换算器

c_temp = input("请输入摄氏温度：")

try:
    c = float(c_temp)
    f = c * 9 / 5 + 32
    print(f"{c:.1f}°C = {f:.1f}°F")
except ValueError:
    print("请输入数字")
