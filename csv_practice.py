# Author: Dang Khoi Ngo
# Module 12 Lab: Read a Sales CSV, Write a Cleaned Report

# Reflection
# 1. In Excel I would open the file, add a Total column, filter it, and save it as a new sheet. That works fine for one file, but I'd have to click through it again every time. With Python I run the script once and get the same result on any file, and it can handle way more rows. Excel is still easier when I just want to look at the data, fix one cell, or make a chart.

# 2. A store could keep a log of every time the daily sales report runs, with the time and the total revenue. Append mode works for this because each run adds a new line and keeps the old ones, so there is a history to look back at. If I used write mode, the file would get wiped every run and only the last entry would be left.

import csv
from datetime import datetime

SALES_FILE = "data/sales.csv"
CLEANED_FILE = "data/cleaned.csv"
LOG_FILE = "data/run_log.txt"

print("--- Exercise 1 ---")
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.reader(f)
    row_count = len(list(reader)) - 1
print(f"Opened {SALES_FILE}. Found {row_count} data rows.")

print("--- Exercise 2 ---")
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

print("--- Exercise 3 ---")
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Header: {header}")
    for row in reader:
        print(row)

print("--- Exercise 4 ---")
total_revenue = 0
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        product, price_str, qty_str = row
        price = float(price_str)
        quantity = int(qty_str)
        total = price * quantity
        total_revenue += total
        print(f"{product}: {quantity} units x ${price:.2f} = ${total:.2f}")
print(f"Total revenue: ${total_revenue:.2f}")

print("--- Exercise 5 ---")
high_value = []
rows_read = 0
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        rows_read += 1
        product, price_str, qty_str = row
        price = float(price_str)
        quantity = int(qty_str)
        total = price * quantity
        if total > 100:
            high_value.append([product, f"{price:.2f}", quantity, f"{total:.2f}"])

with open(CLEANED_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for row in high_value:
        writer.writerow(row)

print(f"Wrote {len(high_value)} of {rows_read} rows to {CLEANED_FILE}.")

print("--- Exercise 6 ---")
# reader gives each row as a list, so I have to remember which index is which
# column. DictReader lets me use the column names, which is easier to read and
# still works if the column order changes.
dict_total = 0
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        total = price * quantity
        dict_total += total
        print(f"{row['product']}: {quantity} units x ${price:.2f} = ${total:.2f}")
print(f"Total revenue: ${dict_total:.2f}")
print("Matches Exercise 4:", round(dict_total, 2) == round(total_revenue, 2))

print("--- Exercise 7 ---")
summary = {}
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        product = row["product"]
        total = float(row["price"]) * int(row["quantity"])
        summary[product] = summary.get(product, 0) + total

for product in sorted(summary):
    print(f"{product}: ${summary[product]:.2f}")

print("--- Exercise 8 ---")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_FILE, "a") as log:
    log.write(f"{timestamp} - total revenue: ${total_revenue:.2f}\n")
print(f"Appended a line to {LOG_FILE}")