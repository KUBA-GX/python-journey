# 第 1 周练习题（含函数速查）

**目标**：把基础语法用一遍，练到「不看教程能写出来」。
**规则**：
1. 每题**自己跑通**再往下。
2. 卡住先自己试 **20 分钟**，再来问（带上「报错原文 + 我试过什么」）。
3. 只用标准库，不装第三方包。
4. 允许查语法，不允许让 AI 生成整段代码。
5. 文件命名 `01_temp.py` … `05_wordcount.py`，都放在 `code/w01/` 下。

---

## 通用速查（忘了就回来看这一张）

| 写法 | 作用 | 示例 | 注意 |
|---|---|---|---|
| `print(x)` | 输出 | `print("hi")` → `hi` | 多个值用逗号：`print(a, b)` |
| `input("提示")` | 读一行输入 | `name = input("名字：")` | **返回值永远是字符串** |
| `int(s)` / `float(s)` | 字符串转数字 | `float("3.5")` → `3.5` | 转不了会抛 `ValueError` |
| `len(s)` | 长度（字符个数） | `len("abc")` → `3` | 空格也算一个字符 |
| `type(x)` | 看类型 | `type(3.0)` → `<class 'float'>` | 排查“多余的 float()”时有用 |
| `f"{x:.1f}"` | 保留 1 位小数 | `f"{98.66:.1f}"` → `98.7` | 会四舍五入 |
| `s.lower()` | 转小写 | `"AbC".lower()` → `"abc"` | 返回新字符串，不改原值 |
| `s.split()` | 按空白切分 | `"a b  c".split()` → `['a','b','c']` | 连续空格会被合并 |
| `s.replace(a, b)` | 替换 | `"a,b".replace(",", " ")` → `"a b"` | 不改原字符串 |
| `x in s` | 是否包含 | `"a" in "cat"` → `True` | 对列表也能用 |
| `for ch in s:` | 逐字符遍历 | 每个字符依次进 `ch` | 不要用 `range(len(s))` |

---

## 题 1：温度换算器 ✅ 已完成

**任务**：输入摄氏温度，输出华氏温度（保留 1 位小数）；输入非数字时提示「请输入数字」而不是崩溃。
**公式**：`F = C * 9 / 5 + 32`

### 函数卡

| 写法 | 作用 | 示例 | 坑 |
|---|---|---|---|
| `input("提示")` | 读一行输入 | `c = input("温度：")` | 返回值是字符串 `"37"`，不是数字 `37` |
| `float(x)` | 转成小数 | `float("37")` → `37.0` | `float("abc")` → `ValueError` |
| `try: ... except ValueError:` | 捕获转换失败 | 见骨架 | `except` 必须配 `try`，且都缩进 4 格 |
| `f"{v:.1f}"` | 保留 1 位小数 | `f"{98.66:.1f}"` → `98.7` | 不加 `.1f` 会输出 `98.8214` |

### 骨架

```python
c_temp = input("请输入摄氏温度：")

try:
    c = float(c_temp)
    f = ...
    print(f"...")
except ValueError:
    print("请输入数字")
```

### 测试用例

| 输入 | 期望 |
|---|---|
| `37` | `37.0°C = 98.6°F` |
| `37.123` | `37.1°C = 98.8°F` |
| `abc` | `请输入数字` |
| `-40` | `-40.0°C = -40.0°F` |

---

## 题 2：密码强度检查

**任务**：输入一个密码，按下面顺序判断，**先满足哪条就是哪条**：

| 顺序 | 条件 | 结果 |
|---|---|---|
| 1 | `len(password) < 6` | 弱 |
| 2 | 长度 ≥ 10，且同时有字母、数字、符号 | 强 |
| 3 | 长度 ≥ 6，且同时有字母、数字 | 中 |
| 4 | 其它 | 弱 |

### 函数卡

