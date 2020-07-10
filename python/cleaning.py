import pandas as pd
from pymongo import MongoClient
import numpy as np

# alapértelmezett beállításokkal, csupán az adatbázisnév tetszőleges
def get_mongo_database(
    db_name, host="localhost", port=27017, username=None, password=None
):
    """ Elérjük a db_name-mel hivatkozott adatbázist MongoDB-ről, hitelesítő adatokkal vagy azok nélkül """

    if username and password:
        mongo_uri = "mongodb://{}:{}@{}/{}".format(username, password, host, db_name)
        # URI = uniform resource identifier
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[
        db_name
    ]  # itt már a második féle jelölést használjuk az adatbázis eléréséhez


def mongo_to_dataframe(
    db_name,
    collection,
    query={},
    host="localhost",
    port=27017,
    username=None,
    password=None,
    no_id=True,
):
    """ Létrehoz egy DataFrame-t egy MongoDB collection-ból """

    db = get_mongo_database(db_name, host, port, username, password)

    # megkeresi a collection-ból a lekérdezés szerinti elemeket
    cursor = db[collection].find(query)

    df = pd.DataFrame(list(cursor))

    # amennyiben azt szeretnénk, hogy törölje ki a MongoDB által hozzáadott id-t
    if no_id:
        del df["_id"]

    return df


# alapvetően, a removeexisting kitörli, ha már létezik,
# a skipifexists, átugorja, ha már létezik,
# de a forceupdate esetén vagy hozzáfűzi, vagy törli és újratölti a removeexisting függvényében
def dataframe_to_mongo(
    df,
    db_name,
    collection,
    host="localhost",
    port=27017,
    username=None,
    password=None,
    removeexisting=True,
    skipifexists=False,
    forceupdate=False,
):
    """ Lement egy DataFrame-t egy MongoDB collection-be """
    db = get_mongo_database(db_name, host, port, username, password)

    if (skipifexists and not forceupdate) and (collection in db.list_collection_names()):
        return

    if (collection in db.list_collection_names()) and removeexisting:
        db[collection].drop()

    records = df.to_dict(orient="records")

    db[collection].insert_many(records)


# egy függvényt hozunk létre, hogy a JSON állományból a Mongo-ra való feltöltést megkönnyítse, és majd a továbbiakban
# az adatbázison keresztül fogjuk elérni az adatunkat


def upload_data_to_mongo_from_path(
    path,
    db_name,
    collection,
    orient="records",
    host="localhost",
    port=27017,
    username=None,
    password=None,
    removeexisting=True,
    skipifexists=False,
    forceupdate=False,
):
    # betöltjük az adatunkat egy DataFrame-be
    data = pd.read_json(path, orient=orient)

    # feltöltjük mongodb-re az adatokat
    dataframe_to_mongo(
        data,
        db_name,
        collection,
        host,
        port,
        username,
        password,
        removeexisting,
        skipifexists,
        forceupdate,
    )


upload_data_to_mongo_from_path(
    "./nobel_prize/nobel_winners/nobel_winners/nwinners.full.json",
    db_name="nobel_prize",
    collection="winners_full",
    removeexisting=True,
    skipifexists=True,
    forceupdate=False,
)

df = mongo_to_dataframe("nobel_prize", "winners_full")

""" print(df.info()) """

""" output:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1136 entries, 0 to 1135
Data columns (total 12 columns):
 #   Column          Non-Null Count  Dtype
---  ------          --------------  -----
 0   link            1136 non-null   object
 1   name            1136 non-null   object
 2   year            1136 non-null   int64
 3   category        1136 non-null   object
 4   country         1136 non-null   object
 5   born_in         1136 non-null   object
 6   text            1136 non-null   object
 7   date_of_birth   1136 non-null   object
 8   date_of_death   1136 non-null   object
 9   place_of_birth  1136 non-null   object
 10  place_of_death  1136 non-null   object
 11  gender          1136 non-null   object
dtypes: int64(1), object(11)
memory usage: 106.6+ KB """

""" print(df.describe()) """

""" output:
              year
count  1136.000000
mean   1971.781690
std      34.344277
min    1809.000000
25%    1950.000000
50%    1978.000000
75%    2000.000000
max    2019.000000 """

