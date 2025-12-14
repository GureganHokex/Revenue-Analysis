class Person:
    def __init__(self,name,age):
        self.name = name #Атрибуту self.name присваеваем переменную name
        self.age = age
    def display_info(self):
        print(f'Name: {self.name} & Age: {self.age}')
    def __del__(self):
        print(f'Удалить {self.age},{self.name}')
    # def say_hello(self):
    #     print('Hello!')
tob = Person('tob',23)
tob.display_info()
# print(tob.age)
# tob.say_hello()