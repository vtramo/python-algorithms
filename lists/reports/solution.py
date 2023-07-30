from data import product_data
from pprint import pprint
from sys import getsizeof


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

    return build_second_report(report)


def build_second_report(report):
    margin_index = product_data[0].index('margin')
    sku_index = report[0].index('SKU')
    current_sales_index = report[0].index('current_sales')
    description_index = report[0].index('description')

    del report[0]
    del product_data[0]
    report.sort(reverse=True, key=lambda l: l[-1])

    def build_row_report(row_report, row_data):
        return [row_report[sku_index]] + \
            [row_report[description_index]] + \
            [row_data[margin_index]] + \
            [row_report[current_sales_index]]

    new_report = (
        build_row_report(row_report, row_data)
        for row_report, row_data in zip(report, product_data)
        if row_report[current_sales_index] > 1000000
    )

    for row in new_report:
        pprint(row)

    # for experimental purposes
    return [
        build_row_report(row_report, row_data)
        for row_report, row_data in zip(report, product_data)
        if row_report[current_sales_index] > 1000000
    ]


def count_bytes_collection(c):
    return sum([getsizeof(x) for x in c])


def main():
    report = build_report()
    print(f'getsizeof(report): {getsizeof(report)} | getsizeof(product_data): {getsizeof(product_data)}')

    bytes_shallow_content_report = sum([getsizeof(x) for x in report])
    bytes_shallow_content_product_data = sum([getsizeof(x) for x in report])
    bytes_deep_content_report = sum(
        [count_bytes_collection(x) for x in report]) + bytes_shallow_content_report + getsizeof(report)
    bytes_deep_content_product_data = sum(
        [count_bytes_collection(x) for x in product_data]) + bytes_shallow_content_product_data + getsizeof(
        product_data)

    print(f'bytes_deep_content_report: {bytes_deep_content_report} | bytes_deep_content_product_data: {bytes_deep_content_product_data}')
    print(f'bytes_shallow_content_report: {bytes_shallow_content_report} | bytes_shallow_content_product_data: {bytes_shallow_content_product_data}')

    copy_report = report[:]
    is_not_a_copy = [id(x) == id(report[i]) for i, x in enumerate(copy_report)]
    have_all_same_id = sum((1 for x in is_not_a_copy if x)) == len(copy_report)
    print(have_all_same_id)

    row_copy_report = report[1][:]
    is_not_a_copy = [id(x) == id(report[1][i]) for i, x in enumerate(row_copy_report)]
    have_all_same_id = sum((1 for x in is_not_a_copy if x)) == len(row_copy_report)
    print(have_all_same_id)


if __name__ == "__main__":
    main()