""" print(df.describe(include=['object'])) """

""" output:
                                             link                    name                category        country  ... date_of_death place_of_birth place_of_death gender
count                                          1136                    1136                    1136           1136  ...          1136           1136           1136   1136
unique                                          932                    1059                       7             61  ...           623            649            336      2
top     http://en.wikipedia.org/wiki/Charles_K._Kao  Marie Skłodowska-Curie  Physiology or Medicine  United States  ...                New York City                  male
freq                                              4                       4                     271            378  ...           364             35            365   1066 """

""" print(df.tail(10)) """

""" output: 
                                                   link                   name  year                category  ...      date_of_death place_of_birth      place_of_death gender
1131  http://en.wikipedia.org/wiki/Adolfo_P%C3%A9rez...  Adolfo Pérez Esquivel  1980                   Peace  ...                      Buenos Aires                       male
1132  http://en.wikipedia.org/wiki/Luis_Federico_Leloir   Luis Federico Leloir  1970               Chemistry  ...    2 December 1987          Paris  Catamarca Province   male
1133      http://en.wikipedia.org/wiki/Bernardo_Houssay       Bernardo Houssay  1947  Physiology or Medicine  ...  21 September 1971   Buenos Aires        Buenos Aires   male
1134  http://en.wikipedia.org/wiki/Carlos_Saavedra_L...  Carlos Saavedra Lamas  1936                   Peace  ...         5 May 1959   Buenos Aires        Buenos Aires   male
1135         http://en.wikipedia.org/wiki/Brian_Schmidt          Brian Schmidt  2011                 Physics  ...                          Missoula                       male """

""" print(df.head(25)) """

""" print(len(df[df.born_in == ''])) # output: 995 """

""" print(df.columns) """

""" output:
Index(['link', 'name', 'year', 'category', 'country', 'born_in', 'text',
       'date_of_birth', 'date_of_death', 'place_of_birth', 'place_of_death',
       'gender'],
      dtype='object') """

""" df = df.set_index('name')
print(df.head(2)) """

""" output:
                                                           link  year                category  country  ... date_of_death place_of_birth place_of_death  gender
name                                                                                                    ...
Eric Kandel *          http://en.wikipedia.org/wiki/Eric_Kandel  2000  Physiology or Medicine           ...                       Vienna                   male
Elfriede Jelinek  http://en.wikipedia.org/wiki/Elfriede_Jelinek  2004              Literature  Austria  ...                 Mürzzuschlag                 female """

""" df = df.reset_index()
print(df.head(2)) """

""" output:
               name                                           link  year                category  ... date_of_death place_of_birth place_of_death  gender
0     Eric Kandel *       http://en.wikipedia.org/wiki/Eric_Kandel  2000  Physiology or Medicine  ...                       Vienna                   male
1  Elfriede Jelinek  http://en.wikipedia.org/wiki/Elfriede_Jelinek  2004              Literature  ...                 Mürzzuschlag                 female """

""" bi_col = df.born_in
print(bi_col)
print(type(bi_col)) """

""" output: 
0              Austria
1
2
3
4       Czech Republic
             ...
1131
1132
1133
1134
1135
Name: born_in, Length: 1136, dtype: object
<class 'pandas.core.series.Series'> """

""" # elérjük az első sort
print(df.iloc[0]) """

""" output:
link                 http://en.wikipedia.org/wiki/Eric_Kandel
name                                            Eric Kandel *
year                                                     2000
category                               Physiology or Medicine
country
born_in                                               Austria
text              Eric Kandel *, Physiology or Medicine, 2000
date_of_birth                                 7 November 1929
date_of_death
place_of_birth                                         Vienna
place_of_death
gender                                                   male """

""" df.set_index('name', inplace=True)
print(df.loc['Albert Einstein']) """

""" output:
                                                         link  year category      country born_in  ...  date_of_birth  date_of_death place_of_birth place_of_death gender
name                                                                                               ...
Albert Einstein  http://en.wikipedia.org/wiki/Albert_Einstein  1921  Physics  Switzerland          ...  14 March 1879  18 April 1955            Ulm      Princeton   male
Albert Einstein  http://en.wikipedia.org/wiki/Albert_Einstein  1921  Physics      Germany          ...  14 March 1879  18 April 1955            Ulm      Princeton   male """

