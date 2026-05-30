import streamlit as st


def footer_home():
    
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
        <div style="color:white !important"><p style="font-weight:bold; color: #E0E7FF !important; font-size:15px">Created with ❤️ and ☕ ~</p></div>
        
        <h5 style="font-weight:bold; color:white !important; font-size:16px;margin-top:0px"><i>Vineet Waman</i></h5>  
        </div>
                
                """, unsafe_allow_html=True)


def footer_dashboard():
     st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
        <p style="font-weight:bold; color:#E0E7FF;; font-size:15px">Created with ❤️ and ☕ ~</p>  
        
        <h6 style="font-weight:bold; color:black; font-size:15px font-size:18px;margin-top:0px"><i>Vineet Waman</i></h6>  
        </div>
                
                """, unsafe_allow_html=True)