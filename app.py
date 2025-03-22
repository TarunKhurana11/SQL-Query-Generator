from dotenv import load_dotenv
load_dotenv() ## load all the environment variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="SQL Query Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
        background-color: #FF4B4B;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        padding: 0.5rem;
    }
    h1 {
        color: #1E3D59;
        text-align: center;
    }
    h2 {
        color: #FF4B4B;
    }
    .stMarkdown {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

##configure our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def clean_sql_query(query):
    # Remove markdown code block formatting
    query = query.replace('```sql', '').replace('```', '')
    # Remove any leading/trailing whitespace
    query = query.strip()
    return query

#Function to load Google Gemini Model and provide sql query as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-1.5-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Function to retieve query fro sql database
def read_sql_query(sql,db):
    try:
        # Clean the SQL query before executing
        sql = clean_sql_query(sql)
        conn=sqlite3.connect(db)
        cur=conn.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"SQL Error: {str(e)}")
        return None

def display_results(data, query):
    if not data:
        st.info("No results found for this query.")
        return

    # Check if the query is a COUNT query
    if "COUNT" in query.upper():
        st.metric("Count", data[0][0])
        return

    # For other queries, create a DataFrame
    try:
        # Get column names from the query
        if "SELECT *" in query.upper():
            columns = ['Name', 'Class', 'Section', 'Marks']
        else:
            # Extract column names from the SELECT clause
            select_part = query.upper().split("SELECT")[1].split("FROM")[0].strip()
            columns = [col.strip() for col in select_part.split(",")]
        
        df = pd.DataFrame(data, columns=columns)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error displaying results: {str(e)}")
        st.write("Raw results:", data)

##Define your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION and MARKS n\nFor example, \nExample 1 - How many entries of records are present?,
the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ; 
\nExample 2 - Tell me all the students studying in Data Science class?, 
the SQL command will be something like this SELECT * FROM STUDENT
 where CLASS="Data Science";
IMPORTANT: Return ONLY the SQL query without any markdown formatting or code blocks.
Do not include ```sql or ``` in your response.
"""
]

# Main App
st.title("🤖 SQL Query Generator")

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This app helps you generate SQL queries from natural language questions.
    Simply type your question and get the corresponding SQL query and results!
    
    **Example Questions:**
    - How many students are in Data Science class?
    - Show me all students with marks above 80
    - What are the different sections?
    """)

# Main content
st.markdown("### Ask your question about the student database")

# Input area with better styling
question = st.text_input(
    "Enter your question here:",
    placeholder="e.g., How many students are in Data Science class?",
    key="input"
)

# Submit button
submit = st.button("Generate SQL Query", type="primary")

# Results area
if submit:
    with st.spinner("Generating SQL query..."):
        response = get_gemini_response(question, prompt)
        
        # Clean and display SQL Query
        clean_query = clean_sql_query(response)
        st.markdown("### Generated SQL Query")
        st.code(clean_query, language="sql")
        
        # Execute and display results
        st.markdown("### Query Results")
        data = read_sql_query(response, "student.db")
        display_results(data, clean_query)

# Footer
st.markdown("---")
st.markdown("Made by using Streamlit and Google Gemini")