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
            res=requests.post(f"{URL}/login", auth=HTTPBasicAuth(username,password))
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
    st.subheader("Upload PDF for specific Role")
    uploaded_file = st.file_uploader("Choose a file to upload.")
    role_for_doc = st.selectbox("Target Role for docs",["doctor","nurse","patient","other"])

    if st.button("Upload Document"):
        if uploaded_file:
            files = {"file":(uploaded_file.name,uploaded_file.getvalue(),"application/pdf")}
            data = {"role":role_for_doc}
            res=requests.post(f"{URL}/docs" , files =files , data= data , auth=get_auth())
    
            if res.status_code == 200:
                doc_info = res.json()
                st.success(f"uploaded : {uploaded_file.name}")
                st.info(f"Doc Id : {doc_info['doc_id']}, Access: {doc_info['accessible_to']}")
                if doc_info.get("warning"):
                    st.warning(doc_info["warning"])
            else:
                st.error(res.json().get("detail","Upload failed !"))
        
        else:
            st.warning("Please upload a file")


# Upload medical report and get a summary
def upload_report():
    st.subheader("Upload your medical report for summary")
    uploaded_file = st.file_uploader("Upload a medical PDF report", type=["pdf"], key="report_uploader")

    if st.button("Upload and Summarize", key="upload_report"):
        if uploaded_file:
            files = {"file":(uploaded_file.name,uploaded_file.getvalue(),"application/pdf")}
            res=requests.post(f"{URL}/docs/report", files=files, auth=get_auth())

            if res.status_code == 200:
                doc_info = res.json()
                st.success(f"Report uploaded: {uploaded_file.name}")
                st.info(f"Doc Id: {doc_info.get('doc_id')}, Role: {doc_info.get('role')}")
                if doc_info.get("warning"):
                    st.warning(doc_info["warning"])
                st.markdown("### Summary")
                st.write(doc_info.get("summary", "No summary returned."))
            else:
                st.error(res.json().get("error","Upload failed !"))
        else:
            st.warning("Please upload a PDF file.")


# View uploaded reports and summaries
def view_reports(report_type=None):
    search_query = st.text_input(
        "Search by filename or upload date (YYYY-MM-DD)",
        value="",
        key=f"search_{report_type}" if report_type else "search_all"
    ).strip().lower()

    res = requests.get(f"{URL}/docs/reports", auth=get_auth())
    if res.status_code != 200:
        st.error(res.json().get("error","Unable to load reports."))
        return

    data = res.json()
    reports = data.get("reports", [])
    if not reports:
        st.info("No uploaded reports found.")
        return

    filtered = [
        report for report in reports
        if (report_type is None or report.get("type") == report_type)
        and (
            not search_query
            or search_query in report.get("filename", "").lower()
            or search_query in report.get("uploaded_at", "").lower()
        )
    ]

    if not filtered:
        st.info("No reports found for this filter.")
        return

    if report_type is None:
        grouped = {}
        for report in filtered:
            report_type_key = report.get("type", "unknown")
            grouped.setdefault(report_type_key, []).append(report)

        if "reference" in grouped:
            st.markdown("### Reference Documents")
            for report in grouped["reference"]:
                with st.expander(f"{report.get('filename')} ({report.get('role')})"):
                    st.write(f"**Uploaded by:** {report.get('owner')}")
                    st.write(f"**Role:** {report.get('role')}")
                    st.write(f"**Uploaded at:** {report.get('uploaded_at')}")
                    st.write("This document is stored as reference material for role-based access.")

        if "patient_report" in grouped:
            st.markdown("### Patient Reports")
            for report in grouped["patient_report"]:
                with st.expander(f"{report.get('filename')} ({report.get('uploaded_at')})"):
                    st.write(f"**Uploaded by:** {report.get('owner')}")
                    st.write(f"**Role:** {report.get('role')}")
                    st.write(f"**Uploaded at:** {report.get('uploaded_at')}")
                    st.markdown("**Summary**")
                    st.write(report.get('summary', 'No summary available.'))

        if "unknown" in grouped:
            st.markdown("### Other Reports")
            for report in grouped["unknown"]:
                with st.expander(f"{report.get('filename')} ({report.get('type')})"):
                    st.write(f"**Uploaded by:** {report.get('owner')}")
                    st.write(f"**Role:** {report.get('role')}")
                    st.write(f"**Uploaded at:** {report.get('uploaded_at')}")
                    st.markdown("**Summary**")
                    st.write(report.get('summary', 'No summary available.'))
        return


# chat interface :
def chat_interface():
    st.subheader("Ask a medical healthcare question:")
    msg=st.text_input("Your query")

    if st.button("Send"):
        if not msg.strip():
            st.warning("Please enter a query !")
        
        res=requests.post(f"{URL}/chat",json={"query":msg,"top_k":5},auth=get_auth())

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
        st.markdown("## Admin dashboard")
        tab1, tab2, tab3, tab4 = st.tabs(["Upload Reference Docs", "Reference Docs", "Patient Reports", "Chat"])

        with tab1:
            st.info("Upload role-specific reference documents for doctors, nurses, patients, or others.")
            upload_docs()

        with tab2:
            st.info("View all reference documents uploaded by admins.")
            view_reports(report_type="reference")

        with tab3:
            st.info("View all patient reports and summaries.")
            view_reports(report_type="patient_report")

        with tab4:
            chat_interface()

    elif st.session_state.role == "patient":
        st.markdown("## Patient dashboard")
        tab1, tab2, tab3 = st.tabs(["Upload Report", "My Reports", "Chat"])

        with tab1:
            st.info("Upload your medical report PDF and receive a concise summary.")
            upload_report()

        with tab2:
            st.info("Review your own uploaded reports and summaries.")
            view_reports()

        with tab3:
            chat_interface()

    else:
        st.markdown("## User dashboard")
        tab1 = st.tab("Chat")
        with tab1:
            st.info("Chat access only. Medical report upload is available for patients.")
            chat_interface()
