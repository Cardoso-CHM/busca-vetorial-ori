import pandas as pd
import json

def gerar_indice_invertido(dir):
  
	df = pd.read_csv(dir, sep=" ", header=None)
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

def salvar_dicionario(dic, dir):

  data = json.dumps(dic)
  f = open(dir,"w")
  f.write(data)
  f.close()

def carregar_dicionario(dir):
  with open(dir, 'r') as f:
      dic = json.load(f)
      return dic
	  
url = "http://dontpad.com/ori_teste.txt"
print(gerar_indice_invertido(url))
