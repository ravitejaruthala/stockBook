import streamlit as st
import pandas as pd
import plotly.express as px

dataURL = "Data.csv"
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
st.header("Stock Summary")
symbols = st.multiselect("Choose a particular stock to visualize", sorted(df["stockSymbol"].unique()))
space(1)



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

def realized_gain_or_loss(df) :
    years_list = df['transactionYear'].unique().tolist()
    for year in years_list :
        total_gain_or_loss = 0
        df_to_consider = df[df['transactionYear']== year]
        sell_transactions = df_to_consider[df_to_consider['transactionType'] == 'Sell']
        if sell_transactions.empty :
            st.write("**Realized Gain till date:** No Sell Transactions in ", year)
        else :
            stocks_list = sell_transactions['stockSymbol'].unique().tolist()
            for stock in stocks_list :
                filter_by_stock = df_to_consider[df_to_consider['stockSymbol']== stock]
                buy_transactions = filter_by_stock[filter_by_stock['transactionType']== 'Buy']
                Total_investment_in_year = buy_transactions['stockInvestment'].sum()
                sell_transactions_in_year = sell_transactions[sell_transactions['stockSymbol'] == stock]
                total_sell_in_year = sell_transactions_in_year['stockInvestment'].sum()
                total_gain_or_loss += total_sell_in_year - Total_investment_in_year
                st.write('Company Name : ', stock, '   |   Year : ' , year)
                st.write("Gain/Loss : ")
                st.metric(label='INR',
					value=(total_sell_in_year - Total_investment_in_year),
					delta = ((total_sell_in_year - Total_investment_in_year)/Total_investment_in_year)*100)
                st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        st.write("Year : ", year, "Total Returns : ", total_gain_or_loss )
                     

if __name__ == '__main__' :
    stockInfo(symbols)
    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    st.header("Gain Summary")
    realized_gain_or_loss(df)