
def fetchdata(company_name):

	URL = "https://ticker.finology.in/company/"+company_name+""

	HEADERS = ({'User-Agent':
				'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
				(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
				'Accept-Language': 'en-US, en;q=0.5'})

	webpage = requests.get(URL, headers=HEADERS)
	soup = BeautifulSoup(webpage.content, "html.parser")
	dom = etree.HTML(str(soup))
	#pe_ratio, pb_ratio, last_price, dividends_per_share, roe, roce, debt_to_equity_ratio
	pe_ratio = dom.xpath('//*[@id="mainContent_updAddRatios"]/div[4]/p')[0].text
	pb_ratio = dom.xpath('//*[@id="mainContent_updAddRatios"]/div[5]/p')[0].text
	roe = dom.xpath('//*[@id="mainContent_updAddRatios"]/div[14]/p/span')[0].text
	debt_to_equity_ratio = dom.xpath('//*[@id="mainContent_divDebtEquity"]/div/span')[0].text
	roce = dom.xpath('//*[@id="mainContent_updAddRatios"]/div[15]/p/span')[0].text