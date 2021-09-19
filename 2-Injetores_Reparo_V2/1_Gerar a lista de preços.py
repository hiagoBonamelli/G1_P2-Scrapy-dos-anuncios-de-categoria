import pandas as pd

lista_preco = []
for i in range(1, 300):
    lista_preco.append(str(i))
    
df_lista_precos = pd.DataFrame({'precos':lista_preco, "status": "FAZER"})
df_lista_precos.to_csv("1_df_lista_precos.csv")