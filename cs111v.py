import csv

with open('user.csv', 'r', encoding='utf-8') as fdat:
    fields = ['1', '2', '3', '4',]
    reader = csv.DictReader(fdat, fields, delimiter=';')
    for i in reader:
        print(i)