""" print(df[(df.gender == 'male') & (df.category == 'Literature')]) """

""" output:
                                                   link                 name  year    category  ...      date_of_death place_of_birth place_of_death gender
37    http://en.wikipedia.org/wiki/Czes%C5%82aw_Mi%C...     Czesław Miłosz *  1980  Literature  ...     14 August 2004       Šeteniai         Kraków   male
40          http://en.wikipedia.org/wiki/John_Steinbeck       John Steinbeck  1962  Literature  ...   20 December 1968        Salinas         Harlem   male
60          http://en.wikipedia.org/wiki/Sinclair_Lewis       Sinclair Lewis  1930  Literature  ...    10 January 1951    Sauk Centre           Rome   male
67        http://en.wikipedia.org/wiki/Eugene_O%27Neill       Eugene O'Neill  1936  Literature  ...   27 November 1953  New York City         Boston   male
74        http://en.wikipedia.org/wiki/William_Faulkner     William Faulkner  1949  Literature  ...        6 July 1962     New Albany        Byhalia   male
...                                                 ...                  ...   ...         ...  ...                ...            ...            ...    ...
1077          http://en.wikipedia.org/wiki/Pablo_Neruda         Pablo Neruda  1971  Literature  ...  23 September 1973         Parral       Santiago   male
1085           http://en.wikipedia.org/wiki/Saul_Bellow        Saul Bellow *  1976  Literature  ...       5 April 2005        Lachine      Brookline   male
1097       http://en.wikipedia.org/wiki/Ivo_Andri%C4%87         Ivo Andrić *  1961  Literature  ...      13 March 1975          Dolac       Belgrade   male
1101         http://en.wikipedia.org/wiki/Elias_Canetti      Elias Canetti *  1981  Literature  ...     14 August 1994           Ruse         Zürich   male
1114   http://en.wikipedia.org/wiki/Maurice_Maeterlinck  Maurice Maeterlinck  1911  Literature  ...         6 May 1949          Ghent           Nice   male """

""" # írja ki a 10-edik és 25-ik sor közötti sorokat
print(df[10:25]) """

""" # kiírja azon győztesek számát, akik nők voltak és irodalom kategóriában nyertek
print(df[(df.gender == 'female') & (df.category == 'Literature')].count()) """

""" print(df.born_in.describe()) """

""" output:
count     1136
unique      42
top
freq       995
Name: born_in, dtype: object """

""" print(set(df.born_in.apply(type)))
# output: {<class 'str'>} """

""" bi_col = df.born_in
bi_col.replace('', np.nan, inplace=True)
print(bi_col.describe()) """

""" output:
count         141
unique         41
top       Germany
freq           25 """

""" df.replace("", np.nan, inplace=True) """

""" # azért van szükség az escape-re a csillag előtt, mert ez egy regExp string
print(df[df.name.str.contains('\*')]['name']) """

""" output:
0                Eric Kandel *
4         Bertha von Suttner *
5       Luis Federico Leloir *
14            Yoichiro Nambu *
37            Czesław Miłosz *
                 ...
1098         Vladimir Prelog *
1099           Peter Medawar *
1101           Elias Canetti *
1104          Zhores Alferov *
1122     Elizabeth Blackburn * """

""" df.name = df.name.str.replace("*", "")
df.name = df.name.str.strip() """

""" print(df[df.name.str.contains('\*')]['name'])
# output: üres """

""" df = df[df.born_in.isnull()] """
""" print(df.count()) """

""" output:
link              995
name              995
year              995
category          995
country           995
born_in             0
text              995
date_of_birth     995
date_of_death     675
place_of_birth    995
place_of_death    674
gender            995 """

# az axis=0 sort jelöl, az axis=1 oszlopot jelöl
""" df = df.drop("born_in", axis=1) """

""" # megkeresi a name oszlopban az egyező sorokat
dupes_by_name = df[df.duplicated('name')]
print(dupes_by_name.count())
# output: 70 ... """

