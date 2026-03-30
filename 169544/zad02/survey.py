class Survey:

    def __init__(self,title:str,*questions:list,anonymous:bool=True)->None:
        self.title=title
        self.questions=questions
        self.anonymous=anonymous
        lista = ['pytanie 1', 'pytanie 2', 'pytanie 3']
