class Weight:
    def __init__(self,kg:float)->None:
        self.kg=kg
    def __add__(self,other:float)->float :
        return self.kg + other.kg
    def __sub__(self,other:float)->float:
        return self.kg - other.kg
