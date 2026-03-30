class Animal:
    def __init__(self,name:str)->None:
        self.name=name
    def speak(self)->str:
        return f"{self.name} speaks"

class Dog(Animal):
    def __init__(self,name)->None:
        super().__init__(name)
    def speak(self)->str:
        return f"{self.name} hau hau"

