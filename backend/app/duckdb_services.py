import pandas as pd
import duckdb
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "duckdb+duckdb:///./app.duckdb"

engine = create_async_engine(DATABASE_URL)
Base = declarative_base()
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def run_duckdb_query(file, query: str):
    try:
        df = pd.read_csv(file.file)
        table_name = file.filename.split(".")[0]
        con = duckdb.connect()
        con.register(table_name, df)

        result_df = con.execute(query).fetchdf()
        return {"columns": result_df.columns.tolist(), "rows": result_df.values.tolist()}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

def get_duckdb_schema(file):
    try:
        df = pd.read_csv(file.file)
        schema = [{"column": col, "dtype": str(dtype)} for col, dtype in df.dtypes.items()]
        return {"table_name": file.filename.split(".")[0], "columns": schema}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
