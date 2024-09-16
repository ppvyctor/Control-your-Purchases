import streamlit as st
import re
import regex
import pandas as pd
import numpy as np
import tempfile

def registration_product(database, path, word = None, option = None):
    if word is None:
        product = st.text_input("Digite o nome do produto")
        left, right = st.columns(2) # Split the screen in two columns
        preco = left.number_input("Digite o preço *UNITÁRIO* do produto", min_value = 0.0) # Input for the price of the product
        quantidade = right.number_input("Digite a quantidade do produto", min_value = 1) # Input for the quantity of the product
    
    else:
        pos = 0
        for x in range(database.shape[0]):
                if database.loc[x, "Produto"] == word:
                    pos = x
                    break
        
        product = st.text_input("Digite o nome do produto", value = database.loc[pos, "Produto"])
        left, right = st.columns(2) # Split the screen in two columns
        preco = left.number_input("Digite o preço *UNITÁRIO* do produto", min_value = 0.0, value = database.loc[pos, "Preço"]) # Input for the price of the product
        quantidade = right.number_input("Digite a quantidade do produto", min_value = 1, value = database.loc[pos, "Quantidade"]) # Input for the quantity of the product
    
    
    if not product in database["Produto"].values or option == "Editar produtos da lista": # If the product is not in the list
        if preco != 0 and re.sub(r"[^a-zà-öø-ÿç]", '', product.lower()) != "": # If the price was different from 0 and the product name is not empty
            if st.button("Adicionar o produto na lista"):  # Button to add the product to the list
                if word is None:
                    database = pd.concat([database, pd.DataFrame({"Produto": [product], "Preço": [preco], "Quantidade": [quantidade]})], 
                                                ignore_index = True) # Add the product to the list
                    database.to_csv(path, index = False) # Save the list to the file
                
                else:
                    database.loc[pos, "Produto"] = product
                    database.loc[pos, "Preço"] = preco
                    database.loc[pos, "Quantidade"] = quantidade
                    database.to_csv(path, index = False)
                    


path = tempfile.gettempdir() + "/product_list.csv"# Path to the user's home directory

try:
    product_list = pd.read_csv(path) # Try to read the file
except:
    product_list = pd.DataFrame({"Produto": [], "Preço": [], "Quantidade": []}) # If the file doesn't exist, create a new DataFrame
    product_list.to_csv(path, index = False) # Save the DataFrame to the file


clear_list = st.sidebar.button("Limpar lista de produtos") # Button in sidebar for clear the list of products

if clear_list: # If the button is clicked
    product_list = pd.DataFrame({"Produto": [], "Preço": [], "Quantidade": []}) # Create a new DataFrame
    product_list.to_csv(path, index = False) # Save the DataFrame to the file

st.markdown('''<h1 style = "text-align: center; font-weight: bold">Controle de Compras!!🛒</h1>''', unsafe_allow_html = True) #  Title of the page

if product_list.shape[0] != 0:
    list_option = ["Adicionar Produto", "Editar produtos da lista", "Remover Produto"]

else:
    list_option = ["Adicionar Produto"]

option = st.selectbox("Selecione a opção desejada", list_option) # Selectbox with the options

st.write("---") # Line break


if option == "Adicionar Produto":
    registration_product(database = product_list, path = path) # Call the function to register a product
        
elif option == "Editar produtos da lista":
    edit_options = st.selectbox("Escolha como deseja procurar o produto a ser editado", ["Nome do produto", "ID do produto"])
    
    if edit_options == "Nome do produto":
        word = st.text_input("Digite o nome do produto").lower()
        
        if re.sub(r"[^a-zà-öø-ÿç]", '', word.lower()) != "":
            if len(word) > 2:
                research = "(" + word + ")" + "{e<=" + str(len(word) // 3) + "}" # Create a regex pattern to search for the product name
            else:
                research = f"({word})" + "{e<=1}"
            research = [product_list.loc[x, "Produto"] for x in range(product_list.shape[0]) if regex.findall(research, product_list.loc[x, "Produto"].lower()) != []] # Search for the product name in the list
            
            if word != []:
                word = st.selectbox("Escolha o produto desejado", research)
                
                st.write("---")
                
                registration_product(database = product_list, path = path, word = word, option = option)
                
            else:
                st.markdown('<b style = "font-size: 25px">Nenhum produto encontrado...</b>', unsafe_allow_html = True)
                word = None
    
    elif edit_options == "ID do produto":
        pos = st.number_input("Digite o ID do produto", min_value = 0, max_value = product_list.shape[0] - 1)
        
        registration_product(database = product_list, path = path, word = product_list.loc[pos, "Produto"], option = option)
        
else:
    edit_options = st.selectbox("Escolha como deseja remover o produto a ser editado", ["Nome do produto", "ID do produto"])
    
    if edit_options == "Nome do produto":
        word = st.text_input("Digite o nome do produto").lower()
        
        if re.sub(r"[^a-zà-öø-ÿç]", '', word.lower()) != "":
            if len(word) > 2:
                research = "(" + word + ")" + "{e<=" + str(len(word) // 3) + "}" # Create a regex pattern to search for the product name
            else:
                research = f"({word})" + "{e<=1}"
            research = [product_list.loc[x, "Produto"] for x in range(product_list.shape[0]) if regex.findall(research, product_list.loc[x, "Produto"].lower()) != []] # Search for the product name in the list
            
            if word != []:
                word = st.selectbox("Escolha o produto desejado", research)
                
                if st.button("Remover produto"):
                    product_list = product_list.drop(index = product_list[product_list["Produto"] == word].index)
                    product_list.to_csv(path, index = False)
    
    else:
        pos = st.number_input("Digite o ID do produto", min_value = 0, max_value = product_list.shape[0] - 1)
        
        if st.button("Remover produto"):
            product_list = product_list.drop(index = pos)
            product_list.to_csv(path, index = False)


st.write("---") # Line break

if product_list.shape[0] == 0: # If the list is empty
    st.markdown('<b style = "font-size: 25px">Nenhum produto adicionado à lista no momento...</b>', unsafe_allow_html = True) # Show a message

else: # If the list is not empty
    left, middle, right = st.columns([0.25, 0.5, 0.25]) # Split the screen in three columns
    middle.dataframe(product_list) # Show database
    
    Total_Value = np.array(product_list["Preço"]) * np.array(product_list["Quantidade"])
    
    middle.write("Total da Compra:  R$" + f"{sum(Total_Value):.2f}".replace(".", ",")) # Show the total value of the products