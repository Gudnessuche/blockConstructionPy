import csv

def main():
    try:
        transactions = []
        with open('mempool.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                txid, fee, weight, parents = row
                transactions.append({
                    'txid': txid,
                    'fee': int(fee),
                    'weight': int(weight),
                    'parents': parents.split(';') if parents else [],
                    'included': False
                })

        selected_transactions = []
        
        def traverse(tx):
            if tx['included']:
                return 0
            
            parent_fees = sum(traverse(next(filter(lambda t: t['txid'] == parent_id, transactions))) for parent_id in tx['parents'])
            
            if parent_fees + tx['fee'] <= 4000000:
                selected_transactions.append(tx['txid'])
                tx['included'] = True
                return tx['fee']
            else:
                return 0

        for tx in transactions:
            traverse(tx)
        
        print('\n'.join(selected_transactions[::-1]))
    
    except Exception as e:
        print('Error:', e)

if __name__ == "__main__":
    main()