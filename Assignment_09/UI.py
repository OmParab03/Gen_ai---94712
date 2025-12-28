from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
import pandas as pd
from pandasql import sqldf
from selenium import webdriver
from selenium.webdriver.common.by import By
import streamlit as st 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#LLM
llm = init_chat_model(
    model="qwen/qwen3-8b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="non-needed"
)


@tool
def csv_query_tool(question, csv_path):
    """
    Accepts a CSV file path and a user question.
    Converts question to SQL using LLM, executes on CSV using pandasql, 
    and returns result with explanation.
    """
    df = pd.read_csv(csv_path)
    schema = ", ".join([f"{col} ({dtype})" for col, dtype in zip(df.columns, df.dtypes)])

  
    sql_prompt = f"""
    You are an expert SQL developer.
    Table: df
    Schema: {schema}
    Convert the following user question into SQL:
    {question}
    Return only the SQL query.
    """

    sql_query = llm.invoke(sql_prompt).content.strip()

    try:
        result_df = sqldf(sql_query, {"df": df})
    except Exception as e:
        return f"SQL Error: {e}"

    
    explain_prompt = f"""
    You are a data analyst.
    Question: {question}
    SQL Query: {sql_query}
    Result: {result_df.to_string(index=False)}
    Explain the result in simple English.
    """

    explanation = llm.invoke(explain_prompt).content
    return explanation



@tool
def internship_tool_available_internship_program(question):
    """
    Scrapes Sunbeam Available internship program  table data using Selenium,
    answers user's question strictly based on scraped data.
    """
    chrome_options=Options()
    chrome_options.add_argument("--headless=new")
    dr=webdriver.Chrome(options=chrome_options)
    dr.implicitly_wait(5)

    dr.get("https://www.sunbeaminfo.in/internship")
    wait=WebDriverWait(dr,10)

    dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    plus_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']")))
    dr.execute_script("arguments[0].scrollIntoView(true);", plus_button)
    plus_button.click()


    table2=dr.find_element(By.ID,value="collapseSix")
    tbody=table2.find_element(By.TAG_NAME,"tbody")
    rows=tbody.find_elements(By.TAG_NAME,"tr")


    for row in rows:
        cols=row.find_elements(By.TAG_NAME,"td")
        info_table2={
            "Technology":cols[0].text,
            "Aim":cols[1].text,
            "Prerequisite":cols[2].text,
            "Learning":cols[3].text,
            "Location":cols[4].text,
        
        }
    return info_table2
@tool
def internship_tool_Batch_schedule(question):
    """
    Scrapes Sunbeam internship Batch schedule table data using Selenium,
    answers user's question strictly based on scraped data.
    """
    


    chrome_options=Options()
    chrome_options.add_argument("--headless=new")
    dr=webdriver.Chrome(options=chrome_options)
    dr.implicitly_wait(5)

    dr.get("https://www.sunbeaminfo.in/internship")
    


    table1=dr.find_element(By.CSS_SELECTOR,"table.table.table-bordered.table-striped")

    body=table1.find_element(By.TAG_NAME,"tbody")
    rows = body.find_elements(By.TAG_NAME,"tr")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME,"td")
        if len(cols)<7:
            continue
        info_table1={
                "sr":cols[0].text,
                "batch":cols[1].text,
                "batch duration":cols[2].text,
                "start date":cols[3].text,
                "End date":cols[4].text,
                "time":cols[5].text,
                "fees":cols[6].text
            }
    return info_table1

# Create the agent with  tools

agent = create_agent(
    model=llm,
    tools=[csv_query_tool, 
           internship_tool_available_internship_program,
           internship_tool_Batch_schedule],
    system_prompt="You are a helpful assistant. Use the appropriate tool to answer questions.but when the tool is used or return any scrapping from any website you return all scrapping data as it is tool returned."
)



def info_csv(csv_file):
    if csv_file is not None:
        df = pd.read_csv(csv_file)
        return df.head(), df.dtypes
    return None, None



#UI
with st.sidebar:
    choice=["CSV-QNA","Scrapping"]
    option=st.selectbox("select for best output",choice)
st.title("Chat bot ")
st.write("Best for data scrapping and CSV-QNA.")

if option == "CSV-QNA":
    csv_path = st.text_input("enter file path..")

    if csv_path:
        head, types = info_csv(csv_path)
        st.dataframe(head)
        st.code(types)

        user_input = st.chat_input("Enter question.")

        if user_input:
            with st.spinner("Generating..."):
                result = agent.invoke({
                    "messages": [
                        {"role": "user", "content": f"{user_input}\nCSV_PATH={csv_path}"}
                    ]
                })
                
                llm_output = result["messages"][-1]
            st.write("AI:", llm_output.content)

else:
    user_input = st.chat_input("ask scrapping question...")

    if user_input:
        with st.spinner("Generating..."):
            result = agent.invoke({
                "messages": [
                    {"role": "user", "content": user_input}
                ]
            })
            
            llm_output = result["messages"][-1]
        st.write("AI:", llm_output.content)
