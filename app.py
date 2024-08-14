
import pandas as pd
import os

# Definujte cestu jako proměnnou
cesta = "/Users/alesligas/Library/CloudStorage/GoogleDrive-ales.ligas@cncenter.cz/Ostatní počítače/Můj notebook/projekty/Krajské a senátní volby 2024/krajské/data"

# Nastavte tuto cestu jako aktuální pracovní adresář
os.chdir(cesta)

# Registracni listiny a kandidati
kzrk = pd.read_excel(os.path.join(cesta, 'KZ2024reg20240807_xlsx', 'kzrk.xlsx'))
kzrkl = pd.read_excel(os.path.join(cesta, 'KZ2024reg20240807_xlsx', 'kzrkl.xlsx'))
kzrkl_s = pd.read_excel(os.path.join(cesta, 'KZ2024reg20240807_xlsx', 'kzrkl_s.xlsx'))
kzrkl_slozeni = pd.read_excel(os.path.join(cesta, 'KZ2024reg20240807_xlsx', 'kzrkl_slozeni.xlsx'))

# ciselniky
cisob = pd.read_excel(os.path.join(cesta, 'KZ2024ciselniky20240807_xlsx', 'cisob.xlsx'))
cns = pd.read_excel(os.path.join(cesta, 'KZ2024ciselniky20240807_xlsx', 'cns.xlsx'))
cnumnuts = pd.read_excel(os.path.join(cesta, 'KZ2024ciselniky20240807_xlsx', 'cnumnuts.xlsx'))
cpp = pd.read_excel(os.path.join(cesta, 'KZ2024ciselniky20240807_xlsx', 'cpp.xlsx'))
cvs_slozeni = pd.read_excel(os.path.join(cesta, 'KZ2024ciselniky20240807_xlsx', 'cvs_slozeni.xlsx'))
cvs = pd.read_excel(os.path.join(cesta, 'KZ2024ciselniky20240807_xlsx', 'cvs.xlsx'))
kzciskr = pd.read_excel(os.path.join(cesta, 'KZ2024ciselniky20240807_xlsx', 'kzciskr.xlsx'))
kzcoco = pd.read_excel(os.path.join(cesta, 'KZ2024ciselniky20240807_xlsx', 'kzcoco.xlsx'))

kzrk = kzrk.merge(kzciskr,on="KRZAST")
kzrk = kzrk.merge(kzrkl_s,on="KSTRANA")
kzrk = kzrk.merge(cpp,on="PSTRANA")

kzrk.sort_values(["NAZEVKRZ","KSTRANA"],inplace=True)
kzrk["KSTRANA"] = kzrk["KSTRANA"].astype(str)
kzrk["ZKRATKAK8"] = kzrk["KSTRANA"] + " - " + kzrk["ZKRATKAK8"]

kzrk.info()

data = kzrk[["PORCISLO","NAZEVKRZ","NAZEVPLNY","JMENO","PRIJMENI","TITULPRED","TITULZA","VEK","POVOLANI","BYDLISTEN","ZKRATKAK8","ZKRATKAP8"]]
data["JMENO"] = data["JMENO"].astype(str)
data["PRIJMENI"] = data["PRIJMENI"].astype(str)

data["Name"] = data["JMENO"] + " " + data["PRIJMENI"]

data["TITULPRED"] = data["TITULPRED"].astype(str)
data["TITULZA"] = data["TITULZA"].astype(str)

data["Title"] = data["TITULPRED"] + ", " + data["TITULZA"]


import numpy as np

# Předpokládejme, že 'Title' je sloupec, ve kterém chcete odstranit ", nan", "nan" a ", " pokud neexistuje titul
# Tento kód byste použili po načtení a filtrování dat

# Pokud sloupec obsahuje skutečné NaN hodnoty, převeďte je na prázdný řetězec
data['Title'] = data['Title'].fillna('')

# Odstraňte řetězec ", nan" z každé hodnoty ve sloupci 'Title'
data['Title'] = data['Title'].str.replace(', nan', '', regex=False)

