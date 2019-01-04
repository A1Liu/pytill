# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
import pandas as pd

def sql_query(database, query, size = None):
    """"Returns a DataFrame object containin the results the of the sql query. Database can be the URL or the engine"""
    if type(database) is str:
        engine = create_engine(database)
    else:
        engine = database
    with engine.connect() as conn:
        rs = conn.execute(query)
        if size is None:
            df = pd.DataFrame(rs.fetchall())
        else:
            df = pd.DataFrame(rs.fetchmany(size))
        df.columns = rs.keys()
        return df




#conn =
#resultset = conn.execute(query)
#df = pd.DataFrame(resultset.fetchall())
#conn.close()
#return df