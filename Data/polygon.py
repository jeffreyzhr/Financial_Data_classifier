import requests
import pandas as pd
import numpy as np

ticker = 'AAPL'
key = 'erQwKpbpLpuj2AQVEZZswtHU7vYaySEw'
api_url = f"https://api.polygon.io/v2/reference/financials/{ticker}?limit=2&apiKey={key}"
data = requests.get(api_url).json()

df = pd.DataFrame(data['results'])

print(df)
