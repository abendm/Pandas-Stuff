# CPI (base 2009)
base09 = cpi.loc['2009'].mean()
cpi09 = 100 * (cpi / base09)
cpi09.head()
