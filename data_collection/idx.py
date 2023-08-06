from pathlib import Path
import sys
import time
import warnings

import pandas as pd
import requests

from utils import parse_date, iter_date


def scrape_daily_trade(dt, n_retry=10):
    dt = parse_date(dt)
    dt = str(dt).replace('-', '')
    
    url = f"https://www.idx.co.id/primary/TradingSummary/GetStockSummary?date={dt}&length=9999"
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51",
    }
    
    for _ in range(n_retry):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', message="Unverified HTTPS request is")
            resp = requests.get(url, verify=False, headers=headers)
        
        if resp.status_code == 200:
            break
            
        time.sleep(5)
            
    assert resp.status_code == 200
    assert set(resp.json().keys()) == {'data', 'draw', 'recordsFiltered', 'recordsTotal'}
    
    return resp


def scrape_and_write_daily_trade(dirpath, dt, replace=False):
    dirpath.mkdir(parents=True, exist_ok=True)
    assert dirpath.is_dir()

    fpath = dirpath / f'{dt}.csv'
    if not replace and fpath.exists():
        return
    
    resp = scrape_daily_trade(dt)

    df = pd.DataFrame(resp.json()['data'])
    if len(df):
        df = df.drop(columns=['No'])
    
    df.to_csv(fpath, sep='|', index=False)
    return df
