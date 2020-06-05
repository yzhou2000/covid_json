import pandas as pd
#getting the data
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
df = pd.read_csv(url)
#getting uszip data
uszip = pd.read_csv('/home/yuzhou/AndroidStudioProjects/covid_json/uszip.csv',dtype={"ZIP":"string"})

uszipcounty=uszip[['ZIP','county','msa','st_code','state']].dropna()
uszipcounty.to_json('./us_zip.json' , orient = 'records')

uscounty=uszip[['county','state','msa']].dropna()

#create us county msa list
uscounty.drop_duplicates(subset=["county","state"],keep='first',inplace=True)


df=df[['date','county','state','cases','deaths']]
df=df.sort_values(by=['state','county','date'])
df['new cases'] = df.groupby(['state','county'])['cases'].diff().fillna(0).astype(int)
df['new deaths'] = df.groupby(['state','county'])['deaths'].diff().fillna(0).astype(int)

#create covid19 dataset by msa
msa=pd.merge(df,uscounty,on=['county','state'],how="left")
us_msa = msa.groupby(['msa','date'],as_index=False).agg({"cases":"sum","deaths":"sum","new cases":"sum","new deaths":"sum"})
us_msa.to_json('./us_msa_covid.json' , orient = 'records')


#create covid19 dataset by state

us_states = df.groupby(['state','date'],as_index=False).agg({"cases":"sum","deaths":"sum","new cases":"sum","new deaths":"sum"})


us_states.to_json('./us_states_covid.json' , orient = 'records')

#create state name and abbreviation mapping
usstate_name=uszip[['state','st_code']].drop_duplicates(subset=['state'],keep='first').set_index('state')['st_code'].to_dict()
#print(usstate_name['Tennessee'])
#output the dataset by states
df=df[~df['state'].isin(['Northern Mariana Islands','Guam','Puerto Rico'])]
for state, df_state in df.groupby('state'):
  df_state.to_json('./' + usstate_name[state] +'.json', orient ='records')
    

