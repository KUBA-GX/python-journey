scores = [78, 92, 65, 88, 95, 71]
total = sum(scores)
count = len(scores)
print(f"平均数是：{(total / count):.2f}")
print(f"最大值是：{max(scores)}")
print(f"最小值是：{min(scores)}")

pass_count = 0
for s in scores:
    if s >= 60:
        pass_count += 1

rate = pass_count / count
print(f"及格率是：{rate * 100:.1f}%")
print(f"降序列表：{sorted(scores, reverse=True)}")

my_total = 0
my_max = scores[0]
my_min = scores[0]
for s in scores:
    my_total += s
    if s >= my_max:
        my_max = s
    if s <= my_min:
        my_min = s
print(f"手写结果：总和{my_total},最大{my_max},最小{my_min}")
print(
    "与内置函数一致：",
    my_total == total and my_max == max(scores) and my_min == min(scores),
)
