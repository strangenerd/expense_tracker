from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    transaction_type = request.form['transaction_type']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    amount = int(request.form['amount'])
    description = request.form['description'][:200]
    category = request.form['category']

    with open('transactions.csv', 'a', newline='') as csvfile:
        fieldnames = ['Type', 'Timestamps', 'Amount', 'Description', 'Category', 'Category1']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        if transaction_type == "Expense":
            writer.writerow({
                'Type': transaction_type,
                'Timestamps': timestamp,
                'Amount': amount,
                'Description': description,
                'Category': category,
                'Category1' : None
            })
        else:
            writer.writerow({
                'Type': transaction_type,
                'Timestamps': timestamp,
                'Amount': amount,
                'Description': description,
                'Category' : None,
                'Category1': category
            })


    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5000) 
