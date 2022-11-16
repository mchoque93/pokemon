import csv
import os

from app.models.models import Pokemon, db
from entrypoint import app



if __name__ == '__main__':
    with app.app_context():

        outfile = open('C:\\Users\\e056701\\PycharmProjects\\pokemon\\pokemon_csv5.csv', 'w', encoding="utf-8", newline='')
        outcsv = csv.writer(outfile, delimiter=";")
        records = db.session.query(Pokemon).all()
        [outcsv.writerow([getattr(curr, column.name) for column in Pokemon.__mapper__.columns] + [",".join([v.name for v in curr.tipos])]) for curr in records]

        # or maybe use outcsv.writerows(records)

        outfile.close()