# Nahradí každý výskyt "nan" samotný prázdným řetězcem
data['Title'] = data['Title'].replace('nan', '')

# Odstraňte ", " na začátku nebo na konci řetězce, které vzniklo v případě chybějícího titulu
data['Title'] = data['Title'].str.replace(r'^, | ,$', '', regex=True)


# Odstraňte jakýkoli výskyt "nan" v textu, včetně případů jako "nanMBA"
data['Title'] = data['Title'].replace(r'nan', '', regex=True)

# Odstraňte případnou přebytečnou čárku a mezeru, pokud zbyla po odstranění "nan"
data['Title'] = data['Title'].str.replace(r'^, | ,$', '', regex=True)


data.info()

####### Streamlit #########

import streamlit as st
import pandas as pd

# Inicializace session state pro text input
if 'text_input' not in st.session_state:
    st.session_state.text_input = ''

# Streamlit app title
st.title('Kandidáti v krajských volbách 2024')

# Search bar for candidate name (vyhledávání napříč celou listinou)
search_name = st.text_input('Hledat podle příjmení', value=st.session_state.text_input).lower()

# Pokud je zadán nový vyhledávací dotaz, aktualizujte session state
if search_name != st.session_state.text_input:
    st.session_state.text_input = search_name
    st.experimental_rerun()  # Zajistí, že nový výraz bude okamžitě vyhledán

# Načtení dat podle aktuálního vyhledávacího dotazu
if st.session_state.text_input:
    filtered_data = data[data['Name'].str.lower().str.contains(st.session_state.text_input)]
else:
    selected_NAZEVKRZ = st.selectbox('Vyberte kraj', data['NAZEVKRZ'].unique())
    filtered_data = data[data['NAZEVKRZ'] == selected_NAZEVKRZ]

    selected_ZKRATKAK8 = st.selectbox('Vyberte volební uskupení', filtered_data['ZKRATKAK8'].unique())
    filtered_data = filtered_data[filtered_data['ZKRATKAK8'] == selected_ZKRATKAK8]

# Zobrazit tlačítko "Zpět" pouze pokud je potvrzeno vyhledávání
if st.session_state.text_input:
    if st.button("Zpět"):
        st.session_state.text_input = ''  # Vymazání session state
        st.experimental_rerun()  # Obnovení stránky pro vymazání vyhledávacího pole

# Checkbox to show only leaders (zobrazí pouze kandidáty s PORCISLO rovno 1)
show_leaders_only = st.checkbox('Zobrazit pouze lídry')

if show_leaders_only:
    filtered_data = filtered_data[filtered_data['PORCISLO'] == 1]

# Seřaďte kandidáty podle PORCISLO
filtered_data['PORCISLO'] = filtered_data['PORCISLO'].astype(int)
filtered_df = filtered_data.sort_values(by='PORCISLO')

# Display the filtered candidate list as text
if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        candidate_header = f"<span style='font-size:20px; font-weight:bold;'>{row['PORCISLO']} {row['Name']}</span>"
        region_info = f"<span style='font-size:12px; float:right;'>{row['NAZEVKRZ']}</span>"

        # Změna barvy na červenou pro text kraje
        region_info = f"<span style='font-size:13px; float:right; color:#FF4B4B;'>{row['NAZEVKRZ']}</span>"
        
        if row['Title']:
            candidate_info = f"{row['Title']}, {row['VEK']} let, {row['POVOLANI']}, {row['BYDLISTEN']}, politická příslušnost: {row['ZKRATKAP8']}"
        else:
            candidate_info = f"{row['VEK']} let, {row['POVOLANI']}, {row['BYDLISTEN']}, politická příslušnost: {row['ZKRATKAP8']}"
        
        full_candidate_info = f"{candidate_header} {region_info}<br><span style='font-size:17px;'>{candidate_info}</span>"
        st.markdown(full_candidate_info, unsafe_allow_html=True)
else:
    st.write('Žádný kandidát neodpovídá zadaným kritériím.')


