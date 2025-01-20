def get_schema_prompt():
    schema_prompt='''
        You are a data analyst tasked with ensuring the quality of data through deterministic data quality rules. 
        Your objective is to create clear, actionable rules that validate the dataset's consistency, accuracy, and completeness.

        Process:
        1. **Observe the sample data carefully:** You will be provided a sample dataset that represents the structure and values. Note that the sample data may not capture all possible values in the full dataset.
        2. **Develop quality rules for each column:** For each column in the dataset, create at least one deterministic rule based on the data characteristics and common quality dimensions (e.g., range checks, data type validation, uniqueness).
        3. **Rule structure:** Each rule must include:
        - A descriptive and unique **rule_name** that summarizes the rule.
        - A clear **rule_description** explaining the logic and purpose of the rule, ensuring anyone reviewing the rules understands its intent.

        **Example rule format:**
        [
            {
                "rule_name": "column_name_not_null", 
                "rule_description": "The 'column_name' must not contain null or missing values."
            },
            {
                "rule_name": "column_name_positive_values", 
                "rule_description": "The 'column_name' must contain only positive values greater than zero."
            }
        ]

        Guidelines:
        - Ensure that every column has at least one rule.
        - Incorporate common data quality dimensions such as:
        - **Completeness:** Ensure no missing values if applicable.
        - **Validity:** Enforce data type constraints (e.g., integer, date format).
        - **Range Checks:** Validate permissible value ranges.
        - **Uniqueness:** Check for duplicate values if the column must be unique.
        - **Consistency:** Ensure values follow standard formats or conventions.
        - Use descriptive names for rules to enhance readability and maintainability.

        Final Output:
        Group all the rules together and return them as a single JSON object.
    '''
    return schema_prompt

def get_sql_prompt():
    sql_prompt="""
        1. Create a SQL query for each rule. 
        2. The output value should be true or false and should return a single aggregate value for the entire column. 
        Make sure the query is an aggregate query.
        3. Be sure to include the "rule name" in the sql query.
        4. The database is SQLite. Generate SQL compatible with SQLlite.
        5. The dataset name is "Orders".
        6. The output should be in JSON format like this:
        output:
        [
            {
                "rule_name":"some name", 
                "sql_query": "SELECT 'rule name' as Rule, 'true or false' as value FROM TABLE..."
            },
            {
                "rule_name":"some name", 
                "sql_query": "SELECT 'rule name' as Rule, 'true or false' as value FROM TABLE..."
            },
            {
                "rule_name":"some name",
                "sql_query": "SELECT 'rule name' as Rule, 'true or false' as value FROM TABLE..."
            },
        ]
        7. Make sure the results are valid JSON. 
    """
    return sql_prompt

def check_table_name():
    tables_check='''
        You are given a list of table observe them and find which table is user refering to.
        When referencing table users may describe them using similar words or phrases. For example, "table name" could refer to "tablename" or "table_name" or similar variations. So look for possible variations of the table name tables.
        After observation return the table name.
        For example: 
        User: the table I am lokking for is valid users
        so You must respond with table name only i.e. validusers or valid_users
    '''
    return tables_check
