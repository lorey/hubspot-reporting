import csv
import os
from datetime import datetime

from matplotlib import mlab
from matplotlib import pyplot

import hubspot


def main():
    write_data_to_csv()
    generate_charts()


def generate_charts():
    # http://matplotlib.org/examples/api/date_index_formatter.html
    r = mlab.csv2rec(open('data.csv'))

    r.sort()
    r = r[-30:]  # get the last 30 values

    fig, ax = pyplot.subplots()

    ax.plot(r.date, r.deals_funnel, 'o-', label='Deal Funnel')
    ax.plot(r.date, r.deals_closed, 'o-', label='Closed Deals')

    fig.autofmt_xdate()  # ?

    pyplot.title('Deal Flow')
    pyplot.xlabel('Date')
    pyplot.ylabel('Amount in Euros')
    pyplot.legend(loc='best')

    pyplot.savefig('dealflow')


def write_data_to_csv():
    deals = hubspot.api.fetch_deals()

    overall_deal_amount_expected = int(sum([deal.get_amount_expected() for deal in deals]))
    print('deal amount expected: %d' % overall_deal_amount_expected)

    overall_deal_amount = int(sum([deal.get_amount() for deal in deals if deal.is_won()]))
    print('deal amount actual: %d' % overall_deal_amount)

    fields = [
        str(datetime.now()),
        overall_deal_amount,
        overall_deal_amount_expected
    ]

    filename = 'data.csv'

    # make sure csv exists
    if not os.path.isfile(filename):
        with open(filename, 'a') as file:
            cw = csv.writer(file)
            # write header
            cw.writerow(['date', 'deals_closed', 'deals_funnel'])

    # append new row
    with open(filename, 'a') as file:
        cw = csv.writer(file)
        cw.writerow(fields)


if __name__ == '__main__':
    main()
