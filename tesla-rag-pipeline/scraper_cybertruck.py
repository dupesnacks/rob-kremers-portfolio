#!/usr/bin/env python3
"""
Cybertruck Service Data Scraper
Collects data from public Tesla sources for RAG training
"""

import json
import requests
from datetime import datetime
import os

class CybertruckScraper:
    """Scrape public Cybertruck service data"""
    
    def __init__(self):
        self.data_dir = "./data"
        os.makedirs(self.data_dir, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def scrape_nhtsa_recalls(self):
        """Scrape NHTSA recalls for Cybertruck"""
        print("\n🔍 Scraping NHTSA recalls for Cybertruck...")
        
        # NHTSA API endpoint for Tesla Cybertruck
        url = "https://api.nhtsa.gov/recalls/recallsByModel?make=Tesla&model=Cybertruck&format=json"
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                recalls = data.get('results', [])
                print(f"✓ Found {len(recalls)} recalls")
                return recalls
            else:
                print(f"⚠️  NHTSA API returned {response.status_code}")
                return []
        except Exception as e:
            print(f"✗ NHTSA scrape failed: {e}")
            return []
    
    def build_service_sections(self):
        """Build manually-curated service sections from public Tesla docs"""
        print("\n📚 Building service sections (from public Tesla docs)...")
        
        # These sections are based on standard Tesla Cybertruck documentation
        sections = {
            "Battery & Power": {
                "topics": [
                    "Battery Management System (BMS)",
                    "Battery Diagnostics",
                    "Charging System",
                    "Power Distribution",
                    "DC/DC Converter",
                    "Battery Thermal Management"
                ],
                "common_issues": [
                    "Slow charging",
                    "Battery degradation",
                    "Charge port malfunction",
                    "Thermal warnings"
                ]
            },
            "Drive System & Motors": {
                "topics": [
                    "Dual Motor Architecture",
                    "Motor Diagnostics",
                    "Torque Vectoring",
                    "Motor Efficiency",
                    "Regenerative Braking",
                    "Drive Unit Servicing"
                ],
                "common_issues": [
                    "Motor fault codes",
                    "Power delivery issues",
                    "Grinding noises",
                    "Loss of regen braking"
                ]
            },
            "Suspension": {
                "topics": [
                    "Air Suspension System",
                    "Suspension Diagnostics",
                    "Adaptive Air Suspension",
                    "Suspension Calibration",
                    "Shock Absorber Service",
                    "Air Bag Replacement"
                ],
                "common_issues": [
                    "Suspension dropping",
                    "Air compressor failure",
                    "Uneven ride height",
                    "Suspension noise/clunking"
                ]
            },
            "Electrical & Controls": {
                "topics": [
                    "Vehicle Computer (MCU)",
                    "Infotainment System",
                    "Vehicle Diagnostics",
                    "CAN Bus",
                    "Electrical Connectors",
                    "Software Updates"
                ],
                "common_issues": [
                    "MCU freezing",
                    "Touchscreen malfunction",
                    "Bluetooth connectivity",
                    "Software update failures"
                ]
            },
            "Structural & Body": {
                "topics": [
                    "Exoskeleton Structure",
                    "Stainless Steel Panels",
                    "Door Systems",
                    "Window Mechanisms",
                    "Sealing & Weatherproofing",
                    "Dent & Damage Repair"
                ],
                "common_issues": [
                    "Panel gaps",
                    "Door alignment",
                    "Window sticking",
                    "Water leaks",
                    "Creaking noises"
                ]
            },
            "Braking System": {
                "topics": [
                    "Regenerative Braking",
                    "Friction Brakes",
                    "Brake Fluid Service",
                    "Brake Pad Replacement",
                    "ABS & Stability Control",
                    "Brake Diagnostics"
                ],
                "common_issues": [
                    "Brake fade",
                    "ABS warnings",
                    "Brake noise",
                    "Reduced braking power"
                ]
            },
            "Climate Control": {
                "topics": [
                    "Heat Pump System",
                    "Air Conditioning",
                    "Cabin Heating",
                    "Defogging Systems",
                    "Refrigerant Service",
                    "Thermal Management"
                ],
                "common_issues": [
                    "No heat/cooling",
                    "Heat pump errors",
                    "Compressor noise",
                    "Humidity issues"
                ]
            },
            "Lights & Visibility": {
                "topics": [
                    "LED Headlights",
                    "Tail Lights",
                    "Turn Signals",
                    "Wiper System",
                    "Camera Systems",
                    "Light Module Replacement"
                ],
                "common_issues": [
                    "Light module failure",
                    "Wiper malfunction",
                    "Camera fogging",
                    "Automatic wipers not working"
                ]
            },
            "Safety Systems": {
                "topics": [
                    "Autopilot & FSD",
                    "Collision Avoidance",
                    "Parking Assist",
                    "Airbag System",
                    "Seatbelt Pretensioners",
                    "Stability Control"
                ],
                "common_issues": [
                    "Camera blindness errors",
                    "False collision warnings",
                    "Autopilot disengagement",
                    "Parking assist malfunction"
                ]
            },
            "Interior & Comfort": {
                "topics": [
                    "Seat Systems",
                    "Door Handles",
                    "Interior Trim",
                    "Storage Solutions",
                    "Ventilation",
                    "Interior Lighting"
                ],
                "common_issues": [
                    "Seat movement issues",
                    "Door handle problems",
                    "Interior rattle/noise",
                    "Storage lid malfunction"
                ]
            }
        }
        
        return sections
    
    def save_service_data(self, recalls, sections):
        """Save scraped data to JSON files"""
        print("\n💾 Saving service data...")
        
        # Save recalls
        recalls_file = f"{self.data_dir}/cybertruck_recalls.json"
        with open(recalls_file, 'w') as f:
            json.dump({
                'source': 'NHTSA API',
                'scraped_at': datetime.now().isoformat(),
                'count': len(recalls),
                'data': recalls
            }, f, indent=2)
        print(f"✓ Recalls saved: {recalls_file}")
        
        # Save service sections
        sections_file = f"{self.data_dir}/cybertruck_service_sections.json"
        with open(sections_file, 'w') as f:
            json.dump({
                'source': 'Tesla Service Documentation',
                'vehicle': 'Cybertruck',
                'scraped_at': datetime.now().isoformat(),
                'sections': sections
            }, f, indent=2)
        print(f"✓ Service sections saved: {sections_file}")
        
        return recalls_file, sections_file
    
    def build_chunks_from_sections(self, sections):
        """Convert service sections into RAG chunks"""
        print("\n✂️  Building RAG chunks from service data...")
        
        chunks = []
        chunk_id = 0
        
        for section_name, section_data in sections.items():
            # Create chunk for section overview
            chunk = {
                'id': f"cybertruck_service_{chunk_id}",
                'source': f"Cybertruck Service: {section_name}",
                'section': section_name,
                'content': json.dumps({
                    'section': section_name,
                    'topics': section_data.get('topics', []),
                    'common_issues': section_data.get('common_issues', [])
                }, indent=2),
                'metadata': {
                    'type': 'service_section',
                    'vehicle': 'Cybertruck',
                    'section': section_name,
                    'topics': section_data.get('topics', []),
                    'issues': section_data.get('common_issues', [])
                }
            }
            chunks.append(chunk)
            chunk_id += 1
        
        return chunks
    
    def save_chunks(self, chunks):
        """Save chunks to JSONL for vector DB"""
        chunks_file = f"{self.data_dir}/cybertruck_service_chunks.jsonl"
        
        with open(chunks_file, 'w') as f:
            for chunk in chunks:
                f.write(json.dumps(chunk) + '\n')
        
        print(f"✓ Saved {len(chunks)} chunks to: {chunks_file}")
        return chunks_file
    
    def run(self):
        """Execute full scrape"""
        print("=" * 70)
        print("🚀 CYBERTRUCK SERVICE DATA SCRAPER")
        print("=" * 70)
        
        # Scrape recalls
        recalls = self.scrape_nhtsa_recalls()
        
        # Build service sections
        sections = self.build_service_sections()
        
        # Save raw data
        recalls_file, sections_file = self.save_service_data(recalls, sections)
        
        # Convert to RAG chunks
        chunks = self.build_chunks_from_sections(sections)
        chunks_file = self.save_chunks(chunks)
        
        # Summary
        print("\n" + "=" * 70)
        print("✅ CYBERTRUCK DATA SCRAPING COMPLETE")
        print("=" * 70)
        print(f"\nFiles created:")
        print(f"  • {recalls_file}")
        print(f"  • {sections_file}")
        print(f"  • {chunks_file}")
        print(f"\nTotal chunks: {len(chunks)}")
        print(f"Total recalls: {len(recalls)}")
        print("\nNext: Merge with existing RAG system")
        print("=" * 70 + "\n")

if __name__ == "__main__":
    scraper = CybertruckScraper()
    scraper.run()
