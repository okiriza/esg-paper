import re
import pandas as pd

def extract_company_mentions(text, df_company):
    company_mentions = []
    for _, row in df_company.iterrows():
        company_name = row['Company Name']
        if company_name.endswith('Tbk.'):
            company_name = company_name[:-1] # delete dot from the end of Tbk.
        ticker = row['Code']
        
        # Regular expression pattern to match the company name in the text (case-insensitive)
        company_name_pattern = re.escape(company_name.strip())
        
        for match in re.finditer(company_name_pattern, text, re.IGNORECASE):
            start_pos = match.start()
            end_pos = match.end()
            # company_id = company_name.replace(" ", "_").lower()  # Generating a simple company ID.
            company_mentions.append((start_pos, end_pos, company_name, ticker))
        
        # Exact match for ticker (case-sensitive with word boundaries)
        ticker_pattern = r'\b{}\b'.format(re.escape(ticker))
        for match in re.finditer(ticker_pattern, text):
            start_pos = match.start()
            end_pos = match.end()
            company_id = ticker  # Generating a simple company ID from the ticker.
            company_mentions.append((start_pos, end_pos, company_id, ticker))

    json_mentions = [{'start': start, 'end': end, 'text': text, 'ticker': ticker} for start, end, text, ticker in company_mentions]

    return json_mentions
  
