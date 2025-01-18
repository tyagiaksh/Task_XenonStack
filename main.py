#%%
from database.database_conn import connect_to_db, get_table_names,get_sample_data
from prompt.prompt import get_schema_prompt, get_sql_prompt, check_table_name
from langchain_groq import ChatGroq
from pydantic import BaseModel, RootModel
from typing import List

class response_table(BaseModel):
    table_name: str
    
class response_dq_rules(BaseModel):
    rule_name: str
    rule_discription: str



def get_llm():
    llm = ChatGroq(temperature=0, groq_api_key="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", model_name="llama-3.1-8b-instant")
    return llm

def get_dq_rules(table,conn):
    llm=get_llm()
    sample_data=get_sample_data(conn,"public",table)
    print(sample_data)
    schema_prompt=get_schema_prompt()
    
    Rules = List[response_dq_rules]
    
    # llm_rules=llm.with_structured_output(Rules)
    response=llm.invoke(f"User want to check the data quality of table: {table} and sample data is {sample_data} {schema_prompt}")
    print(response.rules)
    

def confirm_table_name(conn):
    print("Welcome to Data Quality Check Chatbot")
    user_input = input("Which table would you like to check for data quality? ")
    
    tables = get_table_names(conn)
    table_prompt=check_table_name()
    llm=get_llm()
    
    llm_table=llm.with_structured_output(response_table)
    matching_table=llm_table.invoke(f"User input {user_input} which user want to search, these are the available tables: {tables}  {table_prompt}")
    if matching_table:
        confirmation = input(f"Is '{matching_table}' the table you want to perform data quality check on? (yes/no) ")
        if confirmation.lower() == 'yes':
            print(f"Performing data quality check on table: {matching_table}")
            return matching_table.table_name
        else:
            print("Exiting the application. Please try again with a different table name.")
    else:
        print("No matching table found. Please check the table name and try again.")
    
if __name__ == "__main__":
    conn=connect_to_db()
    table=confirm_table_name(conn)
    get_dq_rules(table,conn)
    
    
    
        

# %%
