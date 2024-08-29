# import re

# def process_procedure(sql_procedure):
#     # Function to replace column names inside square brackets
#     def replace_brackets(match):
#         word = match.group(1)  # Get the word inside the brackets
        
#         # Column name transformations
#         # Replace column names ending with 'embi_key' or 'key' with 'SK'
#         if word.lower().endswith('embi_key') or word.lower().endswith('key'):
#             word = re.sub(r'(?i)embi_key$', 'SK', word)
#             word = re.sub(r'(?i)key$', 'SK', word)
#         # Remove prefix 'DM_' from column names
#         if word.startswith('DM_'):
#             word = word[3:]  # Remove 'DM_' prefix
#         # Check if the word contains any special characters other than underscore
#         if re.search(r'[^a-zA-Z0-9_]', word):
#             return f'"{word}"'  # Replace brackets with double quotes
#         else:
#             return word  # Remove brackets

#     # Replace column name patterns
#     sql_procedure = re.sub(r'\[(.*?)\]', replace_brackets, sql_procedure)

#     # Function to replace table names
#     def replace_table_names(match):
#         table_name = match.group(0)
#         # Replace '[DM' with '[D' for table names
#         return table_name.replace('[DM', '[D')

#     # Pattern to identify table names using SQL structure context
#     table_pattern = r'(?i)(INSERT INTO|UPDATE|DELETE FROM|FROM|JOIN)\s+\[DM_[a-zA-Z0-9_]+\]'
#     # Replace table names matching the pattern
#     sql_procedure = re.sub(table_pattern, replace_table_names, sql_procedure)

#     return sql_procedure

# # Example SQL Procedure
# sql_procedure = """
# CREATE PROCEDURE [dbo].[usp_ManageDM_Sales_Full_02]
#     @Action VARCHAR(10),  -- Defines the action to be performed ('INSERT', 'UPDATE', 'DELETE', 'SELECT')
#     @DataType INT = NULL,
#     @COPA_KEY INT = NULL,
#     @DM_PERIOD_DAY_EMBI_KEY INT = NULL,
#     @DM_PERIOD_MONTH_EMBI_KEY INT = NULL,
#     -- (Include other parameters as needed)
#     @DATE_STAT DATETIME = NULL,
#     @ACCOUNTED INT = NULL,
#     @SHIPPED INT = NULL
#     -- (Add more parameters for other fields)
# AS
# BEGIN
#     SET NOCOUNT ON;

#     -- Action: Insert
#     IF @Action = 'INSERT'
#     BEGIN
#         INSERT INTO [dbo].[DM_Sales_Full_02] (
#             [DataType], [COPA_KEY], [DM_PERIOD_DAY_EMBI_KEY], [DM_PERIOD_MONTH_EMBI_KEY], 
#             -- (List other columns as needed)
#             [DATE_STAT], [ACCOUNTED], [SHIPPED]
#             -- (Include other columns as needed)
#         )
#         VALUES (
#             @DataType, @COPA_KEY, @DM_PERIOD_DAY_EMBI_KEY, @DM_PERIOD_MONTH_EMBI_KEY,
#             -- (List other values as needed)
#             @DATE_STAT, @ACCOUNTED, @SHIPPED
#             -- (Include other values as needed)
#         );
#     END

#     -- Action: Update
#     IF @Action = 'UPDATE'
#     BEGIN
#         UPDATE [dbo].[DM_Sales_Full_02]
#         SET
#             [DM_PERIOD_DAY_EMBI_KEY] = @DM_PERIOD_DAY_EMBI_KEY,
#             [DM_PERIOD_MONTH_EMBI_KEY] = @DM_PERIOD_MONTH_EMBI_KEY,
#             [DATE_STAT] = @DATE_STAT,
#             [ACCOUNTED] = @ACCOUNTED,
#             [SHIPPED] = @SHIPPED
#             -- (Include other columns as needed)
#         WHERE 
#             [DataType] = @DataType 
#             AND [COPA_KEY] = @COPA_KEY;
#             -- (Modify WHERE clause as needed)
#     END

#     -- Action: Delete
#     IF @Action = 'DELETE'
#     BEGIN
#         DELETE FROM [dbo].[DM_Sales_Full_02]
#         WHERE 
#             [DataType] = @DataType 
#             AND [COPA_KEY] = @COPA_KEY;
#             -- (Modify WHERE clause as needed)
#     END

#     -- Action: Select
#     IF @Action = 'SELECT'
#     BEGIN
#         SELECT 
#             [DataType], [COPA_KEY], [DM_PERIOD_DAY_EMBI_KEY], [DM_PERIOD_MONTH_EMBI_KEY],
#             -- (List other columns as needed)
#             [DATE_STAT], [ACCOUNTED], [SHIPPED]
#             -- (Include other columns as needed)
#         FROM [dbo].[DM_Sales_Full_02]
#         WHERE 
#             ([DataType] = @DataType OR @DataType IS NULL) 
#             AND ([COPA_KEY] = @COPA_KEY OR @COPA_KEY IS NULL);
#             -- (Adjust filters as needed)
#     END
# END;"""

# # Process the SQL procedure
# modified_procedure = process_procedure(sql_procedure)

