import streamlit as st
import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

load_dotenv()

URL = os.getenv("BASE_URL")

st.set_page_config(page_title = "MEDICAL HEALTHCARE RAG CHATBOT !!", layout = "centered")

if "username" not in st.session_state:
    st.session_state.username=""
    st.session_state.password=""
    st.session_state.role=""
    st.session_state.logged_in=False
    st.session_state.mode="auth"

def get_auth():
    return HTTPBasicAuth(st.session_state.username,st.session_state.password)

def auth_ui():
    st.title("Medical RAG Assistance")
    st.subheader("Login or Signup")

    tab1, tab2 = st.tabs(["Login" , "Signup"])

    with tab1:
        username = st.text_input("Username" , key="login_user")
        password = st.text_input("Password", type="password" , key= "login_password")
        if st.button("Login"):
            res=requests.get(f"{URL}/login",auth=HTTPBasicAuth(username,password))
            if res.status_code == 200:
                user_data = res.json()
                st.session_state.username = username
                st.session_state.password = password
                st.session_state.role = user_data["role"]
                st.session_state.logged_in = True 
                st.session_state.mode = "chat"
                st.success(f"Welcome {username}")

            else:
                st.error(res.json().get("detail","Login failed"))

    with tab2:
        new_user = st.text_input("New Username" , key="signup_user")
        new_pass = st.text_input("New Pass", type="password" , key= "signup_pass")
        new_role = st.selectbox("Choose Role",["admin","doctor","nurse","patient","other"])
        if st.button("Signup"):
            payload = {"username":new_user,"password":new_pass,"role":new_role}
            res=requests.post(f"{URL}/signup",json=payload)

            if res.status_code == 200:
                st.success("Signup successful ! You can login.")
                
            else:
                st.error(res.json().get("detail","Signup failed"))

# Upload PDF (Admin only)
def upload_docs():
    st.subheader = ("Upload PDF for specific Role")
    uploaded_file = st.file_uploader("Choose a file to upload.")
    role_for_doc = st.selectbox("Target Role for docs",["doctor","nurse","patient","other"])

    if st.button("Upload Document"):
        if uploaded_file:
            files = {"file":(uploaded_file.name,uploaded_file.getvalue(),"application/pdf")}
            data = {"role":role_for_doc}
            res=requests.post(f"{URL}/uploaded_docs" , files =files , data= data , get_auth=get_auth())
    
            if res.status_code == 200:
                doc_info = res.json()
                st.success(f"uploaded : {uploaded_file.name}")
                st.info(f"Doc Id : {doc_info["doc_id"]}, Access:{doc_info['accessible_to']}")
            
            else:
                st.error(res.json().get("detail","Upload failed !"))
        
        else:
            st.warning("Please upload a file")

# chat interface :
def chat_interface():
    st.subheader("Ask a medical healthcare question:")
    msg=st.text_input("Your query")

    if st.button("Send"):
        if not msg.strip():
            st.warning("Please enter a query !")
        
        res=requests.post(f"{URL}/chat",data={"message":msg},auth=get_auth())

        if res.status_code==200:
            reply=res.json()
            st.markdown("### Answer: ")
            st.success(reply["answer"])

            if reply.get("sources"):
                for src in reply["sources"]:
                    st.write(f"--{src}")

            else:
                st.error(res.json().get("detail","Something went wrong."))
            


if not st.session_state.logged_in:
    auth_ui()

else:
    st.title(f"Welcome , {st.session_state.username}")
    st.markdown(f"**Role** : {st.session_state.role} ")
    
    if st.button("Logout"):
        st.session_state.logged_in=False
        st.session_state.username=""
        st.session_state.password=""
        st.session_state.role=""
        st.session_state.mode="auth"
        st.rerun()

    if st.session_state.role == "admin":
        upload_docs()
        st.divider()
        chat_interface()

    else:
        chat_interface()
