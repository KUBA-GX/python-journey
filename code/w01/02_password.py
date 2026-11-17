password = input("输入密码: ")

has_letter = False
has_digit = False
has_symbol = False

for ch in password:
    if ch.isalpha():
        has_letter = True
    elif ch.isdigit():
        has_digit = True
    else:
        has_symbol = True

if len(password) < 6:
    print("弱")
elif len(password) >= 10 and has_letter and has_symbol and has_digit:
    print("强")
elif len(password) >= 6 and has_letter and has_digit:
    print("中")
else:
    print("弱")
