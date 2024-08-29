
CREATE PROCEDURE dbo.usp_ManageDM_Sales_Full_02
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
         INSERT INTO dbo.D_Sales_Full_02 (
             DataType, "COPA SK", D_PERIOD_DAY_SK, D_PERIOD_MONTH_SK, 
             -- (List other columns as needed)
             DATE_STAT, ACCOUNTED, SHIPPED
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
         UPDATE dbo.D_Sales_Full_02
         SET
             D_PERIOD_DAY_SK = @DM_PERIOD_DAY_EMBI_KEY,
             D_PERIOD_MONTH_SK = @DM_PERIOD_MONTH_EMBI_KEY,
             DATE_STAT = @DATE_STAT,
             ACCOUNTED = @ACCOUNTED,
             SHIPPED = @SHIPPED
             -- (Include other columns as needed)
         WHERE 
             DataType = @DataType 
             AND COPA_SK = @COPA_KEY;
             -- (Modify WHERE clause as needed)
     END
     -- Action: Delete
     IF @Action = 'DELETE'
     BEGIN
         DELETE FROM dbo.D_Sales_Full_02
         WHERE 
             DataType = @DataType 
             AND COPA_SK = @COPA_KEY;
             -- (Modify WHERE clause as needed)
     END
     -- Action: Select
     IF @Action = 'SELECT'
     BEGIN
         SELECT 
             DataType, COPA_SK, D_PERIOD_DAY_SK, D_PERIOD_MONTH_SK,
             -- (List other columns as needed)
             DATE_STAT, ACCOUNTED, SHIPPED
             -- (Include other columns as needed)
         FROM dbo.D_Sales_Full_02
         WHERE 
             (DataType = @DataType OR @DataType IS NULL) 
             AND (COPA_SK = @COPA_KEY OR @COPA_KEY IS NULL);
             -- (Adjust filters as needed)
     END
 END;