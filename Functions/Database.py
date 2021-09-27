# Library Imports
import json, os, psycopg2
import urllib.parse as up
from dotenv import load_dotenv

# Options from Json
with open("Config/Options.json") as RawOptions:
    Options = json.load(RawOptions)

# Sqlite functions
def GetConn():
    """
    Get Connection
    ----------

    Returns a connection to the database.
    """
    up.uses_netloc.append("postgres")
    load_dotenv()
    url = up.urlparse(os.getenv("DatabaseUrl"))

    conn = psycopg2.connect(
        database = url.path[1:],
        user = url.username,
        password = url.password,
        host = url.hostname,
        port = url.port,
    )
    return conn
