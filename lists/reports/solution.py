from data import product_data
from pprint import pprint


def build_report():
    labels = product_data[0]

    sku_index = labels.index('sku')
    description_index = labels.index('description')
    unit_sold_web_index = labels.index('units_sold_web')
    unit_sold_stores_index = labels.index('units_sold_stores')
    list_price_index = labels.index('list_price')

    def get_sku_and_description(row_data): return [row_data[sku_index]] + [row_data[description_index]]

    def compute_current_sales(row_data):
        return (row_data[unit_sold_web_index] + row_data[unit_sold_stores_index]) * row_data[list_price_index]

    report = [get_sku_and_description(row_data) + [compute_current_sales(row_data)] for row_data in product_data[1:]]

    report.sort(key=lambda l: l[1])
    report[0:0] = [['SKU', 'description', 'current_sales']]

    build_second_report(report)


def build_second_report(report):
    margin_index = product_data[0].index('margin')
    sku_index = report[0].index('SKU')
    current_sales_index = report[0].index('current_sales')
    description_index = report[0].index('description')

    del report[0]

    def build_row_report(row_report, row_data):
        return [row_report[sku_index]] + \
               [row_report[description_index]] + \
               [row_data[margin_index]] + \
               [row_report[current_sales_index]]

    new_report = [build_row_report(report[i], row_data)
                  for i, row_data in enumerate(product_data[1:])
                  if report[i][current_sales_index] > 1000000]

    report.sort(reverse=True, key=lambda l: l[-1])
    new_report[0:0] = [['SKU', 'description', 'margin', 'current_sales']]
    pprint(report)


def main():
    build_report()


if __name__ == "__main__":
    main()
