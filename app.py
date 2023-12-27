from flask import Flask, render_template, request, redirect, send_file
import csv
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def landing_page():
    return render_template('Actions.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        transaction_type = request.form['transaction_type']
        timestamp = datetime.now().strftime('%Y-%m-%d')
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

    return render_template('expenseFilingpage.html')

@app.route('/clear_transactions')
def clear_transactions():
    # Clear the transactions list
    with open('transactions.csv', "w") as csvfile:
        fieldnames = ['Type', 'Timestamps', 'Amount', 'Description', 'Category', 'Category1']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
    return redirect("/")


@app.route('/download_csv')
def download_csv():
    # Generate CSV content
    csv_file_path = 'transactions.csv'

    #check if there is transactions csv file exist
    if not os.path.exists(csv_file_path):
        return render_template("noTransactionsAvailable.html")
        # sleep(5)
        # return redirect("/")


    # Provide the file for download
    return send_file(csv_file_path, as_attachment=True, download_name='transactions.csv')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
