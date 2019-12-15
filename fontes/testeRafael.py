import pandas as pd
import numpy as np
import json
import math

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

def salvar_dicionario(dic, dir):

  data = json.dumps(dic)
  f = open(dir,"w")
  f.write(data)
  f.close()

def carregar_dicionario(dir):
  with open(dir, 'r') as f:
      dic = json.load(f)
      return dic
  
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
    a = idf_tf[ keys.index(termo) ]
    lista = []
    for k in a:
        lista.append(k)
    return lista
  else:
    return False;

def pesquisar_idf_tf_doc(idf_tf, docs, doc):
  if(doc in docs):
    return idf_tf[:,docs[doc]]
  else:
    return False;

def buscar_termos(frase,x,y,qtd_docs):
    idf_tf = []
    qtd_termos = 0

    
    f = frase.split()
    for p in f:
        k = (pesquisar_idf_tf_termo(y,x,p))
        
        if(k != False):
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

#MAIN
url = "http://dontpad.com/ori_teste.txt"

x = gerar_indice_invertido(url)

# DURANTE A GERAÇÃO DO INDICE, É COLOCADO UM ÍNDICE CHAMADO "#docs" PARA FACILITAR A OBTENÇÃO DE TODOS OS DOCS UTILIZADOS
# DURANTE A EXECUÇAO DA FUNÇÃO "gerar_IDF_TF_de_Dicionario_Invertido", ESTE ÍNDICE "#docs" É RETIRADO DO DICIONÁRIO !
docs = { doc: int(doc.split('doc')[1]) for doc in x["#docs"] }
        
y = gerar_IDF_TF_de_Dicionario_Invertido(x)

qtd_docs = len(docs)
frase = input('Digite os termos que deseja pesquisar: ')
print('')
print('')
buscar_termos(frase,x, y, qtd_docs)

