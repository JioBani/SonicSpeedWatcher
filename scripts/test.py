class Person:

  def __init__(self, _name):
    self.name = _name

  def PrintName(self):
    print(self.name)

  def Print(self):
    self.PrintName()

person = Person("gd")
person.Print()