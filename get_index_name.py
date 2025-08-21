'''
Function to get name of index from index ticker
'''


def get_index_name(index):

    index_names = {'^AORD': 'S&P ASX',
                    '^AORD':'S&P ASX',
                    '^BVSP':'BOVESPA',
                    '^BVSP':'BOVESPA',
                    '^BVSP':'BOVESPA',
                    '^BVSP':'BOVESPA',
                    '^GSPTSE':'TSX',
                    '^GSPTSE':'TSX',
                    '^GSPTSE':'TSX',
                    '^SSEC':'SHANGHAI SE',
                    '^SSEC':'SHANGHAI SE',
                    '^SSEC':'SHANGHAI SE',
                    '^SSEC':'SHANGHAI SE',
                    '^SSEC':'SHANGHAI SE',
                    '^N100':'EURONEXT 100',
                    '^N100':'EURONEXT 100',
                    '^N100':'EURONEXT 100',
                    '^N100':'EURONEXT 100',
                    '^FCHI':'CAC 40',
                    '^GDAXI':'BORSE DAX',
                    '^HSI':'HANG SENG',
                    '^HSI':'HANG SENG',
                    '^HSI':'HANG SENG',
                    '^HSI':'HANG SENG',
                    '^BSESN':'S&P BSE',
                    '^BSESN':'S&P BSE',
                    '^BSESN':'S&P BSE',
                    '^BSESN':'S&P BSE',
                    '^NSEI':'NSE',
                    '^JKSE':'JSX COMPOSITE',
                    '^TASI':'TDW MAIN',
                    '^TASI':'TDW MAIN',
                    '^STI':'FTSE STRAITS TIMES',
                    '^TWII':'TAIWAN SE',
                    '^FTMIB':'FTSE MIB',
                    '^N225':'NIKKEI 225',
                    '^TA125':'TASE 125',
                    '^TA125':'TASE 125',
                    '^TA90':'TASE 90',
                    '^TA35':'TASE 35',
                    '^IRTS':'RTS',
                    '^JALSH':'JSE Africa',
                    '^IBEX':'IBEX 35 COMPOSITE',
                    'MSCI':'MSCI',
                    '^XU100':'XU 100',
                    '^SSMI':'SMI',
                    '^FTMC':'FTSE 250',
                    '^NSEI':'NIFTY 50',
                    '^ISEQ':'ISEQ-OVERALL PR EUR',
                    '^FTSE':'FTSE 100',
                    '^S&P500':'S&P 500',
                    '^MERV':'MERVAL',
                    '^SET50':'SET50',
                    '^SPBLPGPT':'S&P/BVL',
                    '^MXX':'S&P BMV/IPC'}

    name = index
    for key, value in index_names.items():
        if key == index:
            name = value
            break

    return name
