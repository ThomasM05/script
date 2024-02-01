import os
import streamlit as st
from PyPDF2 import PdfMerger
from tabula import read_pdf
import pandas as pd
import base64

# Function to select the folder containing the PDF files
def select_files():
    pdf_files = st.sidebar.file_uploader("Sélectionner les fichiers PDF", type="pdf", accept_multiple_files=True)
    return pdf_files

def merge_pdfs(pdf_files):
    if not pdf_files:
        st.sidebar.warning("Veuillez sélectionner au moins un fichier PDF.")
        return

    merger = PdfMerger()
    for pdf_file in pdf_files:
        merger.append(pdf_file)

    output_file_path = "Fichier_Fusionne.pdf"
    with open(output_file_path, 'wb') as output_file:
        merger.write(output_file)
    st.sidebar.success(f"Fusion réussie des fichiers PDF. Le fichier fusionné est enregistré en tant que: {output_file_path}")
    return output_file_path

def main():
    st.title("Hello, Bienvenue sur votre nouvelle Plateforme...")

    pdf_files = select_files()
    if pdf_files:
        merged_pdf_path = merge_pdfs(pdf_files)
        if merged_pdf_path:
            df_list = read_pdf(merged_pdf_path, encoding='ISO-8859-1', stream=True, area=[269.875, 12.75, 790.5, 961], guess=False, pages='all', java_options="-Djava.awt.headless=true")
            result_df = pd.concat(df_list, ignore_index=True)
            excel_output_path = "Fichier_Extrait.xlsx"
            result_df.to_excel(excel_output_path, index=False)
            st.sidebar.success(f"Les Fichiers ont été enregistrées dans {excel_output_path}")
            st.markdown("<h2 style='text-align: center;'>TELECHARGER LE FICHIER EXCEL ICI :)</h2>", unsafe_allow_html=True)
            st.markdown(get_binary_file_downloader_html(excel_output_path, 'TELECHARGER'), unsafe_allow_html=True)

# Function to create a download link for a file
def get_binary_file_downloader_html(file_path, file_label='File'):
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">{file_label}</a>'
    return href

if __name__ == "__main__":
    main()
