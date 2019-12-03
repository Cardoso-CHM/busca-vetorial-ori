#Tentando fazer a modularização

import numpy as np
import pandas as pd
import math

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
    nomeArquivo = './'+ nomeArquivo + '.txt'
    return np.genfromtxt(nomeArquivo,dtype='str'); 

def zerarArquivo(nomeArquivo):
     return open(nomeArquivo + ".txt","w").close()
 
def gerar_indice_invertido(dir):
  
    df = pd.read_csv(dir, sep=" ", header=None)
    df.columns = ["termo", "doc", "freq"]

    indice_invertido = {}
    total_docs = []
    for t in df.termo.unique():
        rows = df[df.termo == t]

        dic = {}
        dic_docs = {}
        
        for d in rows.doc.unique():
            docs = rows[rows.doc == d]
            doc_name = "doc"+str(d)
            dic_docs[doc_name] = sum(docs.freq)
            if doc_name not in total_docs:
                total_docs.append(doc_name)
        
        dic["freq"] = sum(rows.freq)
        dic["docs"] = dic_docs
        
        indice_invertido[t] = dic
    
    indice_invertido["#docs"] = sorted(total_docs)
    return indice_invertido

def calcIDF(n_docs, qtd_post):
    return math.log10( n_docs/qtd_post )

def calcTF(freq):
    if(freq == 0):
        return 0
    
    return 1 + math.log10( freq )

def gerar_IDF_TF_de_Dicionario_Invertido(dict_indice):
    try:
        idf = []
        tf = []
        
        #Na funcao gerarIndiceInvertido é colocado uma chave com o nome "#docs" contendo uma lista
        # com todos os documentos - para facilitar as operações a seguir
        docs = x["#docs"]
        qtde_total_docs = len(docs)
        del x["#docs"] # retirando indice auxiliar para não causar problemas nas seguintes iteraçÕes:
        
        for termo in dict_indice:
            aux = []
            for doc in docs:
                
                if(doc in dict_indice[termo]["docs"]):
                    aux.append(calcTF(dict_indice[termo]["docs"][doc]))
                else:
                    aux.append(0)
            tf.append(aux)
            idf.append(calcIDF(qtde_total_docs, len(dict_indice[termo]["docs"])))
        
        idf = np.array([idf])
        tf = np.array(tf)
        
        #coluna 0 representa o idf dos termos de busca do usuário
        #como ainda nao existe a string de busca a coluna somente terá zeros
        return np.insert(np.multiply(idf.T,tf), 0, 0, axis=1)
    except Exception as e:
        print("Exeção na função gerar_IDF_TF: " + e)

def pesquisar_idf_tf_termo(idf_tf, indice_invertido, termo):
  keys = list(indice_invertido.keys()) 
  if(termo in keys):
    return idf_tf[ keys.index(termo) ]
  else:
    return False;

def pesquisar_idf_tf_doc(idf_tf, docs, doc):
  if(doc in docs):
    return idf_tf[:,docs[doc]]
  else:
    return False;

def mensagemSucesso():
    print("\n\n--------------------------------------  Pronto!  --------------------------------------------")
    print('Processo executado com sucesso!')
    print("---------------------------------------------------------------------------------------------")
 
def retirarStopWords(inn, stopwords):
    # fazendo a interseção das duas listas
    intersecao = np.intersect1d(inn,stopwords)
    
    # palavras que não estão no arquivo de stopwords
    return np.setdiff1d(inn,intersecao)

def alterarGenero(not_stops, x):
    
    genero = []
    
    for p in not_stops:

        if (p[len(p)-1] == 'a'):
            print('\n'+ p + ' é uma palavra feminina?')
            res = input('Resposta(s/n): ')
            
            while res!='s' and res!='n':
                res = input('Resposta(s/n): ') 
                
            if (res == 's'):
                
                i,j = np.where(x == p) #guarda em 'i' os indices da palavra encontrada 
                
                if (p[len(p)-2] != 'r'):
                    p = p[0:len(p)-1] + 'o'
                    
                else:
                    p = p[0:len(p)-1]
                    
                for indice in np.nditer(i): #percorre as posicoes em que encontrei a palavra
                    aux = x[indice]#Ex: aux = [pequena, 1 ,2]
                    aux[0:1] = p #atribuindo genero a palavra = [pequeno]
                    x[indice] = aux #alteração da palavra realizada em x, mantendo os docs [pequeno, 1 ,2]
                    
        genero.append(p)
    return genero
 
    
def menu():
    print('|| Escolha uma opção |||||||||||||')
    print('||                              ||')
    print('|| 1-Retirar StopWords          ||')
    print('|| 0-Sair                       ||')
    print('||||||||||||||||||||||||||||||||||')
    print('||                              ||')
    
    op = int(input('|| Opcao:'))
    return op

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
        not_stops =  alterarGenero(not_stops, x)
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
