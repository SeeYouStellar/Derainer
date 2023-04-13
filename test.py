from time import strftime, localtime
print(strftime('%Y-%m-%d %H:%M:%S',localtime()))

a = 0

def func():
    global a
    a = 2
    print("func:"+str(a))
    if a == 2:
        a = 4

print(a)
func()
print(a)