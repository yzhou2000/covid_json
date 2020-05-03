import pandas as pd
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
df = pd.read_csv(url)

uszip = pd.read_csv('/home/yuzhou/AndroidStudioProjects/covid_json/uszip.csv')

uscounty=uszip[['County','ST','MSA Name']].rename(columns={"County":"county","ST":"state","MSA Name":"msa"}).dropna()
uscounty.drop_duplicates(subset=["county","state"],keep='first',inplace=True)
print(uscounty[uscounty['state']=='WA'])

df=df[['date','county','state','cases','deaths']]

msa=pd.merge(df,uscounty,on=['county','state'],how="left")
us_msa = msa.groupby(['msa','date'],as_index=False).agg({"cases":"sum","deaths":"sum"})
us_msa.to_json('./us_msa_covid.json' , orient = 'records')


#print(us_msa)

us_states = df.groupby(['state','date'],as_index=False).agg({"cases":"sum","deaths":"sum"})


us_states.to_json('./us_states_covid.json' , orient = 'records')



tndf=df[df['state'] == 'Tennessee']
tndf.to_json('./tn.json' , orient = 'records')
