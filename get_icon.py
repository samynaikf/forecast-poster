
def get_icon(package_name):
	dict = {

	'Low Price High Volume Stocks': '<img class="wp-image-93440 alignright" src="https://iknowfirst.com/wp-content/uploads/2017/01/high-volume-stock1-Recovered-3.jpg" alt="" width="143" height="103"/>',

	'High Volume Stocks': '<img class="alignright wp-image-37906" src="https://iknowfirst.com/wp-content/uploads/2017/01/High-Volume-Stocks.jpg" alt="Best Share To Buy" width="123" height="67" />',

	'52 Week High Stocks': '<img class="alignright wp-image-37906" src="https://iknowfirst.com/wp-content/uploads/2016/05/52-week-high-icon.jpg" alt="Best Share To Buy" width="189" height="62" />',

	'52 Week Low Stocks': '<img class="alignright wp-image-36921" src="https://iknowfirst.com/wp-content/uploads/2016/05/52-Week-Low-Stocks.png" alt="52 Week Low Stocks" width="165" height="54" />',

	'Aggressive Stocks Forecast': '<img class="wp-image-36402 alignright" src="https://iknowfirst.com/wp-content/uploads/2016/11/Risk-Conscious-stocks-300x98.jpg" alt="" width="165" height="54" />',

	'Bank Stock Forecast': '<img class="alignright wp-image-37648" src="https://iknowfirst.com/wp-content/uploads/2016/05/Bank-Stock-Forecast.png" alt="Bank Stock Forecast" width="165" height="54" />',

	'Basic Industry Forecast': '<img class="alignright wp-image-36397" src="https://iknowfirst.com/wp-content/uploads/2016/05/basic-industry-300x98.png" alt="Stock Market Prediction Algorithm" width="165" height="54" />',

	'Biotech Stocks Forecast': '<img class="alignright wp-image-36839" src="https://iknowfirst.com/wp-content/uploads/2016/05/biotech.png" alt="BioTech Stocks" width="162" height="53" />',

	'Bitcoin': '<img class="alignright wp-image-36839" src="https://iknowfirst.com/wp-content/uploads/2016/05/biotech.png" alt="BioTech Stocks" width="162" height="53" />',

	'Bovespa': '<img class="alignright wp-image-36928" src="https://iknowfirst.com/wp-content/uploads/2016/05/Brazil-Stock-Forecast-.png" width="144" height="47" />',

	'Brazil Stock Forecast': '<img class="alignright wp-image-36928" src="https://iknowfirst.com/wp-content/uploads/2016/05/Brazil-Stock-Forecast-.png" width="144" height="47" />',

	'Canadian Stock Forecast': '<img class="alignright wp-image-36398" src="https://iknowfirst.com/wp-content/uploads/2016/05/canadian-stocks-300x98.png" alt="" width="165" height="54" />',

	'Chemicals Stocks': '<img class="alignright wp-image-39238" src="https://iknowfirst.com/wp-content/uploads/2016/06/chemical-300x98.jpg" alt="Chemical Stock Forecast" width="165" height="54" />',

	'Computer Industry': '<img class=" wp-image-37897 alignright" src="https://iknowfirst.com/wp-content/uploads/2016/05/Computer-Industry-1.png" alt=Computer Industry" width="168" height="55" />',

	'Conservative Stock Forecast': '<img class="alignright wp-image-36402" src="https://iknowfirst.com/wp-content/uploads/2016/05/Risk-Conscious-stocks.png" alt="Risk Conscious stocks" width="165" height="54" />',

	'Consumer Stocks': '<img class="size-full wp-image-36334 alignright" src="https://iknowfirst.com/wp-content/uploads/2016/05/curency-165.jpg" alt="curency 165" width="165" height="54" />',

	'Dividend Stocks Forecast': '<img class="alignright wp-image-36399" src="https://iknowfirst.com/wp-content/uploads/2016/05/dividend-stocks-.png" alt="dividend stocks" width="165" height="54" />',

	'Energy Stocks Forecast': '<img class="wp-image-41851 size-full alignright" src="https://iknowfirst.com/wp-content/uploads/2016/07/Energy_small.jpg" width="205" height="67" />',

	'European Stock Forecast': '<img class="alignright wp-image-37481" src="https://iknowfirst.com/wp-content/uploads/2016/05/European-Stock-Forecast-1.png" alt="European Stock Forecast" width="165" height="54" />',

	'Fundamental': '<img class="alignright wp-image-37320" src="https://iknowfirst.com/wp-content/uploads/2016/05/fundamentals.jpg" alt="fundamentals" width="165" height="54" />',

	'Gold & Commodity Forecast': '<img class="alignright wp-image-38329" src="https://iknowfirst.com/wp-content/uploads/2016/05/gold-300x98.png" alt="Gold Forecast" width="165" height="54" />',

	'Healthcare': '<img class="alignright wp-image-38329" src="https://iknowfirst.com/wp-content/uploads/2016/06/Healthcare.png" alt="Healthcare" width="165" height="54" />',

	'Hedge Fund Stocks': '<img class=" wp-image-37919 alignright" src="https://iknowfirst.com/wp-content/uploads/2016/05/hedgefunds.png" alt="hedgefunds" width="165" height="54" />',

	'Options': '<img class="alignright wp-image-38089" src="https://iknowfirst.com/wp-content/uploads/2016/06/Options-.png" alt="Options" width="186" height="61" />',

	'Indices Forecast': '<img class="alignright wp-image-36936" src="https://iknowfirst.com/wp-content/uploads/2016/05/Indices-Forecast.png" alt="Indices Forecast" width="165" height="54" />',

	'Insider Trades': '<img class="alignright wp-image-36855" src="https://iknowfirst.com/wp-content/uploads/2016/05/Insider-Trading.png" alt="insider trading" width="165" height="54" />',

	'Insurance Companies Forecast': '<img class="alignright wp-image-36918" src="https://iknowfirst.com/wp-content/uploads/2016/05/Insurance-Companies.png" alt="insurance" width="165" height="54" />',

	'Israeli Stocks': '<img class="alignright wp-image-38544" src="https://iknowfirst.com/wp-content/uploads/2016/06/Israeli-Stocks.png" alt="Israeli Stocks" width="165" height="54" />',

	'Medicine Stocks': '<img class="alignright wp-image-38187" src="https://iknowfirst.com/wp-content/uploads/2016/06/medicine-stocks.png" width="165" height="54" />',

	'Microsoft Stock Forecast': '<img class="alignright wp-image-37253" src="https://iknowfirst.com/wp-content/uploads/2016/05/mlp-stocks-icon.jpg" alt="Stock Forecast Algorithm" width="165" height="54" />',

	'Pharma Stocks Forecast': '<img class="alignright wp-image-37007" src="https://iknowfirst.com/wp-content/uploads/2016/05/Pharma-Stocks-Forecast-1.png" alt="Pharma Stocks Forecast" width="165" height="54" />',

	'S&P 100 Stocks': '<img class="alignright wp-image-36745" src="https://iknowfirst.com/wp-content/uploads/2016/05/SP-100.png" alt="S&amp;P 100" width="165" height="54" />',

	'Small Cap Forecast': '<img class="alignright wp-image-36394" src="https://iknowfirst.com/wp-content/uploads/2016/11/small-cap-stocks-300x98.jpg" alt="" width="165" height="54" />',

	'Stock Forecast & S&P500 Forecast': '<img class="wp-image-41750 size-full alignright" src="https://iknowfirst.com/wp-content/uploads/2016/07/top-10-stocks_small.jpg" width="144" height="47" />',

	'Stocks Under $5': '<img class="alignright wp-image-36628" src="https://iknowfirst.com/wp-content/uploads/2017/03/icon5-dollars-2.gif" alt="under 5" width="150" height="49" />',

	'Stocks Under $50': '<img class="alignright wp-image-36409" src="https://iknowfirst.com/wp-content/uploads/2016/11/Under-10-300x98.jpg" alt="" width="165" height="54" />',

	'Stocks Under $10': '<img class="alignright wp-image-36409" src="https://iknowfirst.com/wp-content/uploads/2016/11/Under-10-300x98.jpg" alt="" width="165" height="54" />',

	'Tech Stocks Forecast': '<img class="alignright wp-image-37247 size-full" src="https://iknowfirst.com/wp-content/uploads/2016/05/Tech-Stocks-165.jpg" alt="Tech Stocks 165" width="165" height="54" />',

	'Transportation Stocks': '<img class="wp-image-43340 alignright" src="https://iknowfirst.com/wp-content/uploads/2016/11/Transportation-Stocks-300x98.jpg" alt="Transportation Stocks" width="233" height="76" />',

	'UK Stock Forecast': '<img class="wp-image-39582 size-full alignright" src="https://iknowfirst.com/wp-content/uploads/2016/06/UK-Stocks-3.jpg" alt="UK Stock Forecast" width="165" height="54" />',

	'Volatility Forecast': '<img class="size-full wp-image-39602 alignright" src="https://iknowfirst.com/wp-content/uploads/2016/06/Volatility-Forecast.jpg" alt="Volatility Forecast" width="165" height="54" />',

	'S&P500 Companies': '<img class="alignright wp-image-38201" src="https://iknowfirst.com/wp-content/uploads/2016/06/sp500-300x98.png" alt="sp500" width="165" height="54" />',

	'Warren Buffett Portfolio': '<img class="alignright wp-image-36946" src="https://iknowfirst.com/wp-content/uploads/2016/05/Warren-Buffett-Portfolio-.png" alt="Warren Buffett Portfolio" width="165" height="54" />',

	'Real Estate Stock Forecast': '<img class=" wp-image-94837 alignright" src="https://iknowfirst.com/wp-content/uploads/2017/02/real-estate-industry-logo.jpg" alt="" width="82" height="67" />',

	'Tech Giants Stocks Forecast': '<img class=" wp-image-94837 alignright" src="https://iknowfirst.com/wp-content/uploads/2017/02/big-tech-logo.jpg" alt="" width="82" height="67" />',

	}


	for key, value in dict.items():
		if key == package_name:
			return value
	return ''























#
