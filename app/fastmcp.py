from mcp.server.fastmcp import FastMCP
from database import get_db_connection

mcp = FastMCP(name="MCP SQL Server API")

@mcp.tool(name="SQL_Dataset_Query_Tool", description="Allows AI agents to execute SQL queries on a Microsoft SQL Server database.")
def execute_sql_query(query: str):
    """Run safe SELECT queries against the SQL Server database.
    Table Names: Dataset
    Column Names: id, name, report"""
    db_connection = get_db_connection()
    try:
        sql = query.strip().lower()
        if not sql.startswith("select"):
            raise ValueError("Only SELECT queries are allowed.")

        cursor = db_connection.cursor()
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results
    except Exception as e:
        raise ValueError(f"Error executing query: {str(e)}")
    finally:
        db_connection.close()

if __name__ == "__main__":    
    mcp.run()
