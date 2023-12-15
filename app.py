from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/exchange-rate-history/usd-idr')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find(class_="history-rates-data")
history = table.find_all('span', class_='n')

row_length = len(history)

temp = [] #initiating a list 

for i in range(1, row_length):

   #scrapping process

    #get date
    date = table.find_all('a', class_='n')[i].text
    #get rate
    rate = table.find_all('span', class_='n')[i].text[7:]
    rate = rate.replace(',','')

    temp.append((date,rate))

#change into dataframe
data = pd.DataFrame(temp, columns= ['Date','Rate'])

#insert data wrangling here
data['Date'] = data['Date'].astype('datetime64[ns]')
data['Rate'] = data['Rate'].astype('int64')
data = data.set_index('Date')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["Rate"][0]}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(figsize = (10,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)