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
        docs = dict_indice_invertido["#docs"]
        qtde_total_docs = len(docs)
        del dict_indice_invertido["#docs"] # retirando indice auxiliar para não causar problemas nas seguintes iteraçÕes:
        
        for termo in dict_indice:
            
            aux = []
            for doc in docs:
                
                if(doc in dict_indice[termo]["docs"]):
                    aux.append(calcTF(dict_indice[termo]["docs"][doc]))
                else:
                    aux.append(0)
                    
            tf.append(aux)
            idf.append(calcIDF(qtde_total_docs, len(dict_indice[termo]["docs"])) )
        
        idf = np.array([idf])
        #print(len(idf))
        #print(type(idf))
        retornando_idf = idf.transpose()
        tf = np.array(tf)
        #print(len(tf))
        #print(type(tf))
        
        #coluna 0 representa o idf dos termos de busca do usuário
        #como ainda nao existe a string de busca a coluna somente terá zeros
        m = np.insert(np.multiply(idf.T,tf), 0, 0, axis=1)
        m[0:,0:1] = retornando_idf
        return m
    except Exception as e:
        print("Exeção na função gerar_IDF_TF: " + e)

def pesquisar_idf_tf_termo(idf_tf, indice_invertido, termo):
  keys = list(indice_invertido.keys()) 
  if(termo in keys):
    return idf_tf[ keys.index(termo) ]
  else:
    return [];

def pesquisar_idf_tf_doc(idf_tf, docs, doc):
  if(doc in docs):
    return idf_tf[:,docs[doc]]
  else:
    return [];

def buscar_termos(frase,x,y,qtd_docs):
    idf_tf = []
    qtd_termos = 0
    
    f = frase.split()
    
    for p in f:
        k = (pesquisar_idf_tf_termo(y,x,p))
        
        if(len(k) > 0 ):
            qtd_termos += 1
            idf_tf.append(k)
            
    if(qtd_termos == 0):
        return ('Nenhum termo encontrado!')
    else:
        return ranquear(idf_tf,qtd_termos,qtd_docs,f,x,y)

def ranquear(r, qtd, qtd_docs,frase,x,y):
    i = 0
    j = 0
    div = 0
    teste = 0
    vetor_busca = [0.0]*qtd
    docs = []
    
    
    '''
    #criando matriz para receber valores dos documentos
    for k in range(qtd_docs):
        docs.append(vetor_busca)
    '''
        
    #calculo do valor de divisao do valor de busca
    for k in r:
        div += r[i][0]**2
        i += 1
    div = div**(0.5)
    
    #iteração nas colunas do vetor de busca e atribuindo valor de idf/div
    for vb in vetor_busca:
        print(r[j][0],div)
        vetor_busca[teste] = r[j][0]/div
        j += 1
        teste += 1
          
    docs = montar_vetores_distancia(x,frase,y,qtd_docs)
    
    cont2 = 0
    for k in docs:
        cont = 0
        for t in k:
            docs[cont2][cont] = t*vetor_busca[cont]
            cont+=1
        cont2 +=1
    
    ranking = []
    
    for k in docs:
        ranking.append(sum(k))
    
    dc =  np.zeros((qtd_docs,2))
        
    cont = 0
    cont2 = 0
    with np.nditer(dc, op_flags=['readwrite']) as it:
        for i in it:
            if(cont%2 ==0):
                i[...] = ranking[cont2]
                cont2+=1
            else:
                i[...] = cont2
            cont += 1
              
    rk = dc[dc[:,0].argsort()][::-1] 
    rk1 = rk[:,1]
    
    for v in rk1:
        print('Documento: ', int(v))
        
def montar_vetor_busca(dict, lista, lista2):
    keys=list(dict.keys()) #in python 3, you'll need `list(i.keys())`
    numerador = []
    denominador = 0
    for termo in lista:
        if(termo in keys):
            numerador.append(lista2[keys.index(termo), 0])
            denominador = denominador + math.pow(lista2[keys.index(termo), 0],2)
    for valor in numerador:
        denominador=math.sqrt(denominador)
        numerador[numerador.index(valor)] = float(numerador[numerador.index(valor)])/float(denominador)
        #numerador.index(valor) = numerador[valor]/denominador
    return numerador

