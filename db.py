import mysql.connector

server="tramway.proxy.rlwy.net"
port=25079
database="railway"
username="root"
password="CkjQqbvmmpblZmyrmLnlSEVAAURNRlRt"

conn = mysql.connector.connect(
                host=server,
                port=port,
                database=database,
                user=username,
                password=password)