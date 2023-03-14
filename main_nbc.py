import streamlit as st
import pandas as pd
import numpy as np
import pickle
def math ():
    
    loaded_model = pickle.load(open("Status_Stunting_Balita.sav", "rb"))
    akurasi = 81
    col1, col2,col3= st.columns(3)
    with col1:
        Umur = st.number_input("Masukan Umur Dalam Bulan", min_value=0, max_value=150, label_visibility="visible")
    with col2 :
        BB = st.number_input("Masukan Berat Badan dalam Kg ", min_value=0, max_value=100, label_visibility="visible")
    with col3:
        TB = st.number_input("Masukan Tinggi Badan dalam cm ", min_value=0, max_value=100, label_visibility="visible")
    with col2 :
        ST = st.selectbox("Pilih Status Gizi",["Normal","Pendek"])
        if ST == "Normal" :
            ST = int(0)
        else:
            ST = int(1)
    
    user = ([[Umur,BB,TB,ST]])
    if user == ([[0,0,0,0]]):
        st.warning("Tidak Bisa di Proses ")
    else:
        st.write("")
    nbc_pred = loaded_model.predict(user)
    with col2:
        if st.button("Submit"):
            if nbc_pred == ([0]):
                st.success("Balita tergolong Normal")
                st.write("Akurasi yang didapat : ", round(akurasi), "%")
            else :
                st.success("Balita Tergolong Stunting ")
                st.write("Akurasi yang didapat : ", round(akurasi), "%")
                  

math()

