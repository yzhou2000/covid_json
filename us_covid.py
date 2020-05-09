import pandas as pd
#getting the data
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
df = pd.read_csv(url)
#getting uszip data
uszip = pd.read_csv('/home/yuzhou/AndroidStudioProjects/covid_json/uszip.csv',dtype={"ZIP":"string"})

uszipcounty=uszip[['ZIP','st_code','county','msa']].dropna()
uszipcounty.to_json('./us_zip.json' , orient = 'records')

uscounty=uszip[['county','state','msa']].dropna()

#create us county msa list
uscounty.drop_duplicates(subset=["county","state"],keep='first',inplace=True)


df=df[['date','county','state','cases','deaths']]

#create covid19 dataset by msa
msa=pd.merge(df,uscounty,on=['county','state'],how="left")
us_msa = msa.groupby(['msa','date'],as_index=False).agg({"cases":"sum","deaths":"sum"})
us_msa.to_json('./us_msa_covid.json' , orient = 'records')


#create covid19 dataset by state

us_states = df.groupby(['state','date'],as_index=False).agg({"cases":"sum","deaths":"sum"})


us_states.to_json('./us_states_covid.json' , orient = 'records')

#create state name and abbreviation mapping
usstate_name=uszip[['state','st_code']].drop_duplicates(subset=['state'],keep='first').set_index('state')['st_code'].to_dict()
#print(usstate_name['Tennessee'])
#output the dataset by states
df=df[~df['state'].isin(['Northern Mariana Islands'])]
for state, df_state in df.groupby('state'):
  df_state.to_json('./' + usstate_name[state] +'.json', orient ='records')
    


tndf=df[df['state'] == 'Tennessee']
tndf.to_json('./tn.json' , orient = 'records')
