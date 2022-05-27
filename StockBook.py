import streamlit as st
import pandas as pd
import plotly.express as px

dataURL = "/home/boss/Bombarding/projects/stockBook - Streamlit/Data.csv"
data = pd.read_csv(dataURL)
df = pd.DataFrame(data)
#stockSymbol transactionType	transactionDate	stockQuantity	stockPrice	stockInvestment	userComments
st.set_page_config(layout="centered", page_title="StockBook")
st.title("StockBook")
st.write("This application helps you to track your investments.")
st.write(df)


#To add empty lines to the app.
def space(num_lines=1):
    for _ in range(num_lines):
        st.write("")

st.header("Portfolio Summary")

space(3)

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
			st.write("**Return till date:**")
			st.metric(label='INR',
					value=(sellStockDF['stockInvestment'].sum()- buyStockDF['stockInvestment'].sum()),
					delta = ((sellStockDF['stockInvestment'].sum() - buyStockDF['stockInvestment'].sum())/buyStockDF['stockInvestment'].sum())*100)
		space(2)
st.header("Stock Summary")
symbols = st.multiselect("Choose a particular stock to visualize", sorted(df["stockSymbol"].unique()))
space(1)
stockInfo(symbols)






