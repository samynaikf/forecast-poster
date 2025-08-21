

def get_package_name_backup(name):
    package_name = ''
    name_info = name.split('/')[-1].split(' ')[0].split('_')
    for x in range(len(name_info)):
        if x >= len(name_info) - 3:
            break
        package_name += ' '+name_info[x]
    return package_name

def get_package_name(name):
    package_dict = {
    'Australia':	'Australian Stocks',
    'top_10_Australia':	'Australian Stocks',
    'Bovespa':	'Bovespa',
    'Bovespa1':	'Bovespa',
    'top_10_Bovespa1':	'Bovespa',
    'Brazil':	'Brazil Stock Forecast',
    'CANADA':	'Canadian Stock Forecast',
    'Top_20_CANADA':	'Canadian Stock Forecast',
    'Top_10_CANADA':	'Canadian Stock Forecast',
    'China':	'Chinese Stock Forecast',
    'Shanghai':	'Shanghai Stock Forecast',
    'top_10_Shanghai':	'Shanghai Stock Forecast',
    'Shenzhen':	'Shenzhen Stock Forecast',
    'top_10_Shenzhen':	'Shenzhen Stock Forecast',
    'top_10_EUROPE_ETFs':	'European ETFs Forecast',
    'EUROPE_ETFs':	'European ETFs Forecast',
    'EUROPE':	'European Stock Forecast',
    'top_10_EUROPE':	'European Stock Forecast',
    'French':	'French Stock Forecast',
    'Germany':	'German Stock Forecast',
    'HK':	'Hong Kong Stock Forecast',
    'HK_HSI_stocks':	'Hong Kong Stock Forecast',
    'HONGKONG':	'Hong Kong Stock Forecast',
    'Top_10_HONGKONG':	'Hong Kong Stock Forecast',
    'India':	'Indian Stock Forecast',
    'India_stocks':	'Indian Stock Forecast',
    'Top10_India':	'Indian Stock Forecast',
    'Top_10_India':	'Indian Stock Forecast',
    'Indonesia':	'Indonesian Stocks',
    'SaudiArab':	'Saudi Arabian Stocks',
    'top_10_SaudiArab':	'Saudi Arabian Stocks',
    'Singapore':	'Singaporean Stock Forecast',
    'Taiwan':	'Taiwanese Stock Forecast',
    'Italy':	'Italian Stocks',
    'Japan':	'Japan Stock Forecast',
    'Israel':	'Israeli Stocks',
    'top_10_Israel':	'Israeli Stocks',
    'top_10_big_Israel':	'Israeli Stocks',
    'Russia':	'Russian Stock Forecast',
    'SouthAfrica':	'South African Stocks',
    'Spain':	'Spanish Stocks',
    'MSCI_ACWI_East':	'MSCI Stocks Universe',
    'MSCI_ACWI_West':	'MSCI Stocks Universe',
    'Turkey':	'Turkish Stock Forecast',
    'Switzerland':	'Swiss Stocks',
    }

    for key, value in package_dict.items():
        if key in name:
            return value

    print("Could not find matching package name for\n{}".format(name))
    return get_package_name_backup(name)
























#
