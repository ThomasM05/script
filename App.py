import os
import streamlit as st
from PyPDF2 import PdfMerger
from tabula import read_pdf
import pandas as pd
import base64

# Fonction de sélection du dossier contenant les fichiers PDF
def select_folder():
    folder_path = st.sidebar.text_input("Saisir le chemin du dossier contenant les fichiers PDF:")
    return folder_path

def merge_pdfs(folder_path):
    if not folder_path:
        st.sidebar.warning("Please select a folder.")
        return

    if not os.path.isdir(folder_path):
        st.sidebar.warning("Invalid folder path.")
        return

    pdf_files = [file for file in os.listdir(folder_path) if file.endswith('.pdf')]
    if not pdf_files:
        st.sidebar.warning("No PDF files found in the selected folder.")
        return

    merger = PdfMerger()
    for pdf_file in pdf_files:
        with open(os.path.join(folder_path, pdf_file), 'rb') as file:
            merger.append(file)

    output_file_path = os.path.join(folder_path, "merged.pdf")
    with open(output_file_path, 'wb') as output_file:
        merger.write(output_file)
    st.sidebar.success(f"PDF files merged successfully. Merged file saved as: {output_file_path}")
    return output_file_path

def main():
    st.title("Hello, Bienvenue votre nouvelle Plateforme...")

    folder_path = select_folder()
    if st.sidebar.button("DEMARRER"):
        merged_pdf_path = merge_pdfs(folder_path)
        if merged_pdf_path:
            df_list = read_pdf(merged_pdf_path, encoding='ISO-8859-1', stream=True, area=[269.875, 12.75, 790.5, 961], guess=False, pages='all')
            result_df = pd.concat(df_list, ignore_index=True)
            excel_output_path = os.path.join(folder_path, "Fichier_Extrait.xlsx")
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
