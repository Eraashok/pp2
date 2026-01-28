a=int(input())
if(((a%4==0)&(a%10!=0)) or (a%400==0)):
    print("YES")
else:
    print("NO")