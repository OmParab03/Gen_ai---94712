import pandas as pd
import pandasql as ps


file="emp_hdr.csv"
df = pd.read_csv(file)


query = "SELECT * FROM data WHERE sal > 2000"
result=ps.sqldf(query, {"data":df})
print(result)