import math

class ExampleClass:
    def method(self):
        return "instance method called", self

    @classmethod
    def classmethod(cls):
        return "class methdo called", cls

    @staticmethod
    def staticmethod():
        return "static methodo"

#  instance method

c = ExampleClass
c.method(1)
c.classmethod()
ExampleClass.method(c)
c.staticmethod()

#eg

class Pizza:
    def __init__(self, ingridients):
        self.ingridients = ingridients

    def __repr__(self):
        return f"Pizza({self.ingridients!r})"

Pizza(["cheese", "tomatoes"])

# Delicious Pizza Factories With @classmethod

Pizza(['mozzarella', 'tomatoes'])
Pizza(['mozzarella', 'tomatoes', 'ham', 'mushrooms'])
Pizza(['mozzarella'] * 4)

# for different kinds of pizzas

class Pizza:
    def __init__(self, ingridients):
        self.ingridients = ingridients

    def __repr__(self):
        return f"Pizza({self.ingridients!r})"

    @classmethod
    def margherita(cls):
        return cls(["mozzarella", "tomatoes"])

    @classmethod
    def prosciutto(cls):
        return cls(["mozzarella", "tomatoes", "ham"])

Pizza.margherita()
Pizza.prosciutto()

# When To Use Static Methods

class Pizza:
    def __init__(self, radius, ingridients):
        self.radius = radius
        self.ingridients = ingridients

    def __repr__(self):
        return (f"Pizza({self.radius!r}, " f"{self.ingridients!r})")

    def area(self):
        return self.circle_area(self.radius)

    @staticmethod
    def circle_area(r):
        return r**2 * math.pi

p = Pizza(4, ["mozzarella", "tomatoes"])
p
p.area()