| 写法 | 作用 | 示例 | 坑 |
|---|---|---|---|
| `len(s)` | 长度 | `len("abc123")` → `6` | `len("")` → `0` |
| `for ch in s:` | 逐个字符遍历 | `for ch in "ab": print(ch)` | 变量名任意，习惯用 `ch` |
| `ch.isalpha()` | 是否**全是**字母 | `"a".isalpha()` → `True` | **中文也算字母**（`"中".isalpha()` → True） |
| `ch.isdigit()` | 是否**全是**数字 | `"3".isdigit()` → `True` | 全角数字 `"３"` 也是 True |
| `ch.isalnum()` | 是否字母或数字 | `"!".isalnum()` → `False` | 空格 → `False` |
| `ch in "!@#..."` | 是否属于某个字符集合 | `"!" in "!@#"` → `True` | 比手写一堆 `or` 清爽 |
| 布尔变量 | 标记“有没有” | `has_digit = True` | 初值设 `False`，发现才置 `True` |

> 方法调用是 `ch.isalpha()`，**括号不能少**。写成 `if ch.isalpha:` 永远是 `True`（函数对象本身非空），这是最隐蔽的错误之一。

### 骨架

```python
password = input("输入密码：")

has_letter = False
has_digit = False
has_symbol = False

for ch in password:
    # 判断 ch 是哪类字符，把对应的标志位设为 True
    pass

if len(password) < 6:
    print("弱")
elif ...
```

### 测试用例

| 输入 | 期望 |
|---|---|
| `abcd` | 弱（长度不够） |
| `abc123` | 中 |
| `abcdefgh1!` | 强 |
| `12345678` | 弱（没有字母） |
| `!!!!!!!!!!` | 弱（没有字母数字） |

**思考题**：空格算符号吗？`"中".isalpha()` 返回什么？——边界想得越多，程序越不容易出错。

---

## 题 3：猜数字

**任务**：程序随机生成 1~100 的整数，玩家最多猜 7 次；每次提示「太大 / 太小」；猜中输出用了几次；7 次没中输出正确答案。

### 函数卡

| 写法 | 作用 | 示例 | 坑 |
|---|---|---|---|
| `import random` | 导入随机模块 | 写在文件最上面 | 只写一次 |
| `random.randint(a, b)` | 随机整数，**含两端** | `random.randint(1, 100)` | 每次调用都重新生成 |
| `int(s)` | 字符串转整数 | `int("50")` → `50` | `int("3.5")` 会报错，要用 `float` |
| `for i in range(1, 8):` | 循环 7 次，i = 1~7 | `range(7)` → 0~6 | `range(a, b)` 右端不包含 |
| `break` | 立即跳出循环 | 猜中时用 | 只跳出**当前**这层循环 |
| `while True:` | 无限循环 | 配 `break` 使用 | 忘写 `break` 会死循环（Ctrl+C 中断） |

### 骨架

```python
import random

answer = random.randint(1, 100)

for i in range(1, 8):
    guess = int(input(f"第 {i} 次猜："))
    if guess == answer:
        print(...)
        break
    elif guess > answer:
        print("太大了")
    else:
        print("太小了")
```

### 测试用例

无法自动测，但自测三件事：猜中能提前结束、7 次用尽会公布答案、输入 `0` 或 `101` 不崩溃（提示范围更好，但不强制）。

---

## 题 4：成绩统计

**任务**：给定 `scores = [78, 92, 65, 88, 95, 71]`，输出平均分（2 位小数）、最高分、最低分、及格率（百分比 1 位小数）、降序列表。
**要求**：平均值、最大值、最小值**各手写一遍循环**，再用内置函数验证结果一致。

### 函数卡

