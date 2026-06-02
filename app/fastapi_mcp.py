from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi_mcp import FastApiMCP
from .database import get_db_connection

app = FastAPI( title="MCP SQL Server API", version="1.0.0", 
              description="API for executing SQL queries on a Microsoft SQL Server database using MCP.")

mcp = FastApiMCP(app, name="SQL Dataset Query Tool",
                 description="Allows AI agents to execute SQL queries on a Microsoft SQL Server database.")

mcp.mount_http()

class SQLQueryRequest(BaseModel):
    query: str

@app.get("/", summary="Welcome", tags=["General"])
async def root():
    return {"message": "Welcome to the MCP SQL Server API! Use the /query_datasets endpoint to execute SQL SELECT queries."}

@app.post("/query_datasets", summary="Execute a SQL SELECT query against the database", tags=["SQL Queries"])
async def query_datasets(request: SQLQueryRequest, db_connection=Depends(get_db_connection)):    
    """
    Run safe SELECT queries against the SQL Server database. 
    The query must be a SELECT statement and should not contain any potentially harmful operations (e.g., INSERT, UPDATE, DELETE, DROP). 
    The results will be returned as JSON.
    """
    try:
        sql = request.query.strip().lower()
        if not sql.startswith("select"):
            raise HTTPException(status_code=400, detail="Only SELECT queries are allowed.")

        cursor = db_connection.cursor()
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return JSONResponse(content={"results": results})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error executing query: {str(e)}")
    finally:
        db_connection.close()