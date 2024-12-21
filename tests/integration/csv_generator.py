import exrex
import random
import csv

file_name="test_transaction.csv"
with open(file_name, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for i in range(1000):
        spamwriter.writerow([str(int(random.uniform(1, 999999))), exrex.getone("user_\d{3}"), round(random.uniform(10, 5000), 1), "USD", exrex.getone('2024-(0[0-9]|1[0-2])-([0-1][0-9]|2[0-8]) ([0-1][0-9]|2[0-3])(:[0-5]\d){2}')])