# # Save the modified SQL procedure to a text file
# output_file = "modified_procedure.sql"
# with open(output_file, "w") as file:
#     file.write(modified_procedure)

# print(f"Modified SQL procedure has been saved to {output_file}.")



import re

def transform_sql_procedure(input_procedure, output_file):
    def replace_column_name(match):
        # Extract the column name inside brackets
        column = match.group(1)
        # Replace '_EMBI_KEY' and '_KEY' with '_SK'
        if column.endswith('EMBI_KEY') or column.endswith('KEY'):
            column = re.sub(r'(EMBI_KEY|KEY)$', 'SK', column)
        # Remove 'DM_' prefix from column names
        if column.startswith('DM_'):
            column = column[3:]
        # If the column name contains special characters other than underscore, wrap in double quotes
        if re.search(r'[^a-zA-Z0-9_]', column):
            return f'"{column}"'
        return column

    def replace_table_name(match):
        # Replace table names starting with [DM to [D
        table_name = match.group(0)
        return table_name.replace('[DM', '[D', 1)  # Replace only the first occurrence

    # Process each line to replace table and column names accordingly
    lines = input_procedure.splitlines()
    modified_lines = []

    for line in lines:
        # Check and replace table names
        line = re.sub(r'\[DM\w+\]', replace_table_name, line)

        # Replace column names inside square brackets
        line = re.sub(r'\[(.*?)\]', replace_column_name, line)

        # Append the modified line
        modified_lines.append(line)

    # Join all modified lines into the final output
    modified_procedure = '\n'.join(modified_lines)

    # Write the modified procedure to the specified output file
    with open(output_file, 'w') as file:
        file.write(modified_procedure)

# Example usage
input_procedure = """
CREATE PROCEDURE [dbo].[usp_ManageDM_Sales_Full_02]
     @Action VARCHAR(10),  -- Defines the action to be performed ('INSERT', 'UPDATE', 'DELETE', 'SELECT')
     @DataType INT = NULL,
     @COPA_KEY INT = NULL,
     @DM_PERIOD_DAY_EMBI_KEY INT = NULL,
     @DM_PERIOD_MONTH_EMBI_KEY INT = NULL,
     -- (Include other parameters as needed)
     @DATE_STAT DATETIME = NULL,
     @ACCOUNTED INT = NULL,
     @SHIPPED INT = NULL
     -- (Add more parameters for other fields)
 AS
 BEGIN
     SET NOCOUNT ON;
     -- Action: Insert
     IF @Action = 'INSERT'
     BEGIN
         INSERT INTO [dbo].[DM_Sales_Full_02] (
             [DataType], [COPA KEY], [DM_PERIOD_DAY_EMBI_KEY], [DM_PERIOD_MONTH_EMBI_KEY], 
             -- (List other columns as needed)
             [DATE_STAT], [ACCOUNTED], [SHIPPED]
             -- (Include other columns as needed)
         )
         VALUES (
             @DataType, @COPA_KEY, @DM_PERIOD_DAY_EMBI_KEY, @DM_PERIOD_MONTH_EMBI_KEY,
             -- (List other values as needed)
             @DATE_STAT, @ACCOUNTED, @SHIPPED
             -- (Include other values as needed)
         );
     END
     -- Action: Update
     IF @Action = 'UPDATE'
     BEGIN
         UPDATE [dbo].[DM_Sales_Full_02]
         SET
             [DM_PERIOD_DAY_EMBI_KEY] = @DM_PERIOD_DAY_EMBI_KEY,
             [DM_PERIOD_MONTH_EMBI_KEY] = @DM_PERIOD_MONTH_EMBI_KEY,
             [DATE_STAT] = @DATE_STAT,
             [ACCOUNTED] = @ACCOUNTED,
             [SHIPPED] = @SHIPPED
             -- (Include other columns as needed)
         WHERE 
             [DataType] = @DataType 
             AND [COPA_KEY] = @COPA_KEY;
             -- (Modify WHERE clause as needed)
     END
     -- Action: Delete
     IF @Action = 'DELETE'
     BEGIN
         DELETE FROM [dbo].[DM_Sales_Full_02]
         WHERE 
             [DataType] = @DataType 
             AND [COPA_KEY] = @COPA_KEY;
             -- (Modify WHERE clause as needed)
     END
     -- Action: Select
     IF @Action = 'SELECT'
     BEGIN
         SELECT 
             [DataType], [COPA_KEY], [DM_PERIOD_DAY_EMBI_KEY], [DM_PERIOD_MONTH_EMBI_KEY],
             -- (List other columns as needed)
             [DATE_STAT], [ACCOUNTED], [SHIPPED]
             -- (Include other columns as needed)
         FROM [dbo].[DM_Sales_Full_02]
         WHERE 
             ([DataType] = @DataType OR @DataType IS NULL) 
             AND ([COPA_KEY] = @COPA_KEY OR @COPA_KEY IS NULL);
             -- (Adjust filters as needed)
     END
 END;
"""

output_file = 'modified_procedure.sql'

transform_sql_procedure(input_procedure, output_file)
print(f"Modified procedure has been written to {output_file}")
