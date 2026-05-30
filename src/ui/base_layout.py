import streamlit as st



def style_background_home():

    st.markdown("""
        <style>

                .stApp {
                    background: #5865F2 !important;
                }

                .stApp div[data-testid="stColumn"]{
                    background-color:#E0E3FF !important;
                    padding:2.5rem !important;
                    border-radius: 5rem !important;
                    }
        </style>  

                """
            ,unsafe_allow_html=True)
    

def style_background_dashboard():

    st.markdown("""
        <style>

                .stApp {
                    background: #E0E3FF !important;
                }

        </style>  

                """
            ,unsafe_allow_html=True)
    

    

def style_base_layout():
# asdasd
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

                
         /* Hide Top Bar of streamlit */
                
            #MainMenu, footer, header {
                visibility: hidden;
            }
                
            .block-container {
                padding-top:1.5rem !important;    
            }
            
            

            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                line-height:1.1 1important;
                margin-bottom:0rem !important;
            }
                

            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                line-height:0.9 !important;
                margin-bottom:0rem !important;
            }
                
            h3, h4, p {
                font-family: 'Outfit', sans-serif;    
            }
                

            button{
                border-radius: 1.5rem !important;
                background-color: #5865F2 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

  /* PRIMARY BUTTON */

button[kind="primary"]{
    border-radius: 1.5rem !important;
    background-color: #5865F2 !important;
    color: white !important;
    border: none !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    transition: all 0.25s ease-in-out !important;
}

button[kind="primary"] p{
    color: white !important;
}

button[kind="primary"]:hover{
    background-color: #4752d6 !important;
    transform: scale(1.05);
}

button[kind="primary"]:hover p{
    color: white !important;
}



/* SECONDARY BUTTON */

button[kind="secondary"]{
    border-radius: 1.5rem !important;
    background-color: #EB459E !important;
    color: white !important;
    border: none !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    transition: all 0.25s ease-in-out !important;
}

button[kind="secondary"] p{
    color: white !important;
}

button[kind="secondary"]:hover{
    background-color: #d63b8c !important;
    transform: scale(1.05);
}

button[kind="secondary"]:hover p{
    color: white !important;
}



/* TERTIARY BUTTON */

button[kind="tertiary"]{
    border-radius: 1.5rem !important;
    background-color: #1E1F2E !important;
    color: white !important;
    border: none !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    transition: all 0.25s ease-in-out !important;
}

button[kind="tertiary"] p{
    color: white !important;
}

button[kind="tertiary"]:hover{
    background-color: #2a2c40 !important;
    transform: scale(1.05);
}

button[kind="tertiary"]:hover p{
    color: white !important;
}

            button:hover{
                transform :scale(1.05)}
                
  /* Main input container */
div[data-baseweb="input"]{
    background-color: white !important;
    border-radius: 14px !important;
    border: 2px solid transparent !important;
}

/* Actual text input */
div[data-baseweb="input"] input{
    background-color: white !important;
    color: black !important;
    caret-color: black !important;
}

/* Placeholder */
div[data-baseweb="input"] input::placeholder{
    color: rgba(0,0,0,0.5) !important;
}

/* Password eye icon container */
div[data-baseweb="base-input"]{
    background-color: white !important;
}

/* Labels */
label{
    color: black !important;
    font-weight: 700 !important;
}

/* Focus effect */
div[data-baseweb="input"]:focus-within{
    border: 2px solid #5865F2 !important;
    box-shadow: 0 0 12px rgba(88,101,242,0.4) !important;
}
hr{
    border-color: rgba(0,0,0,0.25) !important;
}

/* Streamlit divider */
[data-testid="stDivider"]{
    background-color: rgba(0,0,0,0.25) !important;
}

/* Markdown text */
p{
    color: black !important;
}



[data-testid="stDialog"] *{
    color:white !important;
}

[data-testid="stDialog"] label{
    color:white !important;
}

[data-testid="stDialog"] p{
    color:white !important;
}

[data-testid="stDialog"] span{
    color:white !important;
}
<style>

[data-testid="stDialog"] button[aria-label="Close"] svg{
    fill:white !important;
    color:white !important;
}
[data-testid="stDialog"] .stFileUploader label{
    color:white !important;
}

[data-testid="stDialog"] .stFileUploader small{
    color:#d1d5db !important;
}
[data-testid="stDialog"] button {
    color: white !important;
}

[data-testid="stDialog"] button * {
    color: white !important;
    fill: white !important;
    stroke: white !important;
}
[data-testid="stDialog"] button[aria-label="Close"]{
    color:white !important;
}

[data-testid="stDialog"] button[aria-label="Close"] svg{
    stroke:white !important;
    color:white !important;
}
button[aria-label="Close"]{
    display:none !important;
}



        </style>  

                """
            ,unsafe_allow_html=True)