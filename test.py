import re

def process_procedure(sql_procedure):
    # Function to replace column names inside square brackets
    def replace_brackets(match):
        word = match.group(1)  # Get the word inside the brackets
        # Replace column names ending with 'embi_key' or 'key' with 'SK'
        if word.lower().endswith('embi_key') or word.lower().endswith('key'):
            word = re.sub(r'(?i)embi_key$', 'SK', word)
            word = re.sub(r'(?i)key$', 'SK', word)
        # Remove prefix 'DM_' from column names
        if word.lower().startswith('dm_'):
            word = word[3:]  # Remove 'DM_' prefix
        return f'[{word}]'  # Return the modified word inside brackets

    # Replace all column names inside square brackets
    modified_procedure = re.sub(r'\[(.*?)\]', replace_brackets, sql_procedure)
    
    return modified_procedure

# Example SQL Procedure
sql_procedure = """CREATE PROCEDURE [dbo].[usp_ManageDM_Sales_Full_02]
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
            [DataType], [COPA_KEY], [DM_PERIOD_DAY_EMBI_KEY], [DM_PERIOD_MONTH_EMBI_KEY], 
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
END;"""

# Process the SQL procedure
modified_procedure = process_procedure(sql_procedure)

# Save the modified SQL procedure to a text file
output_file = "modified_procedure.sql"
with open(output_file, "w") as file:
    file.write(modified_procedure)

print(f"Modified SQL procedure has been saved to {output_file}.")
