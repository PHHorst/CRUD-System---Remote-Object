import Pyro5
import Pyro5.client
from Pyro5 import serializers
import sys
import gameClass as gc

proxy = Pyro5.client.Proxy("PYRONAME:HORST_SPERAFICO")

try:
    proxy._pyroBind()
    print("Servidor HORST_SPERAFICO conectado com sucesso")
except:
    print("não vinculou")
    sys.exit(-1)
serializers.SerializerBase.register_dict_to_class("gc.Game", gc.game_dict_to_class)
serializers.SerializerBase.register_class_to_dict(gc.Game, gc.game_class_to_dict)


def cadastrar_jogo():
    try:
        print('Cadastre um jogo')
        nome = input('Digite o nome: ')
        tema = input('Digite o tema: ')
        genero = input('Digite o gênero: ')
        ano = int(input('Digite o ano: '))
        nota = float(input('Digite a nota: '))
        game = gc.Game(nome, tema, genero, ano, nota)
       
        
        # Chame o método create no objeto remoto do servidor
        
        if proxy.create(game):
            print('-----------------------------')
            print('-------JOGO CADASTRADO-------')
            print('-----------------------------')
    except Exception as e:
        print(f"Erro ao cadastrar jogo: {e}")



# Função para listar os jogos cadastrados
def listar_jogos():
    try:
        contador=1
        resultados= proxy.list()
        print('\n\n\n---LISTA DE JOGOS CADASTRADOS---\n\n')
        for jogo in resultados:
            print(f"JOGO {contador}:", jogo.nome.upper())
            print('--------------------------------')
            print("TEMA:", jogo.tema.upper())
            print('--------------------------------')
            print("GÊNERO:", jogo.genero.upper())
            print('--------------------------------')
            print("ANO DE LANÇAMENTO:", jogo.ano)
            print('--------------------------------')
            print("NOTA:", jogo.nota)
            print('--------------------------------\n\n\n')
            contador+= 1
    except Exception as e:
        print(f"Erro ao ler jogos: {e}")

def find_jogo():
    try:
        nome_jogo = input("Digite o nome do jogo a ser Procurado: ")
        game=gc.Game(nome_jogo)
        jogo= proxy.find(game)
        if jogo == None:
            print('-----------------------------')
            print('-----JOGO NÃO ENCONTRADO-----')
            print('-----------------------------')
        else:
            print('-----------------------------')
            print('-------JOGO ENCONTRADO-------')
            print('-----------------------------')

            print("NOME:", jogo.nome.upper())
            print('-----------------------------')
            print("TEMA:", jogo.tema.upper())
            print('-----------------------------')
            print("GÊNERO:", jogo.genero.upper())
            print('-----------------------------')
            print("ANO DE LANÇAMENTO:", jogo.ano)
            print('-----------------------------')
            print("NOTA:", jogo.nota)
            print('-----------------------------')

    except Exception as e:
        print(f"Erro ao procurar jogo: {e}")

# Função para atualizar um jogo
def atualizar_jogo( ):
    try:
        nome_jogo = input("Digite o nome do jogo a ser atualizado: ")
        nome = input('Digite o novo nome: ')
        tema = input('Digite o novo tema: ')
        genero = input('Digite o novo gênero: ')
        ano = int(input('Digite o novo ano: '))
        nota = float(input('Digite a nova nota: '))
        game = gc.Game(nome,tema,genero,ano,nota)
        if proxy.update(nome_jogo,game):
            print('-----------------------------')            
            print("O JOGO:", nome_jogo.upper(),'FOI ATUALIZADO PARA:')
            print('-----------------------------')            
            print("NOVO NOME:", nome.upper())
            print('-----------------------------')
            print("NOVO TEMA:", tema.upper())
            print('-----------------------------')
            print("NOVO GÊNERO:", genero.upper())
            print('-----------------------------')
            print("NOVO ANO DE LANÇAMENTO:", ano)
            print('-----------------------------')
            print("NOVA NOTA:", nota)
            print('-----------------------------')
    except Exception as e:
        print(f"Erro ao atualizar jogo: {e}")

# Função para excluir um jogo
def excluir_jogo( ):
    try:
        nome_jogo = input("Digite o nome do jogo a ser excluído: ")
        game=gc.Game(nome_jogo)
        jogo =proxy.delete(game)
        if jogo == None:
            print('-----------------------------')
            print('-----JOGO NÃO ENCONTRADO-----')
            print('-----------------------------')
        else:
            print('-----------------------------')
            print('--------JOGO DELETADO--------')
            print('-----------------------------')
            print()
            print("NOME:", jogo.nome.upper())
            print('-----------------------------')
            print("TEMA:", jogo.tema.upper())
            print('-----------------------------')
            print("GÊNERO:", jogo.genero.upper())
            print('-----------------------------')
            print("ANO DE LANÇAMENTO:", jogo.ano)
            print('-----------------------------')
            print("NOTA:", jogo.nota)
            print('-----------------------------')



    except Exception as e:
        print(f"Erro ao excluir jogo: {e}")

def exportar_jogos():
    try:
        with open('GamesDB.txt', "w") as arquivo:
            contador = 0
            jogos= proxy.list()
            arquivo.write('\n\n\n---LISTA DE JOGOS CADASTRADOS---\n\n\n')
            for jogo in jogos:
                contador += 1
                arquivo.write("################################\n")
                arquivo.write(f"JOGO {contador}: {jogo.nome.upper()}\n")
                arquivo.write('--------------------------------\n')
                arquivo.write(f"TEMA: {jogo.tema.upper()}\n")
                arquivo.write('--------------------------------\n')
                arquivo.write(f"GÊNERO: {jogo.genero.upper()}\n")
                arquivo.write('--------------------------------\n')
                arquivo.write(f"ANO DE LANÇAMENTO: {jogo.ano}\n")
                arquivo.write('--------------------------------\n')
                arquivo.write(f"NOTA: {jogo.nota}\n")
                arquivo.write('--------------------------------\n\n\n')
        print(f"Base de jogos exportada com sucesso para '{'GamesDB.txt'}'.")
    except Exception as e:
        print(f"Erro ao exportar a base de jogos': {e}")

# Função para sair do programa
def sair():
    
    print("Saindo do programa...")
    exit()

# Função principal
def main():

    options = {
        'create': cadastrar_jogo,
        'list': listar_jogos,
        'find': find_jogo,
        'update': atualizar_jogo,
        'delete': excluir_jogo,
        'export':exportar_jogos,
        'sair': sair
    }

    while True:
        print("\nOpções disponíveis: create, find, list, update, delete, export, sair")
        opcao = input("Escolha uma opção: ").lower()

        if opcao in options:
            options[opcao]()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
