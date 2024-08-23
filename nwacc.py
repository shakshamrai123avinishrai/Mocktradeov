import requests
import time

url = "https://paper-api.alpaca.markets/v2/orders"

stocks = ['IBM', 'AAPL', 'GOOGL', 'MSFT']
holdings = [5, 4, 3, 2]

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "APCA-API-KEY-ID": "PKFO35XBDXXL9WGHK###",
    "APCA-API-SECRET-KEY": "pir9wSvhSv1kgSgofAj80LcgQ4csI6y2fJgUh###"
}

purchase_prices = {}

while True:
    for stock, qty in zip(stocks, holdings):
        payload = {
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
            "symbol": stock,
            "qty": qty
        }
        response = requests.post(url, json=payload, headers=headers)
        print(f"Response for {stock}: {response.text}")
        if response.status_code == 200:
            order_info = response.json()
            order_id = order_info.get('id')
            print(f"Order ID for {stock}: {order_id}")

            time.sleep(2)

            order_status_url = f"https://paper-api.alpaca.markets/v2/orders/{order_id}"
            order_status_response = requests.get(order_status_url, headers=headers)
            if order_status_response.status_code == 200:
                order_status_info = order_status_response.json()
                print(f"Order Status for {stock}: {order_status_info}")
                stock_price =order_status_info.get('filled_avg_price', 'no price available')
                if stock_price and stock_price != 'no price available':
                    purchase_prices[stock] = float(stock_price)
                else:
                    purchase_prices[stock] = 0
            else:
                print(f"Failed to get order status for {stock}")
        else:
            print(f"Failed to place order for {stock}")
    print("Purchase Prices:", purchase_prices)

    total_value = 0
    for stock, qty in zip(stocks, holdings):
        total_value += purchase_prices.get(stock,0)*qty
    print("Total_value_of_Holdings:", total_value)

    total_investment = total_value
    print("Total_investment:",total_investment)

    ratio = [1, 2, 2, 2, 2]
    total_ratio = sum(ratio)
    print(total_ratio)
    part_value = total_investment / total_ratio
    ideal_investment = [part_value*parts for parts in [1,2,2,2,2]]
    print("Total_ideal_investment:",ideal_investment)
    purchase_prices_values = list(purchase_prices.values())
    purchase_prices_values = [float(price) for price in purchase_prices_values]
    ideal_holdings = []
    for investment, price in zip(ideal_investment, purchase_prices_values):
        if price != 0:
            ideal_holdings.append(investment / price)
        else:
            ideal_holdings.append(0) 
    print("Total_ideal_holdings:",ideal_holdings)
    roundoff_holdings = [round(holdings) for holdings in ideal_holdings]
    Transactions = [round_off - holdings  for round_off, holdings in zip( roundoff_holdings, holdings)]

    for stock, transaction in zip(stocks, Transactions):
        if transaction > 0:
            side = "buy"
        elif transaction < 0:
            side = "sell"
            transaction = abs(transaction)
        else:
            continue
        payload = {
            "side": side,
            "type": "market",
            "time_in_force": "day",
            "symbol": stock,
            "qty": transaction
        }
        response = requests.post(url, json=payload, headers=headers)
        print(f"Rebalancing Response for {stock}: {response.text}")

    print("Rebalancing Complete.")
    

    print("Waiting for 5 minutes before next iteration...")
    time.sleep(300)
