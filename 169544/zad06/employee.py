class Employee:
    def __init__(self,name:str,salary:float)->None:
        self.name=name
        self.salary=salary
    def get_bonus(self)->float:
        return self.salary*0.1

class Manager(Employee):
    def __init__(self,name:str,salary:float)->None:
        super().__init__(name,salary)
    def get_bonus(self)->float:
        return self.salary *0.2

