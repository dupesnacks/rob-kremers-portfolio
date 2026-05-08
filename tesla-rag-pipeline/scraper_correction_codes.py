#!/usr/bin/env python3
"""
Tesla Correction Codes Scraper
Fetches all 4000+ correction codes for Model Y 2025+ from Tesla service API
"""

import requests
import json
import time
from datetime import datetime
import pandas as pd

class TeslaCorrectionCodeScraper:
    """Scrape all correction codes from Tesla service API"""
    
    def __init__(self):
        self.base_url = "https://akamai-apigateway-teslaservice-api.tesla.com/api/CorrectionCode"
        self.model_id = 36  # Model Y 2025+
        self.take = 100  # Results per request
        self.codes = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_page(self, skip):
        """Fetch a single page of codes"""
        params = {
            'ModelID': self.model_id,
            'Code': '',
            'CodeName': '',
            'Take': self.take,
            'Skip': skip
        }
        
        try:
            print(f"  Fetching codes {skip}-{skip + self.take - 1}...", end=" ", flush=True)
            response = self.session.get(self.base_url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Tesla API wraps data in responseObject.data
                if 'responseObject' in data and isinstance(data['responseObject'], dict):
                    results = data['responseObject'].get('data', [])
                elif isinstance(data, list):
                    results = data
                elif isinstance(data, dict) and 'data' in data:
                    results = data['data']
                elif isinstance(data, dict) and 'results' in data:
                    results = data['results']
                else:
                    results = []
                
                if isinstance(results, list):
                    print(f"✓ Got {len(results)} codes")
                    return results
                else:
                    print(f"⚠️  Unexpected format")
                    return []
            else:
                print(f"✗ Status {response.status_code}")
                return []
        
        except Exception as e:
            print(f"✗ Error: {e}")
            return []
    
    def run(self):
        """Fetch all correction codes"""
        print("=" * 80)
        print("🚀 TESLA CORRECTION CODES SCRAPER")
        print("=" * 80)
        print(f"\nFetching correction codes for Model Y 2025+ (ModelID: {self.model_id})")
        print(f"API: {self.base_url}")
        print(f"Taking {self.take} codes per request\n")
        
        # Estimate total requests needed (assuming 4000 codes)
        # We'll fetch until we get < 100 codes back
        skip = 0
        page = 1
        empty_pages = 0
        
        while True:
            codes_page = self.fetch_page(skip)
            
            if not codes_page or len(codes_page) == 0:
                empty_pages += 1
                if empty_pages >= 2:  # Stop after 2 empty pages
                    break
            else:
                empty_pages = 0
                self.codes.extend(codes_page)
            
            skip += self.take
            page += 1
            time.sleep(0.5)  # Rate limiting
            
            # Safety limit
            if page > 100:
                print("⚠️  Reached 100 pages, stopping")
                break
        
        print(f"\n✅ FETCHED {len(self.codes)} TOTAL CORRECTION CODES")
        self.save_data()
    
    def save_data(self):
        """Save codes to Excel and JSON"""
        if not self.codes:
            print("❌ No codes fetched!")
            return
        
        print("\n" + "=" * 80)
        print("💾 SAVING DATA")
        print("=" * 80)
        
        # Save as JSON
        json_file = "./data/tesla_correction_codes_model_y_2025.json"
        with open(json_file, 'w') as f:
            json.dump({
                "model": "Model Y 2025+",
                "model_id": self.model_id,
                "total_codes": len(self.codes),
                "scraped": datetime.now().isoformat(),
                "codes": self.codes
            }, f, indent=2)
        print(f"✓ JSON: {json_file}")
        
        # Save as CSV (for Excel)
        csv_file = "./data/tesla_correction_codes_model_y_2025.csv"
        
        # Flatten the structure if needed
        if self.codes and isinstance(self.codes[0], dict):
            df = pd.DataFrame(self.codes)
        else:
            # If codes are just strings, create simple structure
            df = pd.DataFrame({'code': self.codes})
        
        df.to_csv(csv_file, index=False)
        print(f"✓ CSV: {csv_file}")
        
        # Save as Excel with formatting
        excel_file = "./data/tesla_correction_codes_model_y_2025.xlsx"
        try:
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Correction Codes', index=False)
                
                # Auto-adjust column widths
                worksheet = writer.sheets['Correction Codes']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            print(f"✓ Excel: {excel_file}")
        except Exception as e:
            print(f"⚠️  Excel creation failed: {e}")
        
        # Print sample
        print(f"\n📊 SAMPLE DATA ({min(10, len(self.codes))} of {len(self.codes)} codes):")
        print("-" * 80)
        if isinstance(self.codes[0], dict):
            for i, code in enumerate(self.codes[:10]):
                print(f"{i+1}. {code}")
        else:
            for i, code in enumerate(self.codes[:10]):
                print(f"{i+1}. {code}")
        
        print(f"\n{'='*80}")
        print(f"✅ COMPLETE: {len(self.codes)} codes saved")
        print(f"{'='*80}\n")

if __name__ == "__main__":
    scraper = TeslaCorrectionCodeScraper()
    scraper.run()
