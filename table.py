import re

def square_bracket_replace(line):
    # Replace '_EMBI_KEY]' with '_SK]' and '_KEY]' with '_SK]' in the entire line before processing
    line = line.replace('_EMBI_KEY]', '_SK]')
    line = line.replace('_KEY]', '_SK]')

    print("After replacing '_EMBI_KEY]' and '_KEY]':")
    print(line)

    # Replace table names starting with [DM with [D
    line = re.sub(r'\[DM', '[D', line, count=1)  # Only replace the first occurrence which is the table name

    # Function to process each match inside square brackets
    def replace_brackets(match):
        word = match.group(1)  # Get the word inside the brackets
        # For column names starting with DM_, remove 'DM_'
        if word.startswith('DM_'):
            word = word[3:]  # Remove 'DM_' prefix
        # Check if the word contains any special characters other than underscore
        if re.search(r'[^a-zA-Z0-9_]', word):
            return f'"{word}"'  # Replace brackets with double quotes
        else:
            return word  # Remove brackets

    # Use regex to find all words enclosed in square brackets
    modified_line = re.sub(r'\[(.*?)\]', replace_brackets, line)

    # Print final modified line
    print("Final modified line:")
    print(modified_line)
    return modified_line

# Example usage
input_data = """CREATE TABLE [dbo].[DM_Sales_Full_02](
    [DM_CUSTOMER_EMBI_LI_KEY] [int] NOT NULL,
    [DM_CONTRACTOR_EMBI_KEY] [int] NOT NULL,
    [DM_DataType] [int] NOT NULL,
    [COPA_KEY] [int] NOT NULL,
    [VVP43] [decimal](13, 2) NULL,
    [Bareme_BasePrix_REP_Verif] [decimal](5, 0) NULL
)"""

# Call the function and print the output
output = square_bracket_replace(input_data)
print("\nModified Output:\n", output)
