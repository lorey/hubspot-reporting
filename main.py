import csv
import os
from datetime import datetime

from matplotlib import mlab
from matplotlib import pyplot

import hubspot


def main():
    # plot pipelines
    pipelines = hubspot.api.fetch_pipelines()
    for pipeline in pipelines:
        filename = 'data.csv'
        dir_path = 'out/' + pipeline.get_id() + '/'
        file_path = dir_path + filename

        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        write_data_to_csv(file_path, pipeline_id=pipeline.get_id())
        generate_charts_from_csv(file_path, title=pipeline.get_label())

    # plot overall
    filename = 'data.csv'
    dir_path = 'out/' + 'overall' + '/'
    file_path = dir_path + filename

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    write_data_to_csv(file_path)
    generate_charts_from_csv(file_path, title='all deals')


def generate_charts_from_csv(csv_path, title=None):
    # http://matplotlib.org/examples/api/date_index_formatter.html
    r = mlab.csv2rec(open(csv_path))

    # todo fix path deduction
    path = csv_path.replace('data.csv', '')

    r.sort()
    r = r[-30:]  # get the last 30 values

    generate_deal_amount_plot(r, path, title=title)
    generate_deal_count_plot(r, path, title=title)


def generate_deal_count_plot(r, path, title=None):
    fig, ax = pyplot.subplots()

    ax.plot(r.date, r.deals_funnel, '-', label='Deal Funnel')
    ax.plot(r.date, r.deals_closed, '-', label='Closed Deals')

    fig.autofmt_xdate()  # ?

    if title is not None:
        pyplot.title('Deal Flow (%s)' % title)
    else:
        pyplot.title('Deal Flow')

    pyplot.xlabel('Date')
    pyplot.ylabel('# of Deals')
    pyplot.legend(loc='best')

    pyplot.savefig(path + 'deal_count')


def generate_deal_amount_plot(r, path, title=None):
    fig, ax = pyplot.subplots()

    ax.plot(r.date, r.deals_amount_funnel, '-', label='Deal Funnel')
    ax.plot(r.date, r.deals_amount_closed, '-', label='Closed Deals')

    fig.autofmt_xdate()  # ?

    if title is not None:
        pyplot.title('Deal Flow (%s)' % title)
    else:
        pyplot.title('Deal Flow')

    pyplot.xlabel('Date')
    pyplot.ylabel('Amount in Euros')
    pyplot.legend(loc='best')

    pyplot.savefig(path + 'deal_amount')


def write_data_to_csv(path, pipeline_id=None):
    deals = hubspot.api.fetch_deals()
    if pipeline_id is not None:
        deals = [deal for deal in deals if deal.get_pipeline_id() == pipeline_id]

    overall_deal_count = len([1 for deal in deals if deal.is_won()])
    overall_deal_count_expected = sum([deal.get_stage().get_win_probability() for deal in deals])

    overall_deal_amount = int(sum([deal.get_amount() for deal in deals if deal.is_won()]))
    overall_deal_amount_expected = int(sum([deal.get_amount_expected() for deal in deals]))

    fields = [
        str(datetime.now()),
        overall_deal_count,
        overall_deal_count_expected,
        overall_deal_amount,
        overall_deal_amount_expected
    ]

    # make sure csv exists
    if not os.path.isfile(path):
        with open(path, 'w+') as file:
            cw = csv.writer(file)
            # write header
            cw.writerow(['date', 'deals_closed', 'deals_funnel', 'deals_amount_closed', 'deals_amount_funnel'])

    # append new row
    with open(path, 'a') as file:
        cw = csv.writer(file)
        cw.writerow(fields)


if __name__ == '__main__':
    main()
