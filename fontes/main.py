#Tentando fazer a modularização

import numpy as np
import pandas as pd

def verificaStopword(palavr):
    
    ##inicializando a variavel com valor diferente de 's' ou 'n'
    inn = 'k'
    
    #loop para usuário digitar ou 's' ou 'n'
    while inn != 's' and inn != 'n':
        inn = input('A palavra: ' + palavr + ' é uma stopword?(s/n): ')
    
    if(inn == 's'):
        return True
    elif(inn == 'n'):
        return False
    
def escreverEmArquivo(diretorio,frase):
    #Função que abre o arquivo no diretório do parâmetro e escreve a frase do parâmetro
    f = open(diretorio,"a+")
    f.write(frase)
    f.close()

def lerTXT(nomeArquivo):
     return np.genfromtxt(nomeArquivo + ".txt",dtype='str'); 

def zerarArquivo(nomeArquivo):
     return open(nomeArquivo + ".txt","w").close()
 
def gerar_indice_invertido(dir):
  
	df = pd.read_csv(dir+ ".txt", sep=" ", header=None)
	df.columns = ["termo", "doc", "freq"]

	indice_invertido = {}

	for t in df.termo.unique():
		rows = df[df.termo == t]

		dic = {}
		freq = {"freq": sum(rows.freq)}
		dic.update(freq)

		for d in rows.doc.unique():
			docs = rows[rows.doc == d]

			aux = { "doc"+str(d) : sum(docs.freq)}
			dic.update(aux)

		indice_invertido[t] = dic

	return indice_invertido
 
def mensagemSucesso():
    print("\n\n--------------------------------------  Pronto!  --------------------------------------------")
    print('Processo executado com sucesso!')
    print("---------------------------------------------------------------------------------------------")
 
def retirarStopWords(inn, stopwords):
    # fazendo a interseção das duas listas
    intersecao = np.intersect1d(inn,stopwords)
    
    # palavras que não estão no arquivo de stopwords
    return np.setdiff1d(inn,intersecao)

def removerGenero(not_stops, x):
    
    genero = []
    
    for p in not_stops:

        if (p[len(p)-1] == 'a'):
            print('\n'+ p + ' é uma palavra feminina?')
            res = input('Resposta(s/n): ')
            
            while res!='s' and res!='n':
                res = input('Resposta(s/n): ') 
                
            if (res == 's'):
                
                i,j = np.where(x == p)
                i = int(i[0:1])
                print (i)
                
                if (p[len(p)-2] != 'r'):
                    p = p[0:len(p)-1] + 'o'
                    
                else:
                    p = p[0:len(p)-1]
                 
                aux = x[i]
                aux[0:1] = p
                x[i] = aux
                print (x[i])
                    
        genero.append(p)
    return genero
 
def menu1():
    print('||||||||||||||||||||||||||||||||||')
    print('||                              ||')
    print('|| 1-Retirar StopWords          ||')
    print('|| 0-Sair                       ||')
    print('||||||||||||||||||||||||||||||||||')
    print('||                              ||')
    
    op = int(input('|| Opcao:'))
    return op

def menu2():
    print('||||||||||||||||||||||||||||||||||')
    print('||                              ||')
    print('|| 1-Retirar StopWords          ||')
    print('|| 2-Retirar Genero             ||')
    print('|| 3-Gerar arquivo de indice    ||')
    print('|| 4-Gerar Lista                ||')
    print('|| 5-Gerar Lista de StopWords   ||')
    print('|| 0-Sair                       ||')
    print('||||||||||||||||||||||||||||||||||')
    print('||                              ||')
    
    op = int(input('|| Opcao:'))
    return op

opcao = 10
not_stops = []
flag_Menu = 0