""" all_dupes = df[df.duplicated("name", keep=False)] """
""" print(all_dupes.head()) """
# output: 136 ...

""" dupes_by_name = df[df.duplicated('name')]
all_dupes = df[df.name.isin(dupes_by_name.name)]
print(all_dupes.count())
# output: 136 """

""" for name, rows in df.groupby('name'):
    print('name: {}, number of rows: {}'.format(name, len(rows))) """

""" tmp = pd.concat([g for _, g in df.groupby('name') if len(g) > 1])
print(tmp['name']) """

""" output:
19             Alan MacDiarmid
708            Alan MacDiarmid
559            Albert Einstein
812            Albert Einstein
406               Angus Deaton
                 ...
1017    William Lawrence Bragg
643          Władysław Reymont
675          Władysław Reymont
222                Yuan T. Lee
567                Yuan T. Lee """

""" df2 = pd.DataFrame({'name': ['zak', 'alice', 'bob', 'mike', 'bob', 'bob'],
    'score': [4, 3, 5, 2, 3, 7]})

# a megadott DataFrame-t két oszlop szerint rendezi, előszöris a név oszlop szerint, amennyiben annak az értéke megegyezik,
# utána csökkenő sorrendben a pontuk alapján rendezi
print(df2.sort_values(['name', 'score'], ascending=[1, 0])) """

""" print(all_dupes.sort_values('name')[['name', 'country', 'year']]) """

""" output: 
                        name                  country  year
708          Alan MacDiarmid              New Zealand  2000
19           Alan MacDiarmid            United States  2000
812          Albert Einstein                  Germany  1921
559          Albert Einstein              Switzerland  1921
538             Angus Deaton           United Kingdom  2015
...                      ...                      ...   ...
1017  William Lawrence Bragg                Australia  1915
675        Władysław Reymont                   Poland  1924
643        Władysław Reymont  Russia and Soviet Union  1924
567              Yuan T. Lee                   Taiwan  1986
222              Yuan T. Lee            United States  1986 """

""" all_dupes.sort_values('name', inplace=True)
all_dupes.set_index('name', inplace=True)
print(all_dupes.loc['Marie Curie']) """

""" df['country'][708] = 'United States' """

""" output:
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  df['country'][708] = 'United States' """

""" print(df['country'][708])
# output: United States """

""" df.loc[708, 'country'] = 'United States'

print(df.loc[708]) """

""" df.loc[(df.name == 'Alan MacDiarmid') & (df.year == 2000), 'country'] = 'United States'
print(df.loc[(df.name == 'Alan MacDiarmid') & (df.year == 2000), 'country']) # output: United States (kétszer) """

""" df.drop(df[(df.name == 'Alan MacDiarmid') & (df.year == 2000)].index, inplace=True)
# azonban kitörli az összes olyan sort, amelyben a fenti mask teljesül """

""" df = df[~((df.name == 'Alan MacDiarmid') & (df.year == 2000))]
# ebben az esetben is kitörli az összeset """

# Marie Curie-nél problémába ütközünk a metódussal, hiszen név szerint töröltük
# találnunk kell egy relevánsabb oszlopot
""" df.drop_duplicates('name', inplace=True)
print(df[df.name == 'Marie Curie']) """

# ha nem határozunk meg oszlopot, abban az esetben az összes alapján fog duplikátumot keresni,
# ebben az esetben jól hagyja meg Curie-t, azonban MacDiarmid-et nem törli, hiszen a bejegyzésekben van eltérés, az országnál
""" df.drop_duplicates(inplace=True)
print(df[df.name == 'Marie Curie'])
print(df[df.name == 'Alan MacDiarmid']) """

# ebben az esetben már űgy tünik sikeres a duplikátum törlés, hiszen Curie megmaradt, MacDiarmid pedig törlődött
""" df.drop_duplicates(['name', 'year'], inplace=True)
print(df[df.name == 'Marie Curie'])
print(df[df.name == 'Alan MacDiarmid']) """

""" df.drop(df[(df.name == u'Marie Sk\u0142odowska-Curie')].index, inplace=True) """

