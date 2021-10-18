#class override
class A:
    def __init__(self):
        self.multiply(15)
        print(self.i)

    def multiply(self, i):
        self.i = 4 * i;


class B(A):
    def __init__(self):
      super().__init__()

    def multiply(self, i):
        self.i = 2 * i;


obj = B()


#class override
class A:
    def __init__(self):
        self.multiply(15)

    def multiply(self, i):
        self.i = 4 * i;


class B(A):
    def __init__(self):
        super().__init__()
        print(self.i)

    def multiply(self, i):
        self.i = 2 * i;
obj = B()

# example of class

class Demo:
    def check(self):
        return " Demo's check "
    def display(self):
        print(self.check())
class Demo_Derived(Demo):
    def __check(self):
        return " Derived's check "
Demo().display()
Demo_Derived().display()


#class function and object.
class demo1:
    a='nitin'
    def function_one(self):
        print('this is msg inside class')
obj1=demo1()
obj2=demo1()
obj2.a='nisn'
print(obj1.a)
print(obj2.a)

class vechile:
    name=''
    kind=''
    color=''
    value=1

    def description(self):
        desc_str="%s is a %s %s worth $%.2f."%(self.name,self.color,self.kind,self.value)
        print(desc_str)

car=vechile()
car.name='fer'
car.color='red'
car.kind=''
car.value=2000.4567

print(car.description())


#multiple inheritance

class a(object):
    def __init__(self):
        self.str1='hello'
        print('a')

class b(object):
    def __init__(self):
        self.str2='python'
        print('b')

class derived(a,b):
    def __init__(self):
        a.__init__(self)
        b.__init__(self)
        print("derived")

    def printstring(self):
        print(self.str1,self.str2)


ob=derived()
ob.printstring()


# multi level inheritance

class a:
    def __init__(self):
        self.n="pythonn"

class b(a):
    def __init__(self):
        self.a=2021


class d(b):
    def __init__(self):
        a.__init__(self)
        b.__init__(self)
        print(self.n,self.a)

obj=d()



class practice:
    x=5
    def display(self,x):
        x=30
        print(x)
        print(self.x)
ob=practice()
ob.display(12)

i=0
while i<10:
    print(i)
    i += 1

for x in range(6,1,-1):
    print(x)

string = "my name is x"
for i in string:
        print(i, end=", ")



print("hello")