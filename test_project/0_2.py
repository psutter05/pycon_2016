from odo import odo
import pandas as pd

df = odo('data/2.csv', pd.DataFrame)
odo(df, 'data/2_final.csv')
