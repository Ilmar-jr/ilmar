import streamlit as st
import pandas as pd
import web

st.set_page_config(layout="wide")

if st.button("Atualizatr", type="primary"):
    tabela = web.webscraping()
    vendedor = tabela['Vendedor'].unique()
    perfil = tabela['perfil'].unique()
    cargo = tabela['cargo'].unique()
    forma = tabela['forma de pagamento'].unique()
    
    #tabela.to_excel('base.xlsx')
    #st.table(tabela)
else:
    tabela=pd.read_excel('base.xlsx')
    vendedor = tabela['Vendedor'].unique()
    perfil = tabela['perfil'].unique()
    cargo = tabela['cargo'].unique()
    forma = tabela['forma de pagamento'].unique()

dados = pd.DataFrame(tabela)

with st.sidebar:
    vendedor = st.selectbox('vendedor',vendedor,index=None)
    perfil = st.selectbox('perfil',perfil,index=None)
    cargo = st.selectbox('cargo',cargo,index=None)
    forma = st.selectbox('forma',forma,index=None)
   

if vendedor:
    dados = dados[dados['Vendedor'] == vendedor]

if perfil:
    dados = dados[dados['perfil'] == perfil]

if cargo:
    dados = dados[dados['cargo'] == cargo]

if forma:
    dados = dados[dados['forma de pagamento'] == forma]

st.table(dados)
