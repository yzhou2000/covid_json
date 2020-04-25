import pandas as pd
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
df = pd.read_csv(url)
df=df[['date','county','state','cases','deaths']]
df.to_json(r'./us_covid.json' , orient = 'records',lines=True)


