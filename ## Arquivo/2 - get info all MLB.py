#!/usr/bin/env python
# coding: utf-8

# # Get info dos anuncios do vendedor 1.0

# In[1]:


import pandas as pd
import numpy as np


# In[ ]:





# In[2]:


df = pd.read_csv('./mlb 37.csv')


# In[ ]:





# In[68]:


#testes
marca = response[0]['body']['attributes'][0]['name']
print('marca:',marca)
modelo = response[0]['body']['attributes'][4]['name']
print('modelo:', modelo)
qntd_velas = response[0]['body']['attributes'][0]['name']
print('qntd de velas:', qntd_velas)
numero_peca = response[0]['body']['attributes'][5]['name']
print('nmr de peça:', numero_peca)
sku = response[0]['body']['attributes'][6]['name']
print('sku:',sku)
link = response[0]['body']['permalink']
print('link:',link)


# In[ ]:





# In[7]:


import requests
import json
import os
import pandas as pd
from time import sleep

guarda_info = []
cont = 0
for i, row in df.iterrows():
    cont += 1
    print(cont)
    url = "https://api.mercadolibre.com/items?ids="+ row['anuncios']

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    #json_data = json.loads(response.text)

    response = response.json()

    try:
        titulo = response[0]['body']['title']#title 5
    #print(titulo)
    except:
        titulo = 'nao tem'

    try:
        preco = response[0]['body']['price']#title 5
        #print(preco)
    except:
        preco = 'nao tem'

    try:
        base_preco = response[0]['body']['base_price']
    except:
        base_preco = 'nao tem'

    try:
        link = response[0]['body']['permalink']#title 5
        #print(link)
    except:
        link = 'nao tem'

    try:
        seller_id = response[0]['body']['seller_id']
    except:
        seller_id = 'nao tem'

    try:
        category_id = response[0]['body']['category_id']
    except:
        category_id = 'nao tem'

    try:
        available_quantity = response[0]['body']['available_quantity']
    except:
        available_quantity = 'nao tem'

    try:
        sold_quantity = response[0]['body']['sold_quantity']
    except:
        sold_quantity = 'nao tem'

    try:
        listing_type_id = response[0]['body']['listing_type_id']       
    except:
        listing_type_id = 'nao tem'

    try:
        tempo = response[0]['body']['start_time']       
    except:
        tempo = 'nao tem'

    try:
        condition = response[0]['body']['condition'] 
    except:
        condition = 'nao tem'

    try:
        quality_picture = response[0]['body']['tags'][0]

    except:
        quality_picture = 'nao tem'

    try:
        payment = response[0]['body']['tags'][1]

    except:
        payment = 'nao tem'

    try:
        cart_eligible = response[0]['body']['tags'][3]

    except:
        cart_eligible = 'nao tem'






    try:
        try:
            try:
                try:
                    try:
                        marca = response[0]['body']['attributes'][0]['name']#title 5
                        if marca == 'Marca':
                            marca1 = response[0]['body']['attributes'][0]['value_name']#title 5
                            #print(marca1)
                        else:
                            sys.exit()
                    except:
                        marca = response[0]['body']['attributes'][1]['name']#title 4
                        if marca == 'Marca':
                            marca1 = response[0]['body']['attributes'][1]['value_name']#title 4
                            #print(marca1)
                        else:
                            sys.exit()
                except:
                    marca = response[0]['body']['attributes'][0]['name']#title 3
                    if marca == 'Marca':
                        marca1 = response[0]['body']['attributes'][0]['value_name']#title 3
                        #print(marca1)
                    else:
                        sys.exit()
            except:
                marca = response[0]['body']['attributes'][0]['name']
                if marca == 'Marca':
                    marca1 = response[0]['body']['attributes'][0]['value_name']
                    #print(marca1)
                else:
                    sys.exit()
        except:
            marca = response[0]['body']['attributes'][0]['name']
            if marca == 'Marca':
                marca1 = response[0]['body']['attributes'][0]['value_name']
            else:
                sys.exit()
    except:
        marca1 = 'nao tem'

    try:
        try:
            try:
                try:
                    linha = response[0]['body']['attributes'][4]['name']#title 5
                    if linha == 'Linha':
                        linha1 = response[0]['body']['attributes'][4]['value_name']#title 5
                        #print(linha1)
                    else:
                        sys.exit()
                except:
                    sys.exit()
            except:
                sys.exit()
        except:
            sys.exit()
    except:
        linha1 = 'nao tem'

    try:
        try:
            try:
                try:
                    try:
                        modelo = response[0]['body']['attributes'][5]['name']#title 5
                        if modelo == 'Modelo':
                            modelo1 = response[0]['body']['attributes'][5]['value_name']#title 5
                            #print(modelo1)
                        else:
                            sys.exit()
                    except:
                        modelo1 = 'nao tem'


                        # modelo = response[0]['body']['attributes'][5]['name']#title 4
                       # if modelo == 'Modelo':
                       #     modelo1 = response[0]['body']['attributes'][5]['value_name']#title 4
                       #     #print(modelo1)
                       # else:
                       #     sys.exit()
                except:
                    modelo = response[0]['body']['attributes'][6]['name']#title 3
                    if modelo == 'Modelo':
                        modelo1 = response[0]['body']['attributes'][6]['value_name']#title 3
                        #print(modelo1)
                    else:
                        sys.exit()
            except:
                modelo = response[0]['body']['attributes'][4]['name']
                if modelo == 'Modelo':
                    modelo1 = response[0]['body']['attributes'][4]['value_name']
                else:
                    sys.exit()
        except:
            modelo = response[0]['body']['attributes'][2]['name']
            if modelo == 'Modelo':
                modelo1 = response[0]['body']['attributes'][2]['value_name']
            else:
                sys.exit()
    except:
        modelo1 = 'nao tem'

    try:
        try:
            try:
                try:
                    try:
                        try:
                            try:
                                numero_peca = response[0]['body']['attributes'][8]['name']#title 5
                                if numero_peca == 'Número de peça':
                                    numero_peca1 = response[0]['body']['attributes'][8]['value_name']#title 5
                                    #print(numero_peca1)
                                else:
                                    sys.exit()
                            except:
                                numero_peca = response[0]['body']['attributes'][7]['name']#title 4
                                if numero_peca == 'Número de peça':
                                    numero_peca1 = response[0]['body']['attributes'][7]['value_name']#title 4
                                    #print(numero_peca1)
                                else:
                                    sys.exit()
                        except:
                            numero_peca = response[0]['body']['attributes'][8]['name']#title 3
                            if numero_peca == 'Número de peça':
                                numero_peca1 = response[0]['body']['attributes'][8]['value_name']#title 3
                                #print(numero_peca1)
                            else:
                                sys.exit()
                    except:
                        numero_peca = response[0]['body']['attributes'][9]['name']
                        if numero_peca == 'Número de peça':
                            numero_peca1 = response[0]['body']['attributes'][9]['value_name']
                            #print(numero_peca1)
                        else:
                            sys.exit()
                except:
                    numero_peca = response[0]['body']['attributes'][11]['name']
                    if numero_peca == 'Número de peça':
                        numero_peca1 = response[0]['body']['attributes'][11]['value_name']
                    else:
                        sys.exit()
            except:
                numero_peca = response[0]['body']['attributes'][6]['name']
                if numero_peca == 'Número de peça':
                    numero_peca1 = response[0]['body']['attributes'][6]['value_name']
                else:
                    sys.exit()
        except:
            numero_peca = response[0]['body']['attributes'][4]['name']
            if numero == 'Número de peça':
                numero_peca1 = response[0]['body']['attributes'][4]['value_name']
            else:
                sys.exit()
    except:
        numero_peca1 = 'nao tem'

    try:
        try:
            try:
                try:
                    qntd_peca = response[0]['body']['attributes'][6]['name']#title 5
                    if qntd_peca == 'Quantidade de velas':
                        qntd_peca1 = response[0]['body']['attributes'][6]['value_name']#title 5
                        #print(qntd_peca1)
                    else:
                        sys.exit()
                except:
                    qntd_peca = response[0]['body']['attributes'][6]['name']#title 4
                    if qntd_peca == 'Quantidade de velas':
                        qntd_peca1 = response[0]['body']['attributes'][6]['value_name']#title 4
                        #print(qntd_peca1)
                    else:
                        sys.exit()
            except:
                qntd_peca = response[0]['body']['attributes'][3]['name']
                if qntd_peca == 'Quantidade de velas':
                    qntd_peca1 = response[0]['body']['attributes'][3]['value_name']#title 4
                    #print(qntd_peca1)
                else:
                    sys.exit()           
        except:
            sys.exit()
    except:
        qntd_peca1 = 'nao tem'

    try:
        try:
            try:
                try:
                    try:
                        sku = response[0]['body']['attributes'][9]['name']
                        if sku == 'SKU':
                            sku1 = response[0]['body']['attributes'][9]['value_name']
                            #print(sku1)
                        else:
                            sys.exit()
                    except:
                        sku = response[0]['body']['attributes'][7]['name']
                        if sku == 'SKU':
                            sku1 = response[0]['body']['attributes'][7]['value_name']
                        else:
                            sys.exit()
                except:
                    sku = response[0]['body']['attributes'][8]['name']
                    if sku == 'SKU':
                        sku1 = response[0]['body']['attributes'][8]['value_name']
                    else:
                        sys.exit()
            except:
                sku = response[0]['body']['attributes'][10]['name']
                if sku == 'SKU':
                    sku1 = response[0]['body']['attributes'][10]['value_name']
                else:
                    sys.exit()
        except:
            sku = response[0]['body']['attributes'][5]['name']
            if sku == 'SKU':
                sku1 = response[0]['body']['attributes'][5]['value_name']
            else:
                sys.exit()
    except:
        sku1 = 'nao tem'

    try:
        try:
            codigo_universal = response[0]['body']['attributes'][1]['name']
            if codigo_universal == 'Código universal de produto':
                codigo_universal1 = response[0]['body']['attributes'][1]['value_name']
                if codigo_universal1 == 'None':
                    codigo_universal1 = 'nao tem'
                else:
                    codigo_universal1 = response[0]['body']['attributes'][1]['value_name']
            else:
                sys.exit()
        except:
            codigo_universal = response[0]['body']['attributes'][2]['name']
            if codigo_universal == 'Código universal de produto':
                codigo_universal1 = response[0]['body']['attributes'][2]['value_name']
                if codigo_universal1 == 'None':
                    codigo_universal1 = 'nao tem'
                else:
                    codigo_universal1 = response[0]['body']['attributes'][1]['value_name']
            else:
                sys.exit()       
    except:
        codigo_universal1 = 'nao tem'
    
    
    dicionario = {
        'mlb': row['anuncios'],
        'titulo': titulo,
        'preco': preco,
        'marca': marca1,
        'linha': linha1,
        'modelo': modelo1,
        'nmr de peça': numero_peca1,
        'qntd de velas': qntd_peca1,
        'sku': sku1,
        'seller_id': seller_id,
        'category_id': category_id,
        'available_quantity' : available_quantity,
        'sold_quantity' : sold_quantity,
        'listing_type_id': listing_type_id,
        'tempo': tempo,
        'condition': condition,
        'quality_picture': quality_picture,
        'payment': payment,
        'cart_eligible': cart_eligible,
        'codigo_universal': codigo_universal1,
        'link': link
    }
    
    guarda_info.append(dicionario)
    
    del titulo
    del preco
    del marca1
    del linha1
    del modelo1
    del numero_peca1
    del qntd_peca1
    del sku1
    del seller_id
    del category_id
    del available_quantity
    del sold_quantity
    del listing_type_id
    del tempo
    del condition
    del quality_picture
    del payment
    del cart_eligible
    del codigo_universal1
    del link
    
df_api = pd.DataFrame(guarda_info)
        


# In[8]:


df_api


# In[74]:


df_api['mlb'].value_counts()
df_api['mlb'].shape


# In[21]:


#tratar valores NONE
df_api = df_api.replace({None: 'nao tem'})


# In[22]:


#Salvar 
df_api.to_csv('37_mlb_com_infos.csv', index=False)


# In[ ]:




