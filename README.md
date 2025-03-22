# SQL-Query-Generator
 
# Description
This project is a **Streamlit web application** that allows users to convert natural language questions into SQL queries using **Google Gemini AI**. It interacts with an **SQLite database** to fetch the data corresponding to the generated SQL query and display it in the web app.
# Features
- Converts natural language input into SQL queries using **Google Gemini AI**.
- Executes SQL queries on an **SQLite** database.
- User-friendly interface built with **Streamlit**.
- Secure management of API keys using **dotenv**.
- Demonstrates AI and database integration in real-world applications.
# Technologies used
- **Google Gemini AI** for natural language processing and query generation.
- **Streamlit** for creating the web interface.
- **SQLite** for managing and querying the database.
- **Python** for backend logic.
- **dotenv** for environment variable management.
# Usage
- After running the app, you will be prompted to input a natural language question in the text input box.
- For example:
  - **"Which students have marks greater than 80?"**
  - **"How many students are in Section A?"**
- The app will generate an SQL query, execute it on the database, and display the results on the UI.
