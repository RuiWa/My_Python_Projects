#汉诺塔游戏，hanoi(a,b,c,n)表示：a借助b向c移n个盘子
def hanoi(a,b,c,n):
    if n == 1:
        print(a,'->',c)
    else:
        hanoi(a,c,b,n-1)
        print(a,'->',c)
        hanoi(b,a,c,n-1)
hanoi('a','b','c',3)


#斐波那契数列
def fib(n):
    if n == 0 or n == 1:
        return n
    else:
        return fib(n-1) + fib(n-2)

#numB = 2时：函数为求一个数的二进制
def foo(num,base):
    if(num >= base):
      foo(num // base, base)
    print(num % base, end = ' ')
      
numA = int(input())
numB = int(input())
foo(numA,numB)
