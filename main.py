from database.database_conn import connect_to_db, get_table_names,get_sample_data,execute_query
from prompt.prompt import get_schema_prompt, get_sql_prompt, check_table_name
from langchain_groq import ChatGroq
from pydantic import BaseModel, RootModel
from typing import List,TypedDict
import json
from tabulate import tabulate

class response_table(BaseModel):
    table_name: str
    
class response_dq_rules(TypedDict):
    rule_name: str
    rule_discription: str

class response_sql_queries(TypedDict):
    rule_name: str
    sql_query: str

class SqlQueries(List):
    sql_queries: List[response_sql_queries]
    
class Rules(List):
    rules: List[response_dq_rules]



def get_llm():
    llm = ChatGroq(temperature=0, groq_api_key="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", model_name="llama-3.3-70b-versatile")
    return llm

def get_dq_rules(table,conn):
    llm=get_llm()
    sample_data=get_sample_data(conn,"public",table)
    schema_prompt=get_schema_prompt()
    
    llm_rules=llm.with_structured_output(Rules)
    response=llm_rules.invoke(f"User want to check the data quality of table: {table} and sample data is {sample_data} {schema_prompt}")
    # print(response)
    return response

def get_sql_query_result(data,conn):
    response_data=[]
    for item in data:
        new_item={}
        query=item['sql_query']
        result=execute_query(query,conn)
        
        extracted_result = [res[1] for res in result]
        
        if len(extracted_result) == 1:
            extracted_result = extracted_result[0]
        
        new_item['rule_name']=item['rule_name']
        new_item['sql_query']=item['sql_query']
        new_item['result']=extracted_result
        response_data.append(new_item)
    # print(response_data)
    return response_data
        

def get_sql_queries(response, table):
    llm=get_llm()
    sql_prompt=get_sql_prompt()
 
    llm_sql=llm.with_structured_output(SqlQueries)
    response=llm_sql.invoke(f"rules : {response} with table : public.{table} and follow these guidlines {sql_prompt}")
    data = response.get('iterable', [])
    
    table_data = [[item['rule_name'], item['sql_query']] for item in data]
    
    # Print the table using tabulate
    headers = ["Rule Name", "SQL Query"]
    print(tabulate(table_data, headers=headers, tablefmt="pretty"))
    return data

def confirm_table_name(conn):
    print("Welcome to Data Quality Check Chatbot")
    user_input = input("Which table would you like to check for data quality?")
    
    tables = get_table_names(conn)
    table_prompt=check_table_name()
    llm=get_llm()
    
    llm_table=llm.with_structured_output(response_table)
    matching_table=llm_table.invoke(f"User input : {user_input} which user want to search, these are the available tables: {tables}  {table_prompt}")
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
    response=get_dq_rules(table,conn)
    data=get_sql_queries(response, table)
    confirmation = input("Would like to check data quality metrics? (yes/no)")
    if confirmation.lower() == 'yes':
        response=get_sql_query_result(data, conn)
        table_data = [[item['rule_name'], item['sql_query'], item['result']] for item in response]
    
        # Print the table using tabulate
        headers = ["Rule Name", "SQL Query", "Result"]
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))
    else:
        print("Exiting the application. Thank you for using the Data Quality Check Chatbot.")
        conn.close()
    
