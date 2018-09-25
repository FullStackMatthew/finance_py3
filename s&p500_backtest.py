#Import all required libraries for program:

import sqlite3
import csv
import pandas as pd
import matplotlib.pyplot as plt
import datetime 


#We download directly from yahoo.com, five years of historical daily data for the spy (S&P 500 etf).

df  = pd.read_csv("C:/Users/mzecchini1989/Downloads/SPY.csv")


#Now we have to convert our Datestamp column in the csv so python can now parse in a native format. 
# %Y - year including the century
# %m - month (01 to 12)
# %d - day of the month (01 to 31)
#YES THE ORDER MATTERS!!!

df['Datestamp']=pd.to_datetime(df['Datestamp'], format="%m/%d/%Y")

#Open the csv data file in read mode 'r'.

f=open('C:/Users/mzecchini1989/Downloads/SPY.csv','r') 

#We create a reader object for python to manipulate the data within the csv file we created. 

reader = csv.reader(f)

#Next we establish a connection to a brand new database (local) using sqlite3.

sql = sqlite3.connect('spy.db')

#Our new variable 'cur' will let python know exactly where to position new arguments and logic.

cur = sql.cursor()

#Once we've made a connection to a new database, time to populate it with the columns we intend on inserting with data from our csv file.
#As you may have noticed the "IF NOT EXISTS" SQL command makes sure not to overwrite data in the case that it already exists.
#When setting up a SQL database it's good practice to specify the data type that will be accepted in each field. "INT" = Integer format.

cur.execute('''CREATE TABLE IF NOT EXISTS spy
            (Datestamp INT, Open INT, High INT, Low INT, Close INT, Volume INT)''') 

#Using a simple for loop we can interate over each column, the "?" is a temporary placeholder for sqlite3. 
                         
for row in reader:
        cur.execute("INSERT INTO spy VALUES (?, ?, ?, ?, ?, ?)", row)
        
#To make sure our database is properly outputting the data, it's always a good idea to print.
#The "*" SQL command allows us to select the entire database instead of individually selecting each item we want to print.

for row in cur.execute('SELECT * FROM spy'):
        print(row)

#Many times when manipulating large data sets graphing the data is an excellent way to establish relationships mathmatically.
#Here we use our matplotlib library to plot a line graph. 

df.plot(kind='line',x='Datestamp',y='Close', color='m')

#Setting up proper x axis and y axis labeling

plt.xlabel("Time")
plt.ylabel("Closing Price")
plt.title("SPY performance 5 YEARS")
plt.show()

#Finally we close both connections to the csv file and the SQL database.
#The commit() function MUST be called in order to execute any changes that are made at the end of a program or nothing will happen. 

f.close()
sql.commit()
sql.close()