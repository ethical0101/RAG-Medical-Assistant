import streamlit as st
from utils.api import upload_pdfs_api

def render_uploader():
    st.sidebar.header("📥 Upload Medical Documents (.PDFs)")

    uploaded_files=st.sidebar.file_uploader("Upload Multiple PDFs", accept_multiple_files=True, type=["pdf"])

    if st.sidebar.button("Upload DB") and uploaded_files:
        with st.sidebar.spinner("Processing PDFs..."):
            try:
                response=upload_pdfs_api(uploaded_files)
                if response.status_code == 200:
                    st.sidebar.success("✅ PDFs uploaded successfully!")
                else:
                    try:
                        detail=response.json().get("detail", "Upload failed")
                    except Exception:
                        detail="Upload failed"
                    st.sidebar.error(f"❌ Upload failed: {detail}")
            except Exception as e:
                st.sidebar.error(f"❌ Error: {str(e)}")
