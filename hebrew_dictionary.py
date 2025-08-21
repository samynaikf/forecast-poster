

def translate(phrase):
    dict = {'Forecast':	'תחזית',
            'Change':	'שינוי',
            'Symbol':	'המניה',
            'Accuracy':	'דיוק',
            'Hit Ratio': 'אחוז ההצלחה',
            'Algorithmic Stock Forecast':	'תחזית אלגוריתמית',
            'Forecast Performance (long)':	'תחזית ביצועים )GNOL(',
            'Forecast Performance (currencies)':	'תחזית ביצועים )GNOL(',
            'Forecast Performance (short)':	 'תחזית ביצועים )TROHS(',
            'Days':	'ימים',
            'Month':	'חודש',
            'Months':	'חודשים',
            'Year':	'שנה',
            'Updated on': 	'עודכן ב',
            'Forecast Performance (long+short)':	 'תחזית ביצועים )TROHS & GNOL(',
            'Jan':	'ינואר',
            'Feb':	'פברואר',
            'Mar':	'מרץ',
            'Apr':	'אפריל',
            'May':	'מאי',
            'Jun':	'יוני',
            'Jul':	'יולי',
            'Aug':	'אוגוסט',
            'Sep':	'ספטמבר',
            'Oct':	'אוקטובר',
            'Nov':	'נובמבר',
            'Dec':	'דצמבר'}

    for key, value, in dict.items():
        if phrase == key:
            return dict[key][::-1]

    return ' '

#
