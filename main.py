import hubspot


def main():
    deals = hubspot.api.fetch_deals()

    overall_deal_amount_expected = sum([deal.get_amount_expected() for deal in deals])
    print('deal amount expected: %f' % overall_deal_amount_expected)

    overall_deal_amount = sum([deal.get_amount() for deal in deals if deal.is_won()])
    print('deal amount actual: %f' % overall_deal_amount)


if __name__ == '__main__':
    main()
