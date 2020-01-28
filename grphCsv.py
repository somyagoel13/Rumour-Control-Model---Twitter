# import pandas as pd
#
# df=pd.read_csv('users1.csv',header=None)
#
# df.columns=['id','handle','followers']
# #print(df.head())
# usrs=list(df['id'])
#
# with open('fol1.csv','r') as r,open('grph.csv','w') as w:
#     for u in usrs:
#         row=[u]
#         row.append

import pandas as pd
pd.read_csv('fol1.csv', header=None).T.to_csv('grph.csv', header=False, index=False)

# import csv
# from itertools import zip
# a = zip(*csv.reader(open("fol1.csv", "rb")))
# csv.writer(open("grph.csv", "wb")).writerows(a)
