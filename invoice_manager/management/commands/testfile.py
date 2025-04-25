import json

# Path to your original .sim file
file_path = "/Users/abc/Documents/TEXVO/texvo/invoice_manager/management/commands/Backup_25Apr2025_1731.sim"

# Load the content (the file is JSON in disguise)
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Access the first table object
invoice_data = data.get("InvoiceTBLs", [{}])[0]
# print(invoice_data)
# print(type(data))
for item in data:
    print(type(data),item)
other_data = data["OtherData"]
print(other_data)
# print(len(invoice_data))
# clients=invoice_data["clients"]
# print(len(clients))
# for client in clients:
#     print(type(client))
#     for key, value in client.items():
#         print(f"{key}: {value}")
    # Extract expenses and purchases

# expenses = invoice_data.get("expenses", [])
# purchases = invoice_data.get("purchases", [])

# Example: Print the first 3 records from each
# print("Expenses:")
# for item in expenses[:3]:
#     print(item)

# print("\nPurchases:")
# for item in purchases[:3]:
#     print(item)
