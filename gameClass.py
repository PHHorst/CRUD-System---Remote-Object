class Game():
    def __init__(self, nome,tema='',genero='',ano=0,nota=0):
        self.nome= nome
        self.tema= tema
        self.genero= genero
        self.ano= ano
        self.nota= nota

def game_class_to_dict(obj):
	gameDict = {
		"__class__": "gc.Game",
		"nome":obj.nome,
		"tema":obj.tema,
		"genero":obj.genero,
		"ano":obj.ano,
		"nota":obj.nota,
	}
	return gameDict 

def game_dict_to_class(classname,dic):
	a = Game(dic["nome"], dic["tema"], dic["genero"], dic["ano"], dic["nota"])
	return a