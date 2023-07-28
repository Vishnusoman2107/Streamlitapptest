import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


# Function to get S&P 500 stock symbols
def get_sp500_symbols():
    data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    table = data[0]
    return table['Symbol'].tolist()


# Function to get Nifty stock symbols
def get_nifty_symbols():
    # Replace 'raw_url_of_your_excel_file' with the actual raw URL of your Excel file on GitHub
    excel_url = 'https://github.com/Vishnusoman2107/Streamlitapptest/blob/4b12da88a809bbf2f8d8e3ee65e936153898cd8b/Book2.xlsx'
    exceldata = pd.read_excel(excel_url)
    # Assuming 'Symbol' is the column name you want to access
    symbol_column = exceldata['Symbol']
    # Add '.NS' to all symbols in the 'Symbol' column
    symbol_column = symbol_column.apply(lambda symbol: symbol + '.NS')
    return symbol_column


# Function to fetch income statement and metrics for S&P 500 stocks
def get_company_info(ticker):
    company = yf.Ticker(ticker)
    info = company.info
    income_statement = company.get_income_stmt()
    metric = company.get_cash_flow()

    income_statement = income_statement.loc[
        ['TotalRevenue', 'CostOfRevenue', 'EBIT', 'NetIncome', 'DilutedAverageShares',
         'NetIncomeFromContinuingOperationNetMinorityInterest', 'NetIncomeCommonStockholders',
         'NetIncomeIncludingNoncontrollingInterests', 'DilutedEPS']]
    metric = metric.loc[['CashFlowFromContinuingFinancingActivities', 'CashFlowFromContinuingInvestingActivities',
                         'CashFlowFromContinuingOperatingActivities', 'FreeCashFlow']]

    return info, income_statement, metric


# Function to fetch income statement and metrics for Nifty stocks
def get_nifty_info(ticker):
    company = yf.Ticker(ticker)
    info = company.info
    income_statement = company.get_income_stmt()
    metric = company.get_cash_flow()

    income_statement = income_statement.loc[['TotalRevenue', 'NetIncome', 'DilutedAverageShares', 'NetIncomeFromContinuingOperationNetMinorityInterest','NetIncomeCommonStockholders', 'NetIncomeIncludingNoncontrollingInterests', 'DilutedEPS']]
    metric = metric.loc[['FinancingCashFlow','InvestingCashFlow','OperatingCashFlow','FreeCashFlow']]

    return info, income_statement, metric


# Main Streamlit app code
def main():
    st.title('Stock Dashboard')

    # Sidebar to select the stock index and ticker symbol
    stock_index = st.sidebar.radio('Select Stock Index', ['S&P 500', 'Nifty'])

    if stock_index == 'S&P 500':
        stock_symbols = get_sp500_symbols()
    else:
        stock_symbols = get_nifty_symbols()

    ticker = st.sidebar.selectbox('Select Ticker', stock_symbols)

    # Input for start date and end date
    start_date = st.sidebar.text_input('Start Date (dd/mm/yyyy)')
    end_date = st.sidebar.text_input('End Date (dd/mm/yyyy)')

    # Convert date format to yyyy-mm-dd for yfinance
    try:
        start_date = pd.to_datetime(start_date, format='%d/%m/%Y').strftime('%Y-%m-%d')
        end_date = pd.to_datetime(end_date, format='%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        st.sidebar.error('Invalid date format. Use dd/mm/yyyy.')

    if start_date and end_date:
        # Fetch historical stock price data using yfinance
        df = yf.download(ticker, start=start_date, end=end_date)

        # Plotting the stock price data using plotly
        if not df.empty:
            st.write(f"## Historical Stock Prices for {ticker}")
            fig = px.line(df, x=df.index, y='Close', title=f'{ticker} Close Price')
            fig.update_xaxes(title='Date')
            fig.update_yaxes(title='Close Price')
            st.plotly_chart(fig)
        else:
            st.sidebar.warning('No data available for the selected date range.')

        # Fetch and display company information
        if stock_index == 'S&P 500':
            info, income_statement, metric = get_company_info(ticker)
        else:
            info, income_statement, metric = get_nifty_info(ticker)

        st.write(f"## {info['longName']} ({ticker})")
        st.write(f"**Sector:** {info['sector']}")
        st.write(f"**Industry:** {info['industry']}")
        st.write(f"**Market Cap:** {info['marketCap']}")

        st.write("## Income Statement")
        st.write(income_statement)

        st.write("## Metrics")
        st.write(metric)


if __name__ == '__main__':
    main()
