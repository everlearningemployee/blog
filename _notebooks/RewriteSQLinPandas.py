#%% Pandas import + 데이터 불러오기
import pandas as pd
# pd.set_option('display.max_columns', 3)
# pd.set_option('display.max_columns', None)

airports = pd.read_csv('data/airports.csv')
airport_freq = pd.read_csv('data/airport-frequencies.csv')
runways = pd.read_csv('data/runways.csv')

#%% Dataframe 
print(airports)
print('='*80)
print(airports.shape)
print('='*80)
print(airports.columns)
print('='*80)
pd.set_option('display.max_columns', None)
print(airports.describe())
pd.set_option('display.width', 200)
print(airports)

#%% SELECT, WHERE, DISTINCT, LIMIT
'''
select * 
  from airport_freq;
'''
# pd.set_option('display.max_columns', 5)
pd.set_option('display.max_columns', None)

print(airport_freq)
# print(type(airport_freq))

#%% SELECT, WHERE, DISTINCT, LIMIT
'''
select description 
  from airport_freq;
'''
df = airport_freq.description
print(df)
print(type(df))

#%% SELECT, WHERE, DISTINCT, LIMIT
'''
select name 
  from airports
 limit 3;
'''
s = airports.head(10).name
print(s)
print('='*30)
s = airports.name.head(10)
print(s)
print(type(s))

#%% SELECT, WHERE, DISTINCT, LIMIT
'''
select ident, 
       name, 
       municipality 
  from airports;
'''
df = airports[['ident', 'name', 'municipality']]
print(df)
print(type(df))

#%% SELECT, WHERE, DISTINCT, LIMIT
'''
select * 
  from airports 
 where municipality = 'Los Angeles';
'''
# df = airports[airports.municipality == 'Anchor Point']
df = airports[airports.municipality == 'Los Angeles']
print(df)


#%% SELECT, WHERE, DISTINCT, LIMIT
'''
select ident, 
       name, 
       municipality 
  from airports 
 where municipality = 'Los Angeles'
'''

df = airports[airports.municipality == 'Los Angeles'] \
             [['ident', 'name', 'municipality']]
# df = airports[airports.municipality == 'Anchor Point'][['ident', 'name', 'municipality']]
print(df)
print('='*80)
df = airports[['ident', 'name', 'municipality']][airports.municipality == 'Los Angeles']
print(df)

#%% SELECT, WHERE, DISTINCT, LIMIT
'''
select distinct type 
  from airport;
'''
a = airports.type.unique()
print(a)

# df = airports[['ident', 'name', 'municipality']].unique()
# print(df)

#%% SELECT with multiple conditions
'''
select * 
  from airports 
 where iso_region = 'US-CA' 
   and type = 'seaplane_base';
'''
df = airports[(airports.iso_region == 'US-CA') 
              & (airports.type == 'seaplane_base')] \
             [['name', 'iso_region', 'type']]
             
print(df)
print(type(df))

#%% SELECT with multiple conditions
'''
select ident, 
       name, 
       municipality 
  from airports 
 where iso_region = 'US-CA' 
   and type = 'large_airport';
'''
df = airports[(airports.iso_region == 'US-CA') & (airports.type == 'large_airport')] \
             [['ident', 'name', 'municipality']]
print(df)
print('='*80)
df = airports[['ident', 'name', 'municipality']] \
             [(airports.iso_region == 'US-CA') & (airports.type == 'large_airport')] 
print(df)

#%% ORDER BY
'''
  select * 
    from airport_freq 
   where airport_ident = 'KLAX' 
order by type;
'''
df = airport_freq[airport_freq.airport_ident == 'KLAX'].sort_values('type')
print(df)
print('='*80)

'''
  select * 
    from airport_freq 
   where airport_ident = 'KLAX' 
order by type desc;
'''
df = airport_freq[airport_freq.airport_ident == 'KLAX'].sort_values('type', ascending=False)
print(df)

#%% IN… NOT IN
'''
select * 
  from airports 
 where type in ('heliport', 'balloonport');
'''
df = airports[airports.type.isin(['heliport', 'balloonport'])]
print(df)
print('='*80)

'''
select * 
  from airports 
 where type not in ('heliport', 'balloonport');
'''
df = airports[~airports.type.isin(['heliport', 'balloonport'])]
print(df)

#%% GROUP BY, COUNT, ORDER BY
'''
  select iso_country, 
         type, 
         count(*) 
    from airports 
group by iso_country, 
         type 
order by iso_country, 
         type;
'''
s = airports.groupby(['iso_country', 'type']).size()
print(s)
print('='*80)

'''
  select iso_country, 
         type, 
         count(*) 
    from airports 
group by iso_country, 
         type 
order by iso_country, 
         count(*) desc;
'''
df = airports.groupby(['iso_country', 'type']).size()  \
             .to_frame('size').reset_index()  \
             .sort_values(['iso_country', 'size'], ascending=[True, False])
print(df)

