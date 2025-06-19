import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("mymoviedb.csv", lineterminator = "\n")
print(df.head())  # Shows the first 5 rows to confirm it's loaded

df.info()

print(df['Genre'].head())

print(df.duplicated().sum())#checking for duplicate movies/data

print(df.describe())

"""
Summary :-

> we have a  dataframe consisting of 9827 rows and columns.
> our dataset looks a bit tidy with no NaNs nor duplicated values.
> Release_Date column needs to be casted into date time and to extract only the year value.
> Overview, Original_Language and Poster URL wouldn't be so useful during analysis,so we'll drop them.
> there is noticable outliers in popularity column.
> Vote_Average better be categorised for proper analysis.
> Genre column has comma saperated values and white spaces that need to be handled and casted into category.

"""
#covert Release_Date datatype object to datetime formate
df['Release_Date'] = pd.to_datetime(df['Release_Date'])
print(df['Release_Date'].dtype)

#we need only year so we convert it into only year
#now only  showing year
df['Release_Date'] = df['Release_Date'].dt.year
print(df['Release_Date'].dtype)
print(df.head())


#Dropping the columns that not needed
cols = ['Overview','Original_Language','Poster_Url']
df.drop(cols,axis=1,inplace=True)
print(df.columns) #looking columns
print(df.head())

"""
We are Categorizing Vote_Average columns:=
       We would cut the Vote_Average values and make 4 categories:
        popular, average, below_avg, not_popular to describe it more using
        categorize_col() function provided above.
"""

def catigorize_col(df,col,labels):       #user-define-function 
    edges = [df[col].describe()['min'],
             df[col].describe()['25%'],
             df[col].describe()['50%'],
             df[col].describe()['75%'],
             df[col].describe()['max']]
    
    #cut  is useful for categorization
    df[col] = pd.cut(df[col], edges, labels = labels, duplicates = 'drop')
    return df

labels = ['not_popular', 'below_avg', 'average', 'popular']

#calling function
catigorize_col(df,'Vote_Average', labels)

print(df['Vote_Average'].unique())
print(df.head())

#checking movies how much scores  popular,average,below_avg and  not  popular
print(df['Vote_Average'].value_counts())

#removing NaN, Duplicates values  from  rows
print(df.dropna(inplace=True))

#checking NaN  values Remove or Not
print(df.isna().sum())

print(df.head())

"""
We'd split genres into list and then explode our dataframe to have
only one genre per row  each movie
"""

df['Genre'] = df['Genre'].str.split(', ')#split , and space in genre
df = df.explode('Genre').reset_index(drop=True)#in genre every data having in new row
print(df.head())

#Casting Genre column into category 
df ['Genre'] = df['Genre'].astype('category') #.astype helps  to convert any column into category

print(df['Genre'].dtypes)

print(df.info())

print(df.nunique()) #checking how mach unique values have

print(df.head())

# **Data Visualization**

sns.set_style('whitegrid')  #visualization look good

# Q1: What is most frequent genre of movies released  on Netflix?

print(df['Genre'].describe())

#Creating charts for showing  Genre Category
sns.catplot(y = 'Genre', data = df, kind='count', order=df['Genre'].value_counts
            ().index, color ='blue')
plt.title('Genre Column Distribution')
plt.savefig('Genre Category Chart.png', dpi=300, bbox_inches='tight')
plt.show()


# Q2: Which has highest votes in vote avg column

sns.catplot(y = 'Vote_Average', data  = df, kind='count', order=df['Vote_Average'].value_counts
            ().index , color='red' )
plt.title('Vote_Average Distribution')
plt.savefig('Highest Vote in Vote Average.png', dpi=300, bbox_inches='tight')
plt.show()


# Q3: What movie got the highest popularity? what's its genre?

print(df.head())

#showing how is the most popular movie with genre
print(df[df['Popularity'] == df['Popularity'].max()])


# Q4: What movie got the lowest popularity? what's its genre?

print(df[df['Popularity'] == df['Popularity'].min()])


# Q5: Which year  has the most filmmed movies?

df['Release_Date'].hist()
plt.title('Release Date Column Distribution')
plt.savefig('Most Filmmed Movies Year.png', dpi=300, bbox_inches='tight')
plt.show()


"""
*CONCLUSION*:-
 > Q1 : What is most frequent genre of movies released  on Netflix?
 Drama Genre is the most frequent genre in our dataset and has appeared more than 14%
 of the times among  19  other genre.

 > Q2 : Which has highest votes in vote avg column
 we have  25.5% of our dataset with  popular vote (6520 rows). Drama again gets the 
 highest popularity among  fans by being having more than 18.5% movies popularity

 > Q3 : What movie got the highest popularity? what's its genre?
 Spider-Man: No  Way Home has the highest popularity rate in our dataset and its has genre 
 of Action, Adventure and Science Fiction.

 > Q4 : What movie got the lowest popularity? what's its genre?
 The united states, thread has the lowest rate in our dataset and it has genre pf music,
 drama, war, scince  fiction and History..

 > Q5 : Which year  has the most filmmed movies?
 Year 2020 has the highest filming rate in our dataset.
 
"""