# minden rendben van, kivéve, hogy most vehettük észre, hogy két Curie-nk van, a második felesleges tehát azt is törölhetjük
""" print(df[df.duplicated('name', keep=False)].sort_values('name')[['name', 'country', 'year']]) """

""" df = df.reindex(np.random.permutation(df.index)) """






def clean_data(df):
    # első lépésben, az összes üres értéket NaN-ra állítjuk, hogy a Pandas a statisztikák során nem számolja
    df = df.replace("", np.nan)
    # kiegészítő lépésekben töröljük a csillagokat és a felesleges space-t a nevekből
    df.name = df.name.str.replace("*", "")
    df.name = df.name.str.strip()

    # létrehoz egy új DataFrame-t azokkal a sorokkal, ahol valid born_in mező van
    df_born_in = df[df.born_in.notnull()]
    # második lépésben, az összes olyan sort töröljük a DataFrame-ből, amelynél a born_in nem volt üres, azaz nem volt NaN
    df = df[df.born_in.isnull()]

    # harmadik lépésben, töröljük a born_in oszlopot, hiszen nem releváns, nincs egy olyan sor sem, amely értéket tárolna ott
    df = df.drop("born_in", axis=1)
    df = df.reindex(np.random.permutation(df.index))

    # negyedik lépésben töröljük a duplikátumokat, két releváns szempont szerint, ami elsőként a név, majd az év,
    # azokat törli, ahol mindkettő megegyezik, így elkerülve azt, hogy olyant töröljünk aki kétszert nyert
    df = df.drop_duplicates(['name', 'year'])

    # töröljük a duplikátum lengyel karakteres Curie-t
    # rendezzük az objektumokat indexük szerint
    df = df.sort_index()

    df = df.drop(df[(df.name == u'Marie Sk\u0142odowska-Curie')].index)
    # töröljük a rossz dátummal felírt Ragnar Granit-ot is
    df = df.drop(df[(df.name == 'Ragnar Granit') & (df.year == 1809)].index)
    # javítjuk az elhibázott 1809-es dátumokat
    df.loc[(df.name == 'Artturi Ilmari Virtanen') & (df.year == 1809), 'year'] = 1945
    df.loc[(df.name == u'Frans Eemil Sillanp\u00E4\u00E4') & (df.year == 1809), 'year'] = 1939
    # töröljük Horst L. Störmer-t is, hiszen kétszer jelenik meg, kétféleképpen írt névvel
    df = df.drop(df[(df.name == u'Horst L. Störmer') & (df.year == 1998)].index)
    # javítjuk Henderson hamis elhalálozási dátumát
    df.loc[(df.name == 'Richard Henderson') & (df.year == 2017), 'date_of_death'] = np.nan;

    # átalakítjuk datetime64 objektummá az időoszlopainkat
    df.date_of_birth = pd.to_datetime(df.date_of_birth)
    df.date_of_death = pd.to_datetime(df.date_of_death)

    # a MongoDB-n való tárolás miatt vissza kell alakítani object-é az oszlopot, és NaN-ra állítani a NaT-okat,
    # mert másképp nem engedi feltölteni, ValueError miatt
    df.date_of_death = df.date_of_death.astype(object).where(df.date_of_death.notnull(), np.nan)

    # kiszámoljuk minden győztes esetén az életkorukat, amikor megkapták a díjat,
    # használjuk a DateTimeIndex metódust, hogy jelezzük a Pandas-nak dátummal dolgozunk
    df['award_age'] = df.year - pd.DatetimeIndex(df.date_of_birth).year

    return df, df_born_in

df, df_born_in = clean_data(df)

# feltöltsük az adatbázisba
dataframe_to_mongo(df, 'nobel_prize', 'winners_cleaned', removeexisting=True, skipifexists=True)
dataframe_to_mongo(df_born_in, 'nobel_prize', 'winners_born_in', removeexisting=True, skipifexists=True)




""" # rendezzük az objektumokat indexük szerint
df = df.sort_index() """

""" # javítjuk Henderson hamis elhalálozási dátumát
df.loc[(df.name == 'Richard Henderson') & (df.year == 2017), 'date_of_death'] = np.nan; """

