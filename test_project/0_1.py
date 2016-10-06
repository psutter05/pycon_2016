from odo import odo
import pandas as pd

df = odo('data/1.csv', pd.DataFrame)
odo(df, 'data/1_final.csv')