| 写法 | 作用 | 示例 | 坑 |
|---|---|---|---|
| `sum(lst)` | 求和 | `sum([1,2,3])` → `6` | 元素必须是数字 |
| `max(lst)` / `min(lst)` | 最大 / 最小 | `max([1,9])` → `9` | **空列表会报错** |
| `sorted(lst)` | 返回**新**排序列表 | `sorted([3,1])` → `[1,3]` | 原列表不变 |
| `sorted(lst, reverse=True)` | 降序 | `[3,1]` | 别拼成 `reverse=true` |
| `lst.sort()` | **原地**排序 | 无返回值！ | `x = lst.sort()` 会得到 `None` |
| `round(x, 2)` | 四舍五入 | `round(3.14159, 2)` → `3.14` | 优先用 f-string 格式化 |
| `len(lst)` | 元素个数 | `len([1,2])` → `2` | 不是索引最大值 |
| `f"{p:.1f}%"` | 百分比格式 | `f"{83.333:.1f}%"` → `83.3%` | 百分号写在引号内 |

> **`sorted()` 和 `.sort()` 的区别是新手必考题**：`sorted()` 有新列表，`.sort()` 原地改且返回 `None`。

### 骨架

```python
scores = [78, 92, 65, 88, 95, 71]

total = 0
for s in scores:
    total += s

average = total / len(scores)
print(f"平均分：{average:.2f}")
# 最高分、最低分改成自己写循环
# 及格率：数出 >= 60 的个数，除以总数
print(f"降序：{sorted(scores, reverse=True)}")
```

### 测试用例

手算核对：
- 总分 `489`，平均分 `81.50`
- 最高 `95`，最低 `65`
- 及格人数 `6`，及格率 `100.0%`
- 降序 `[95, 92, 88, 78, 71, 65]`

---

## 题 5：词频统计（本周大关卡）

**任务**：读一个 `.txt` 文件，统计每个单词出现次数（转小写、去标点），按次数降序输出前 10 名，并写入 `result.txt`。

### 函数卡

| 写法 | 作用 | 示例 | 坑 |
|---|---|---|---|
| `open(path, encoding="utf-8")` | 打开文件 | 见骨架 | Windows 默认编码是 GBK，**中文必须指定 utf-8** |
| `with open(...) as f:` | 自动关闭文件 | 见骨架 | 不用 `with` 就要手动 `f.close()`，忘了可能没写进磁盘 |
| `f.read()` | 读全部内容成字符串 | `text = f.read()` | 大文件别用，会吃满内存 |
| `s.lower()` | 转小写 | `"The".lower()` → `"the"` | The / the 才能合并计数 |
| `s.split()` | 按空白切成单词列表 | `"a b".split()` → `['a','b']` | 会把标点粘在单词上（`"the,"`） |
| `s.replace(",", " ")` | 去标点（笨办法） | 可以连续调用 | 先替换成空格，避免两个词粘连 |
| `d.get(k, 0)` | 取字典值，不存在给默认 | `counts.get(w, 0) + 1` | 直接用 `counts[w]` 在键不存在时**报 KeyError** |
| `d.items()` | 取出 (键, 值) 对 | `for w, c in counts.items():` | 用于排序和遍历 |
| `sorted(d.items(), key=lambda kv: kv[1], reverse=True)` | 按次数降序 | 见骨架 | `key` 函数决定按哪一列排序 |
| `f.write(s)` | 写字符串 | 不会自动换行 | 要换行自己加 `\n` |

### 骨架

```python
with open("test.txt", encoding="utf-8") as f:
    text = f.read()

text = text.lower()
for p in [",", ".", "!", "?", ";", ":", "\"", "'"]:
    text = text.replace(p, " ")

words = text.split()

counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1

top10 = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:10]

for i, (w, c) in enumerate(top10, 1):
    print(f"{i}. {w:<12} {c}")

with open("result.txt", "w", encoding="utf-8") as f:
    for w, c in top10:
        f.write(f"{w}\t{c}\n")
```

### 测试用例

自己造一个 200 词以上的英文 `test.txt`，故意让 `the` 出现 12 次、`python` 出现 8 次，验证输出顺序和计数。再放几个大写单词和带标点的词，确认合并正确。

---

## 提交方式

```powershell
git add -A
git commit -m "第1周-题N：题目名"
git push
```

> `git add -A` 会把 `w01/` 下所有改动一起加入，包括别人帮你更新的说明文档。