def montar_vetores_distancia(dict, lista, lista2,qtd_docs):
    
    vd = []
    for coluna, k in enumerate(range(qtd_docs)):
        keys=list(dict.keys())
        i=coluna+1
        numerador = []
        denominador = 0
        while i< coluna+2 :
            for termo in lista:
                if(termo in keys) :
                    numerador.append(lista2[keys.index(termo), coluna+1])
                    denominador = denominador + math.pow(lista2[keys.index(termo), coluna+1],2)
                    
            denominador=math.sqrt(denominador)
            for valor in numerador:
                if(denominador ==0.0) :
                    numerador[numerador.index(valor)] = 0;
                else :
                    numerador[numerador.index(valor)] = float(numerador[numerador.index(valor)])/float(denominador)
            
            i+=1
        
        vd.append(numerador)
    
    return vd

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

def mensagemSucesso():
    print("\n\n--------------------------------------  Pronto!  --------------------------------------------")
    print('Processo executado com sucesso!')
    print("---------------------------------------------------------------------------------------------\n\n")
 

def menu():
    print('||||||||||||||||||||||||||||||||||')
    print('||                              ||')
    print('|| 1-Retirar StopWords          ||')
    print('|| 2-Retirar Genero             ||')
    print('|| 3-Gerar Lista                ||')
    print('|| 4-Gerar Lista de StopWords   ||')
    print('|| 5-Realizar Busca Vetorial    ||')
    print('|| 0-Sair                       ||')
    print('||                              ||')
    print('||||||||||||||||||||||||||||||||||')
    print('||                              ||')
    
    op = int(input('|| Opcao:'))
    return op


#MAIN - INICIO DA EXECUÇÃO DO PROGRAMA
    
opcao = -1
not_stops = []
entrada = lerTXT("Lista01") # lendo arquivo de entrada
stopwords = lerTXT('stopwords') # lendo arquivo contendo stopwords achadas na internet

while opcao != 0:
    #Criando um sistema dinaminco de menu, obrigando o usuário primeiro tirar as stopwords para depois manipular as demais funções
    opcao = menu()
    
    if opcao == 1:
        # le arquivo txt de entrada em uma matriz "x" sendo a primeira coluna as palavras, a segunda os documentos que ela ocorre e a terceira a frequência da ocorrência
    
        # cria uma lista contendo a primeira coluna da matriz e retira as palavras repetidas
        palavras = np.unique(entrada[:,0])

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
        not_stops =  alterarGenero(not_stops, entrada)
        mensagemSucesso()
        
    elif opcao == 3:
        #zerando arquivo de saida
        zerarArquivo("Lista02")
        #Ordenando as palavras alfabeticamente
        not_stops.sort()
        for p in not_stops:
            #pegando todas as linhas da matriz "x" onde a primeira coluna é igual a "p", ou seja, pegando todas as linhas cuja a palavra é igual a palavra p
            temp = entrada[entrada[:,0] == p]
            for t in temp[:]:
                #Escrevendo linha por linha cuja primeira coluna é igual a "p"
                #t[0],t[1] e t[2] são as colunas de cada linha da matriz x, (0 é a palavra, 1 o documento e 2 a frequencia)
                escreverEmArquivo("Lista02.txt",t[0] + ' ' + t[1] + ' ' + t[2] + '\n')
        mensagemSucesso()
        
    elif opcao == 4:
        #Escrevendo as stopwords e não-stopwords em seus respectivos arquivos
        for p in stops:
            escreverEmArquivo("stopwords.txt",' \n' + p)
        mensagemSucesso()
    
    elif opcao == 5:
        frase = input('Digite os termos que deseja pesquisar: ')
        dict_indice_invertido = gerar_indice_invertido("./Lista02.txt")
        docs = { doc: int(doc.split('doc')[1]) for doc in dict_indice_invertido["#docs"] }
        qtd_docs = len(docs)
        
        matriz_idf_tf = gerar_IDF_TF_de_Dicionario_Invertido(dict_indice_invertido)
        
        buscar_termos(frase, dict_indice_invertido,matriz_idf_tf, qtd_docs)
    
    elif opcao != 0:
        print("|| Opção inválida!\n")

print("|| Programa finalizado!")