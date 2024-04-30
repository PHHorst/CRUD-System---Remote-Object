import Pyro5
import Pyro5.core
from Pyro5 import serializers
import Pyro5.server
import mysql.connector 
import gameClass as gc

meubd = mysql.connector.connect(
    host='localhost',
    user='root',
    password='******',
    database='GAME'
)

cursor = meubd.cursor()

@Pyro5.server.expose
class operacao:
    def create(self,game):
        
        print(game.nome,game.tema,game.genero,game.ano,game.nota)
        comando_insert = 'INSERT INTO atributos (nome, tema, genero, ano, nota) VALUES (%s, %s, %s, %s, %s)'
        valores = (game.nome, game.tema, game.genero, game.ano, game.nota)
        cursor.execute(comando_insert, valores)
        meubd.commit()

        print("Jogo cadastrado com sucesso.")
        return True

    def list(self):
            comando_select = 'SELECT * FROM atributos'
            cursor.execute(comando_select)
            resultados = cursor.fetchall()
            jogos = []
            
            for resultado in resultados:
                jogo = gc.Game(nome=resultado[0], tema=resultado[1], genero=resultado[2], ano=resultado[3], nota=resultado[4])
                jogos.append(jogo)
            print('Jogos listados com sucesso')
            return jogos
        
    def find(self,game):
        comando_select = 'SELECT * FROM atributos WHERE nome = %s'
        cursor.execute(comando_select, (game.nome,))
        resultado= cursor.fetchone()
        if resultado== None:
            print('Jogo não foi encontrado')
            return None
        else:
            jogo = gc.Game(resultado[0],resultado[1],resultado[2],resultado[3],resultado[4])
            print('Jogo encontrado com sucesso')
            return jogo

    
    def update(self, nome,game):

        # Lista de campos disponíveis para atualização
        campos = ['nome', 'tema', 'genero', 'ano', 'nota']
        valores=[game.nome,game.tema,game.genero,game.ano,game.nota]
        # Gera a parte SET do comando UPDATE
        set_clause = ", ".join([f"{campo} = %s" for campo in campos])

        # Monta o comando UPDATE
        comando_update = f'UPDATE atributos SET {set_clause} WHERE nome = %s'  # Assumindo que a chave primária é "id"

        # Executa o comando UPDATE com os valores recebidos e o nome do jogo
        cursor.execute(comando_update, [*valores, nome])
        meubd.commit()
        print("Jogo atualizado com sucesso.")
        return True

    def delete(self, game):
        comando_select = 'SELECT * FROM atributos WHERE nome = %s'
        cursor.execute(comando_select, (game.nome,))
        resultado= cursor.fetchone()
        print(resultado)
        if resultado== None:
            print('Jogo não foi encontrado')
            return None
        else:
            jogo = gc.Game(resultado[0],resultado[1],resultado[2],resultado[3],resultado[4])
            comando_delete = 'DELETE FROM atributos WHERE nome = %s'  # Usando o nome como critério
            cursor.execute(comando_delete, (game.nome,))
            meubd.commit()
            print('Jogo deletado com sucesso')
            return jogo


def main():
    o = operacao()
    servidor = Pyro5.server.Daemon()
    serializers.SerializerBase.register_dict_to_class("gc.Game", gc.game_dict_to_class)
    serializers.SerializerBase.register_class_to_dict(gc.Game, gc.game_class_to_dict)
    URI = servidor.register(o)
    #print("endereço do objeto: ", URI)
    server="HORST_SPERAFICO"
    dns = Pyro5.core.locate_ns()
    dns.register(server, URI)
    print(f'Servidor {server} conectado com sucesso')
    servidor.requestLoop()

if __name__=="__main__": main()

#cursor.close()
#meubd.close()

