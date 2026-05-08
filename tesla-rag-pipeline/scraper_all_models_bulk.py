#!/usr/bin/env python3
"""
Bulk Tesla Correction Codes Scraper - All Models
Fetches all correction codes for all Tesla models in parallel
"""

import requests
import json
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

class BulkTeslaScraper:
    """Scrape all correction codes for all Tesla models"""
    
    def __init__(self):
        self.base_url = "https://akamai-apigateway-teslaservice-api.tesla.com/api/CorrectionCode"
        self.models = {
            'Model S': [1, 18],
            'Model 3': [35, 7],
            'Model X': [19, 2],
            'Model Y': [36, 17],
            'Cybertruck': [103],
        }
        self.take = 100
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_model_codes(self, model_name, model_id):
        """Fetch all codes for a single model"""
        print(f"\n🔄 Fetching {model_name} (ID: {model_id})...")
        
        codes = []
        skip = 0
        page = 1
        empty_pages = 0
        
        while True:
            params = {
                'ModelID': model_id,
                'Code': '',
                'CodeName': '',
                'Take': self.take,
                'Skip': skip
            }
            
            try:
                response = self.session.get(self.base_url, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract data from Tesla API response
                    if 'responseObject' in data and isinstance(data['responseObject'], dict):
                        results = data['responseObject'].get('data', [])
                    else:
                        results = []
                    
                    if not results or len(results) == 0:
                        empty_pages += 1
                        if empty_pages >= 2:
                            break
                    else:
                        empty_pages = 0
                        codes.extend(results)
                        print(f"  ✓ Page {page}: {len(results)} codes (total: {len(codes)})")
                    
                    skip += self.take
                    page += 1
                    time.sleep(0.3)  # Rate limiting
                    
                    if page > 100:  # Safety limit
                        break
                else:
                    print(f"  ✗ Status {response.status_code}")
                    break
            
            except Exception as e:
                print(f"  ✗ Error: {e}")
                break
        
        print(f"  ✅ {model_name} (ID: {model_id}): {len(codes)} codes")
        return model_name, model_id, codes
    
    def run(self):
        """Fetch all models in parallel"""
        print("=" * 80)
        print("🚀 BULK TESLA CORRECTION CODES SCRAPER - ALL MODELS")
        print("=" * 80)
        print(f"\nModels to scrape: {len([m for ms in self.models.values() for m in ms])} total")
        print("Running in parallel for speed...\n")
        
        all_model_data = {}
        
        # Create list of (model_name, model_id) tuples
        tasks = []
        for model_name, model_ids in self.models.items():
            for model_id in model_ids:
                tasks.append((model_name, model_id))
        
        # Run in parallel
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_task = {
                executor.submit(self.fetch_model_codes, name, mid): (name, mid) 
                for name, mid in tasks
            }
            
            for future in as_completed(future_to_task):
                model_name, model_id, codes = future.result()
                all_model_data[f"{model_name}_ID{model_id}"] = {
                    'model_name': model_name,
                    'model_id': model_id,
                    'code_count': len(codes),
                    'codes': codes
                }
        
        print("\n" + "=" * 80)
        print("💾 SAVING DATA")
        print("=" * 80)
        
        # Save individual model files
        total_codes = 0
        for key, data in all_model_data.items():
            model_name = data['model_name']
            model_id = data['model_id']
            codes = data['codes']
            total_codes += len(codes)
            
            # Sanitize filename
            filename = f"{model_name.replace(' ', '').replace('+', 'Plus')}_{model_id}"
            
            json_file = f"./data/tesla_correction_codes_{filename}.json"
            with open(json_file, 'w') as f:
                json.dump({
                    'model': model_name,
                    'model_id': model_id,
                    'total_codes': len(codes),
                    'scraped': datetime.now().isoformat(),
                    'codes': codes
                }, f, indent=2)
            
            print(f"✓ {model_name} ID {model_id}: {len(codes)} codes → {json_file}")
        
        # Save master combined file
        master_file = "./data/tesla_correction_codes_ALL_MODELS.json"
        with open(master_file, 'w') as f:
            json.dump({
                'all_models': all_model_data,
                'total_models': len(all_model_data),
                'total_codes': total_codes,
                'scraped': datetime.now().isoformat()
            }, f, indent=2)
        print(f"\n✓ Master file: {master_file}")
        
        # Summary
        print("\n" + "=" * 80)
        print("✅ SCRAPING COMPLETE")
        print("=" * 80)
        
        print(f"\n📊 SUMMARY:")
        print(f"  • Total Models: {len(all_model_data)}")
        print(f"  • Total Codes: {total_codes:,}")
        print(f"  • Avg Codes/Model: {total_codes // len(all_model_data)}")
        
        print(f"\n🔍 BREAKDOWN BY MODEL:")
        for key in sorted(all_model_data.keys()):
            data = all_model_data[key]
            print(f"  • {data['model_name']} (ID {data['model_id']}): {data['code_count']:,} codes")
        
        print(f"\n✅ READY FOR RAG INGESTION")
        print("=" * 80 + "\n")
        
        return all_model_data

if __name__ == "__main__":
    scraper = BulkTeslaScraper()
    scraper.run()
