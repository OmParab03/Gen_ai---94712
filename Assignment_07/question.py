import streamlit as st
import pandas as pd
import pandasql as ps
import os
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

st.title("📊 CSV SQL Chatbot")
st.write("Ask questions about your CSV file in natural language. The app will generate SQL and summarize results.")

with st.sidebar.header("File uploading."):
     csv_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])


llm_sql = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("groq_api")
)

if csv_file:
    df = pd.read_csv(csv_file)

    st.subheader("Preview of CSV")
    st.dataframe(df.head())

    st.subheader("CSV Data Types")
    st.code(df.dtypes)

    question = st.text_input("Ask anything about the CSV (e.g., count of male employees)")

    if st.button("Run Query") and question:
        with st.spinner("Generating SQL query..."):
            llm_input = f"""
            Table Name: data
            Table Schema: {df.dtypes}
            Question: {question}
            Instruction:
                Write a SQL query for the above question.
                Generate SQL query only in plain text format and nothing else.
                If you cannot generate the query, then output 'Error'.
            """

            result = llm_sql.invoke(llm_input)
            query = result.content.strip()


        if query.lower() != "error":
            try:
                ans = ps.sqldf(query, {"data": df})

                st.subheader("Query Result")
                st.dataframe(ans)

                url = "http://127.0.0.1:1234/v1"
                llm_summary = ChatOpenAI(
                    base_url=url,
                    model="qwen/qwen3-8b",
                    api_key="dummy_api"
                )

                summary_prompt = (
                    "Give me only a summary of the given data in English in few sentences. Data:\n"
                    + ans.to_string(index=False)
                )

                st.subheader("Summary")
                summary_placeholder = st.empty()
                summary_text = ""

                for chunk in llm_summary.stream(summary_prompt):
                    if chunk.content:
                        summary_text += chunk.content
                        summary_placeholder.markdown(summary_text)

            except Exception as e:
                st.error(f"Error executing SQL: {e}")
else:
    st.info("Please upload a CSV file to begin.")