""" # átalakítjuk datetime64 objektummá az időoszlopainkat
df.date_of_birth = pd.to_datetime(df.date_of_birth, errors='coerce')
df.date_of_death = pd.to_datetime(df.date_of_death, errors='coerce') """

""" # kiszámoljuk minden győztes esetén az életkorukat, amikor megkapták a díjat,
# használjuk a DateTimeIndex metódust, hogy jelezzük a Pandas-nak dátummal dolgozunk
df['award_age'] = df.year - pd.DatetimeIndex(df.date_of_birth).year """

""" print(df.sort_values('award_age').iloc[:10][['name', 'award_age', 'category', 'year']]) """

""" output:
                        name  award_age                category  year
702         Malala Yousafzai         17                   Peace  2014
1017  William Lawrence Bragg         25                 Physics  1915
754              Nadia Murad         25                   Peace  2018
521     Georges J. F. Köhler         30  Physiology or Medicine  1976
131            Tsung-Dao Lee         31                 Physics  1957
443               Paul Dirac         31                 Physics  1933
885   Werner Karl Heisenberg         31                 Physics  1932
86             Carl Anderson         31                 Physics  1936
905         Rudolf Mössbauer         32                 Physics  1961
49           Tawakkol Karman         32                   Peace  2011 """

""" df_dupes_by_link = df[df.duplicated('link', keep=False)]
print(df_dupes_by_link) """

""" output:
                                                  link                  name  year   category  ...     date_of_death     place_of_birth place_of_death  gender
41          http://en.wikipedia.org/wiki/Linus_Pauling      Linus C. Pauling  1962      Peace  ...    18 August 1994           Portland        Big Sur    male
99          http://en.wikipedia.org/wiki/Linus_Pauling      Linus C. Pauling  1954  Chemistry  ...    18 August 1994           Portland        Big Sur    male
102          http://en.wikipedia.org/wiki/John_Bardeen          John Bardeen  1956    Physics  ...   30 January 1991            Madison         Boston    male
156          http://en.wikipedia.org/wiki/John_Bardeen          John Bardeen  1972    Physics  ...   30 January 1991            Madison         Boston    male
289  http://en.wikipedia.org/wiki/Horst_Ludwig_St%C...  Horst Ludwig Störmer  1998    Physics  ...               NaN  Frankfurt am Main            NaN    male
467      http://en.wikipedia.org/wiki/Frederick_Sanger      Frederick Sanger  1958  Chemistry  ...  19 November 2013           Rendcomb      Cambridge    male
514      http://en.wikipedia.org/wiki/Frederick_Sanger      Frederick Sanger  1980  Chemistry  ...  19 November 2013           Rendcomb      Cambridge    male
955  http://en.wikipedia.org/wiki/Horst_Ludwig_St%C...      Horst L. Störmer  1998    Physics  ...               NaN  Frankfurt am Main            NaN    male
958           http://en.wikipedia.org/wiki/Marie_Curie           Marie Curie  1903    Physics  ...       4 July 1934             Warsaw    Sancellemoz  female
970           http://en.wikipedia.org/wiki/Marie_Curie           Marie Curie  1911  Chemistry  ...       4 July 1934             Warsaw    Sancellemoz  female """

""" print(df.count()) """

""" output:
link              927
name              927
year              927
category          927
country           927
text              927
date_of_birth     927
date_of_death     634
place_of_birth    927
place_of_death    633 # hiányzó érték
gender            927 

# minden oszlopnál helyben vagyunk, kivétel ez alól a place_of_death oszlop, aholis egy érték hiányzik
"""

""" print(df.gender) """

""" print(df[(df.place_of_death.isnull()) & (~(df.date_of_death.isnull()))]) """

""" # alapértelmezetten az errors paraméter ignore-dra van állítva, jelen esetben azt akarjuk, hogy ezeket mutassa ki
print(pd.to_datetime(df.date_of_birth, errors='raise')) """

""" output:
1      1946-10-20
2      1940-10-15
3      1944-01-06
6      1887-02-05
7      1929-01-30
          ...
1131   1931-11-26
1132   1906-09-06
1133   1887-04-10
1134   1878-11-01
1135   1967-02-24 """