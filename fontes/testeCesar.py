import pandas as pd
import numpy as np
import json
import math

def gerar_dict_documentos_pdf(dir_docs_pdfs):
    import PyPDF2
    import glob 
    
    pdfs = glob.glob(dir_docs_pdfs)
    docs = {}
    for file in pdfs:
        #Fazendo um if para apenas arquivos .pdf
        if file.endswith('.pdf'):
            filename = file.split("\\")[-1]
            filename = filename.split(".pdf")[0]
            #Lendo os arquivos
            fileReader = PyPDF2.PdfFileReader(open(file, "rb"))
            #Declarando variavel igual a 0
            count = 0
            #Lendo a quantidade de páginas de todos PDF
            count = fileReader.numPages
            #Criando vetor para armazenar palavras do pdf
            palavras = []
            #Fazendo um while enquanto tiver arquivo PDF para ler
            while count >= 1:
                count -= 1
                #Recebendo a leitura de todas páginas dos pdfs
                pageObj = fileReader.getPage(count)
                #Extraindo todos os textos e salvando na váriavel text
                text = pageObj.extractText()
                palavras.append(text.replace("\n", ""))
            docs[filename] = palavras
    return docs

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
        docs = dict_indice["#docs"]
        qtde_total_docs = len(docs)
        del dict_indice["#docs"] # retirando indice auxiliar para não causar problemas nas seguintes iteraçÕes:
        
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
    return False;

def pesquisar_idf_tf_doc(idf_tf, docs, doc):
    if(doc in docs):
        return idf_tf[:,docs[doc]]
    return False;

#MAIN

url = "http://dontpad.com/ori_teste.txt"

x = gerar_indice_invertido(url)

# DURANTE A GERAÇÃO DO INDICE, É COLOCADO UM ÍNDICE CHAMADO "#docs" PARA FACILITAR A OBTENÇÃO DE TODOS OS DOCS UTILIZADOS
# DURANTE A EXECUÇAO DA FUNÇÃO "gerar_IDF_TF_de_Dicionario_Invertido", ESTE ÍNDICE "#docs" É RETIRADO DO DICIONÁRIO !
docs = { doc: int(doc.split('doc')[1]) for doc in x["#docs"] }
        
y = gerar_IDF_TF_de_Dicionario_Invertido(x)
