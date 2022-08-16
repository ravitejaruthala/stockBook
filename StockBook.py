import streamlit as st
import pandas as pd
import plotly.express as px

#To add empty lines to the app.
def space(num_lines=1):
    for _ in range(num_lines):
        st.write("")

def stockInfo(selectedList):
	for stock in selectedList:
		st.write('**Stock Name:**',stock)
		stockDF = df[df['stockSymbol']==stock]
		buyStockDF = stockDF[stockDF['transactionType']=='Buy']
		sellStockDF = stockDF[stockDF['transactionType']=='Sell']
		holdingQty = buyStockDF['stockQuantity'].sum() - sellStockDF['stockQuantity'].sum()
		st.write('**Stocks purchased till date:**', buyStockDF['stockQuantity'].sum())
		st.write('**Stocks holding till date:**', holdingQty)
		if holdingQty:
			st.write("**Return till date:** *No return till date.*")
		else:	
			st.write("**Return on investment:**")
			st.metric(label='INR',
					value=(sellStockDF['stockInvestment'].sum()- buyStockDF['stockInvestment'].sum()),
					delta = ((sellStockDF['stockInvestment'].sum() - buyStockDF['stockInvestment'].sum())/buyStockDF['stockInvestment'].sum())*100)
		space(2)
st.set_page_config(layout="centered", page_title="StockBook")
st.title("StockBook")
st.write("This application helps you to track your investments.")
st.write('''We recommend you to use a specific format to track your portfolio. To start, you can download the sample file below. 
			Or, if you already using one, please upload your file.''')
st.download_button('Download your free sample', data="sample.csv", file_name='sample.csv')
uploaded_file = st.file_uploader('Upload your file here!!', type=['csv'], accept_multiple_files=False)
if uploaded_file is not None:
	data = pd.read_csv(uploaded_file)
	df = pd.DataFrame(data)
	#st.write(df)
	st.header("Portfolio Summary")
	portfolioSummary = px.pie(df, values='stockInvestment', names='stockSymbol')
	st.write(portfolioSummary)
	st.write('Need a pandas query that can retrive holding shares - Better to maintain a dict with share name and share quantity')
	space(3)
	st.header("Stock Summary")
	symbols = st.multiselect("Choose a particular stock to retrive its summary", sorted(df["stockSymbol"].unique()))
	space(1)
	stockInfo(symbols)
	st.header("Return statement")
	st.write('A table that provides profit (descending) and loss (ascending')
	st.header("Investment summary")
	st.write('A statement that provides overview on investments')
else:
	st.write("You need to upload a file to track.")
