# =================================== IMPORT MODULE YANG DIGUNAKAN =============================== #

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from   streamlit_option_menu import option_menu 
import plotly.express as px
import plotly.figure_factory as ff
import base64
import pickle

# ====================================== IMPORT DATASET VISUALISASI ====================================== #

dataset = pd.read_csv('Status_Gizi_Bul_Viz.csv')

# ====================================== MEMBUAT TAMEPILAM ====================================== #

st.set_page_config(
    page_title="nbc_status_stunting",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Encoding untuk gambar background
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('bg_nbc_fix.jpg') 

# Encoding untuk gambar side bar
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("bg_side.jpg")
page_bg_img = f"""
<style>

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.write("""
            # APLIKASI KLASIFIKASI STATUS STUNTING PADA BALITA DI KABUPATEN BULELENG 🤱
""")

# ====================================== MENU APLIKASI ====================================== #

pilihan =   option_menu(
            menu_title="MENU",  # required
            options=["HOME", "KLASIFIKASI", "REFRENSI"],  # required
            icons=["house", "bi bi-bar-chart-fill", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
#==========================> MEMBUAT FUNGSI APLIKASI <=============================== #
def math ():
    
    loaded_model = pickle.load(open("Status_Stunting_Balita.sav", "rb"))
    akurasi = 81
    col1, col2,col3= st.columns(3)
    with col1:
        Umur = st.number_input("Masukan Umur Dalam Bulan", min_value=0, max_value=150, label_visibility="visible")
    with col2 :
        BB = st.number_input("Masukan Berat Badan dalam Kg ", min_value=0, max_value=100, label_visibility="visible")
    with col3:
        TB = st.number_input("Masukan Tinggi Badan dalam cm ", min_value=0, max_value=150, label_visibility="visible")
    with col2 :
        ST = st.selectbox("Pilih Status Gizi",["","Normal","Pendek"])
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
                st.success("Balita Tergolong Stunting")
                st.write("Akurasi yang didapat : ", round(akurasi), "%")
            
#==========================> MEMBUAT FUNGSI LOG IN DAN SIGN UP USER <=============================== #

# Membuat Enkripsi
# digunakan untuk keamanan data admin

#==========================> MEMBUAT FUNGSI VISUALISASI DATA <=============================== #
def bar():
	fig = px.bar(dataset, x="Kecamatan", y=dataset.columns,
              hover_data={"Kecamatan"},
              title='Persentase Status Balita di Kabupaten Buleleng Tahun 2021')
	fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y")
	st.plotly_chart(fig,use_container_width = True)

import hashlib                                      # Module untuk melakukan penyandian atau enkripsi

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# ============================================ MEMBUAT DATABASE ======================================= #

import sqlite3 
conn = sqlite3.connect('data_admin.db')
c = conn.cursor()

# Membuat Fungsi sebagai tabel data admin
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

# Membuat Fungsi sebagai inputan data user
def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

# Membuat Fungsi sebagai login user
def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

# Fungsi menampilkan semua data admin/user
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

# ============================================ SETTING TAMPILAN TIAP MENU ======================================= #

if pilihan == "HOME":
    st.image('stunting_fix.png')
elif pilihan == "KLASIFIKASI":
   
	menu = ["Login","SignUp"]
	gambar = st.sidebar.image("atas.png", use_column_width=True)
	choice = st.sidebar.selectbox(" ",menu)


	if choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))

			if result:

				# main.refresh()
				st.success("Logged In as {}".format(username))
				st.sidebar.image("anak.png", use_column_width=True)

				task = st.selectbox("Pilih Informasi",["Visualisasi Data","Analytics","Profiles"])
				if task == "Visualisasi Data":
					bar()
				elif task == "Analytics":
					st.write("Proses Klasifikasi")
					math ()
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")

	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")
else :
    st.write("Data Bersumber Dari Dinas Kesehatan Kabupaten Buleleng")
