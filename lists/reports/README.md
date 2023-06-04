# Report Builder

Given the data in `data.py`:
1. We need to create the data for a basic report that contains three fields: `SKU` (a SKU is a stock keeping unit, 
a term for a product item ID), `description`, and `current_sales`. We are starting with a list of rows of data, and each 
row of data is itself a list, something like this (actual data may differ):
```text
['sku', 'description', 'cost', 'stock', 'margin', 'list_price', 'units_sold_web', 'units_sold_stores', 'date']
['31288', 'Super Whatsit, Large (Dozen)', 301.81, 479, 0.47, 442.22, 457, 956, 509, '2021-06-21'],
['35957', 'Premium Widget, Extra Large (Gross)', 794.74, 855, 0.37, 1088.98, 816, 442, 254, '2021-06-21'],
['91505', 'Deluxe Widget, Extra Large (Gross)', 16.23, 2808, 0.28, 20.77, 406, 665, 11, '2021-06-21'],

(data continues...)
```
The report, again, will need to have only 3 fields:
```
sku, description, current_sales
```
Finally, the directive is to sort this report by `SKU`. The first few lines of this first report should look something like this:
```text
[['11009', 'Economy Device, Micro (Dozen)', 4123855.6999999997],
 ['11663', 'Economy Device, Micro (Gross)', 2529807.6999999997],
 ['13290', 'Premium Gizmo, Large ', 1520431.36],
 ['15862', 'Economy Whatsit, Micro (Gross)', 4089473.0999999996],
 (data continues...)
```
2. Now you need to create a second report, this time with the same data fields plus the margin field from the original data, but with only SKUs with sales over a million (1,000,000). The report will be sorted on current sales from highest to lowest. You should get something that starts out like this:
```text
[['72710', 'Economy Gizmo, Large ', 0.47, 4558402.0],
 ['11009', 'Economy Device, Micro (Dozen)', 0.29, 4123855.6999999997],
 ['15862', 'Economy Whatsit, Micro (Gross)', 0.37, 4089473.0999999996],
 ['30603', 'Budget Whatsit, Giant (Dozen)', 0.45, 3294479.01],
 ['80372', 'Economy Device, Large (Gross)', 0.42, 2694492.3],
(data continues...)```