import pandas as pd
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
df = pd.read_csv(url)
df=df[['date','county','state','cases','deaths']]
df.to_json('./us_covid.json' , orient = 'records',lines=True)

tndf=df[df['state'] == 'Tennessee']
tndf.to_json('./tn.json' , orient = 'records')
