<img width="1183" height="784" alt="app ss" src="https://github.com/user-attachments/assets/789e35ce-ca14-4f4f-9822-7d9d20731921" />

Crypto Price Tracker is an interactive cryptocurrency analytics dashboard built with Python and Streamlit. The application integrates the CoinGecko public API to fetch real-time and historical market data and visualizes price movements using Plotly. The project focuses on clean UI design, efficient data handling, and the implementation of basic technical analysis indicators.

The application allows users to select from the top 20 cryptocurrencies by market capitalization or manually enter a coin . Users can analyze price performance across multiple time ranges including 1 day, 7 days, 1 month, and 1 year. Historical price data is processed using Pandas and displayed through interactive line charts.

For deeper financial analysis, the dashboard includes two technical indicators: the 20-period Moving Average (MA20) and the 50-period Moving Average (MA50). These indicators are calculated using true rolling window logic to ensure accuracy, and users can dynamically enable or disable them through toggle controls.

To improve performance and reduce unnecessary API calls, the project uses Streamlit’s caching mechanism. Session state management is implemented to control time range selection and maintain a responsive user interface. Basic error handling is also included to manage invalid coin IDs and potential API rate limits.

To run the project clone the repository, install the required dependencies using pip, and start the application with the command "streamlit run app.py". This project demonstrates practical experience in REST API integration, data transformation, financial indicator implementation, and interactive dashboard development.
Author:Ece Koçak
