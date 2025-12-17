import csv

with open("products.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)       
    data = list(reader)         

print("\n--- Product Details ---")
for row in data:
    print(row)

print("\nTotal rows:", len(data))

count_above_500 = 0
for row in data:
    price = int(row[3])
    if price > 500:
        count_above_500 += 1
print("Products priced above 500:", count_above_500)

total_price = 0
for row in data:
    total_price += int(row[3])
avg_price = total_price / len(data)
print("Average price:", avg_price)

category = input("\nEnter category name: ")

print("Products in category:", category)
for row in data:
    if row[2].lower() == category.lower():
        print(row[1])

total_qty = 0
for row in data:
    total_qty += int(row[4])
print("\nTotal quantity in stock:", total_qty)