while opcao != 0:
    #Criando um sistema dinaminco de menu, obrigando o usuário primeiro tirar as stopwords para depois manipular as demais funções
    if flag_Menu == 0 :
        while opcao >1 :
            opcao = menu1()
        
    else:
        opcao = menu2()
    
    if opcao == 1:
        # le arquivo txt de entrada em uma matriz "x" sendo a primeira coluna as palavras, a segunda os documentos que ela ocorre e a terceira a frequência da ocorrência
        x = lerTXT("Lista01")
    
        # cria uma lista contendo a primeira coluna da matriz e retira as palavras repetidas
        palavras = np.unique(x[:,0])
        # lendo arquivo contendo stopwords achadas na internet
        stopwords = lerTXT('stopwords')
        palavras = retirarStopWords(palavras, stopwords)
        #quantidade de palavras
        tam = len(palavras)
        #contador para iterar de 10 em 10 palavras
        cnt = 0
        #Realizando supervisão com o usuário para o mesmo decidir quais palavras são e não são stopwords
        #listas de stopwords e "não-stopwords"
        stops = []
        
        while cnt != tam:
            #Criando sublista de 10 em 10 palavras para agilizar o processo
            #Pode ser que o tamanho da lista nao seja divisivel por 10 e pra isso precisamos guardar a diferença entre o contador e o tamanho
            aux = tam-cnt
                
            if (aux) >= 10:
                sub_lista = list(palavras[cnt:cnt+10])
                cnt += 10
            else:
                sub_lista = list(palavras[cnt:(cnt+aux)])
                cnt += aux
                    
            print("\nAlguma das palavras abaixo é uma stopword?\n")
            for s in sub_lista:
                print('"'+ s +'"')
            #Se uma das 10 palavras for uma stopword o programa passa uma a uma perguntando
            #Caso contrário as 10 palavras são adicionadas a lista de not_stops
    
            #inicializando com letra diferente de 's' ou 'n' para forçar usuário a digitar sim ou nao
            res = 'a'
            while res!='s' and res!='n':
                res = input('Resposta(s/n): ')
            if res == 's':
                #Verificando se todas as palavras são stopwords
                res2 = 'a'
                while res2!='s' and res2!='n':
                    res2 = input("Todas?(s/n): ")
            
                    if res2 == 's':
                        #Todas as palavras são stopwords
                        stops = stops + sub_lista
                    else:    
                        for p in sub_lista:
                            #Verificar uma a uma se é stopword
                            if(verificaStopword(p)):
                                #Se entrou aqui a palavra "p" é uma stopword
                                stops.append(p)
                            else:
                                #Se entrou aqui a palavra "p" não é uma stopword
                                not_stops.append(p)
        
            else:
                #Todas as palavras são stopwords
                not_stops = not_stops + sub_lista
        flag_Menu = 1        
        mensagemSucesso()
    elif opcao == 2:
        not_stops =  removerGenero(not_stops, x)
        mensagemSucesso()
    elif opcao == 3:
        print(gerar_indice_invertido("entrada-teste"))
        mensagemSucesso()
    elif opcao == 4:
        #zerando arquivo de saida
        zerarArquivo("Lista02")
        #Ordenando as palavras alfabeticamente
        not_stops.sort()
        for p in not_stops:
            #pegando todas as linhas da matriz "x" onde a primeira coluna é igual a "p", ou seja, pegando todas as linhas cuja a palavra é igual a palavra p
            temp = x[x[:,0] == p]
            for t in temp[:]:
                #Escrevendo linha por linha cuja primeira coluna é igual a "p"
                #t[0],t[1] e t[2] são as colunas de cada linha da matriz x, (0 é a palavra, 1 o documento e 2 a frequencia)
                escreverEmArquivo("Lista02.txt",t[0] + ' ' + t[1] + ' ' + t[2] + '\n')
        mensagemSucesso()
    elif opcao == 5:
        #Escrevendo as stopwords e não-stopwords em seus respectivos arquivos
        for p in stops:
            escreverEmArquivo("stopwords.txt",' \n' + p)
        mensagemSucesso()