#%% HAVING
'''
  select type, 
         count(*) 
    from airports 
   where iso_country = 'US' 
group by type 
  having count(*) > 1000 
order by count(*) desc;
'''
s = airports[airports.iso_country == 'US'] \
             .groupby('type').filter(lambda g: len(g) > 1000) \
             .groupby('type').size() \
             .sort_values(ascending=False)
print(s)

#%% Top N records
'''
  select iso_country 
    from by_country 
order by size desc 
   limit 10;
'''
by_country = airports.groupby(['iso_country']).size()\
                     .to_frame('airport_count').reset_index()

df = by_country.nlargest(10, columns='airport_count')
print(df)
print('='*80)

'''
  select iso_country 
    from by_country 
   order by size desc 
   limit 10 
  offset 10;
'''  
df = by_country.nlargest(10, columns='airport_count').tail(5)
print(df)

#%% Aggregate functions (MIN, MAX, MEAN)
'''
  select max(length_ft), 
         min(length_ft), 
         avg(length_ft), 
         median(length_ft)   -- 사용자정의 함수로 만들었다 치고
    from runways;
'''
print(runways.head(3))
print(runways.describe())

# df = runways.agg({'length_ft': ['min', 'max', 'mean', 'median', 'count', 'std']})
df = runways.agg({'airport_ref': ['min', 'max', 'mean', 'median', 'count', 'std']})
print(df)
print('='*80)
print(df.T)

#%% JOIN
'''
  select airport_ident, 
         a.type, 
         a.description, 
         frequency_mhz 
    from airport_freq as a join airports as b
      on airport_freq.airport_ref = airports.id 
   where airports.ident = 'KLAX'
'''
df = airport_freq.merge(
            airports[airports.ident == 'KLAX'][['id']], 
            left_on='airport_ref', 
            right_on='id', 
            how='inner'
         )[['airport_ident', 'type', 'description', 'frequency_mhz']]
print(df)
print('='*80)

df = pd.merge(
            airport_freq,
            airports[airports.ident == 'KLAX'][['id']], 
            left_on='airport_ref', 
            right_on='id', 
            how='inner'
         )[['airport_ident', 'type', 'description', 'frequency_mhz']]
print(df)

#%% UNION ALL and UNION
'''
  select name, 
         municipality 
    from airports 
   where ident = 'KLAX' 
union all 
  select name, 
         municipality 
    from airports 
   where ident = 'KLGB';
'''
print(airports[airports.ident == 'KLAX'][['name', 'municipality']])
print('='*80)
print(airports[airports.ident == 'KLGB'][['name', 'municipality']])
print('='*80)
df = pd.concat([
            airports[airports.ident == 'KLAX'][['name', 'municipality']], 
            airports[airports.ident == 'KLGB'][['name', 'municipality']]
        ])
print(df)

#%% INSERT
'''
create table heroes (id integer, name text);	
insert into heroes values (1, 'Harry Potter');	
insert into heroes values (2, 'Ron Weasley');	
insert into heroes values (3, 'Hermione Granger');	
'''

df1 = pd.DataFrame({'id': [1, 2], 'name': ['Harry Potter', 'Ron Weasley']})
print(df1)
print('='*80)
df2 = pd.DataFrame({'id': [3], 'name': ['Hermione Granger']})
print(df2)
print('='*80)
df1 = pd.concat([df1, df2]).reset_index(drop=True)
print(df1)


#%% UPDATE
'''
update airports 
   set home_link = 'http://www.lawa.org/welcomelax.aspx' 
 where ident == 'KLAX';
'''

airports[airports['ident'] == 'KLAX'][['home_link']]
# airports[airports.ident == 'KLAX'][['home_link']]
print(airports.loc[airports['ident'] == 'KLAX', 'home_link'])

airports.loc[airports['ident'] == 'KLAX', 'home_link'] = 'http://www.lawa.org/welcomelax.aspx'
print(airports.loc[airports['ident'] == 'KLAX', 'home_link'])

airports.loc[airports.type == 'heliport', 'home_link'] = 'http://haha'
print(airports[airports.type == 'heliport'][['ident', 'name', 'home_link']])

#%% Immutability

airports.home_link = 'http//hoho' # work
print(airports.home_link)
print('='*80)
airports[airports['ident'] == 'KLAX'].home_link = 'http//haha' # not work
print(airports[airports['ident'] == 'KLAX'].home_link)

#%% DELETE
'''
delete from airport_freq 
      where type = 'MISC';
'''
pd.set_option('display.width', 200)
airport_freq = pd.read_csv('data/airport-frequencies.csv')

airport_freq1 = airport_freq[airport_freq.type != 'MISC']
print(airport_freq1)
print('='*80)
airport_freq = airport_freq.drop(airport_freq[airport_freq.type == 'MISC'].index)
print(airport_freq)

#%% Pandas에서 직접 SQL 구문 실행하기
df1 = airport_freq[airport_freq.airport_ident == 'KLAX'] \
                  .sort_values('type', ascending=False)
print(df1)
print('='*80)

sql = '''
  select * 
    from airport_freq 
   where airport_ident = 'KLAX' 
order by type desc;
'''
df2 = ps.sqldf(sql)
print(df2)


