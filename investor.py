import csv


# Placeholder for Investor class

class Investor:
    def __init__(self, name, company_name, email):
        self.name = name
        self.company_name = company_name
        self.email = email

    @staticmethod
    def from_csv_row(row):
        return Investor(row['Name'], row['Company Name'], row['Email'])


# Placeholder for read_investors_from_csv function

def read_investors_from_csv(file):
    investors = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            investor = Investor.from_csv_row(row)
            investors.append(investor)
    return investors
