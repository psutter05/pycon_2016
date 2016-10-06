from odo import odo
import pandas as pd

df_1 = odo('data/1_final.csv', pd.DataFrame)
df_2 = odo('data/2_final.csv', pd.DataFrame)

print('Something has changed')

df_final = pd.concat([df_1, df_2])
odo(df_final, 'data/final.csv')
