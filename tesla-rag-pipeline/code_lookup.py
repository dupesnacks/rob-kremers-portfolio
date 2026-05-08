#!/usr/bin/env python3
"""
Tesla Correction Code Lookup Tool
Search for correction codes by description, model, or work type
"""

import json
import pandas as pd
import sys
from typing import List, Dict

class CodeLookup:
    def __init__(self):
        self.df = pd.read_csv('./data/Tesla_Correction_Codes_Master.csv')
        self.index = self._load_index()
    
    def _load_index(self):
        with open('./data/Tesla_Codes_Index.json', 'r') as f:
            return json.load(f)
    
    def lookup_by_code(self, code: str) -> Dict:
        """Look up a specific code"""
        code = code.upper().strip()
        if code in self.index:
            return {code: self.index[code]}
        return {}
    
    def search_by_description(self, keywords: str, model: str = None) -> List[Dict]:
        """Search by description keywords"""
        results = self.df.copy()
        
        # Filter by model if specified
        if model:
            results = results[results['Model'].str.contains(model, case=False, na=False)]
        
        # Search description
        keyword_list = keywords.lower().split()
        for keyword in keyword_list:
            results = results[results['Description'].str.contains(keyword, case=False, na=False)]
        
        return results.to_dict('records')
    
    def search_by_work_type(self, work_type: str, model: str = None, limit: int = 10) -> List[Dict]:
        """Search by work type"""
        results = self.df[self.df['Work_Type'].str.contains(work_type, case=False, na=False)]
        
        if model:
            results = results[results['Model'].str.contains(model, case=False, na=False)]
        
        return results.head(limit).to_dict('records')
    
    def search_by_model_and_keywords(self, model: str, keywords: str) -> List[Dict]:
        """Search specific model for keywords"""
        results = self.df[self.df['Model'].str.contains(model, case=False, na=False)]
        
        keyword_list = keywords.lower().split()
        for keyword in keyword_list:
            results = results[results['Description'].str.contains(keyword, case=False, na=False)]
        
        return results.to_dict('records')
    
    def list_models(self):
        """List all models"""
        return sorted(self.df['Model'].unique().tolist())
    
    def format_results(self, results: List[Dict], limit: int = 20) -> str:
        """Format results for display"""
        if not results:
            return "❌ No results found"
        
        output = f"\n📋 FOUND {len(results)} RESULTS:\n"
        output += "=" * 100 + "\n"
        
        for i, result in enumerate(results[:limit], 1):
            output += f"\n{i}. Code: {result['Code']}\n"
            output += f"   Model: {result['Model']}\n"
            output += f"   Description: {result['Description']}\n"
            output += f"   Work Type: {result['Work_Type']}\n"
            output += f"   Labor Hours: {result['Labor_Hours']} hrs\n"
        
        if len(results) > limit:
            output += f"\n... and {len(results) - limit} more\n"
        
        return output

# Test queries
if __name__ == "__main__":
    lookup = CodeLookup()
    
    print("🔍 TESLA CORRECTION CODE LOOKUP")
    print("=" * 100)
    
    # Example 1: Look up specific code
    print("\n1️⃣ LOOKUP CODE 00000010:")
    result = lookup.lookup_by_code("00000010")
    if result:
        for code, data in result.items():
            print(f"   Code: {code}")
            print(f"   Model: {data['model']}")
            print(f"   Description: {data['description']}")
            print(f"   Work Type: {data['work_type']}")
    
    # Example 2: Search Cybertruck tonneau cover
    print("\n2️⃣ SEARCH: 'Remove and replace tonneau cover for Cybertruck':")
    results = lookup.search_by_model_and_keywords("Cybertruck", "tonneau cover")
    print(lookup.format_results(results))
    
    # Example 3: Search Model Y for battery
    print("\n3️⃣ SEARCH: 'Battery work on Model Y':")
    results = lookup.search_by_model_and_keywords("Model Y", "battery")
    print(lookup.format_results(results))
    
    # Example 4: All remove and replace codes for Model S
    print("\n4️⃣ SEARCH: 'Remove and Replace codes for Model S':")
    results = lookup.search_by_work_type("Remove and Replace", "Model S", limit=15)
    print(lookup.format_results(results, limit=15))
    
    # Example 5: List models
    print("\n5️⃣ AVAILABLE MODELS:")
    for model in lookup.list_models():
        count = len(lookup.df[lookup.df['Model'] == model])
        print(f"   • {model}: {count} codes")
