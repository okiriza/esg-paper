import re

def extract_company_mentions(text, company_data):
    company_mentions = []
    for _, row in company_data.iterrows():
        company_name = row['Company Name']
        ticker = row['Code']
        
        # Regular expression pattern to match the company name in the text (case-insensitive)
        company_name_pattern = re.escape(company_name.strip())
        
        for match in re.finditer(company_name_pattern, text, re.IGNORECASE):
            start_pos = match.start()
            end_pos = match.end()
            # company_id = company_name.replace(" ", "_").lower()  # Generating a simple company ID.
            company_mentions.append((start_pos, end_pos, company_name))
        
        # Exact match for ticker (case-sensitive with word boundaries)
        ticker_pattern = r'\b{}\b'.format(re.escape(ticker))
        for match in re.finditer(ticker_pattern, text):
            start_pos = match.start()
            end_pos = match.end()
            company_id = ticker  # Generating a simple company ID from the ticker.
            company_mentions.append((start_pos, end_pos, company_id))
    
    return company_mentions