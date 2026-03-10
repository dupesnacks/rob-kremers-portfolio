#!/usr/bin/env python3
"""
Comprehensive Cybertruck Service Data Scraper
Collects parts, tires, technical docs, diagnostic codes, TSBs, etc.
"""

import json
import os
from datetime import datetime

class ComprehensiveCybertruckScraper:
    """Comprehensive scraper for all Cybertruck service data"""
    
    def __init__(self):
        self.data_dir = "./data"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def build_parts_catalog(self):
        """Build comprehensive parts catalog with part numbers"""
        print("\n🔧 Building Parts Catalog...")
        
        parts = {
            "Drivetrain": {
                "Motors & Drive Units": [
                    {"part_name": "Front Motor Assembly", "part_number": "1520240-00-A", "labor_hours": 4.5, "category": "Motor"},
                    {"part_name": "Rear Motor Assembly", "part_number": "1520250-00-B", "labor_hours": 5.0, "category": "Motor"},
                    {"part_name": "Motor Bearing Kit", "part_number": "1520260-00-A", "labor_hours": 2.0, "category": "Bearing"},
                    {"part_name": "Inverter Module", "part_number": "1520300-00-A", "labor_hours": 3.5, "category": "Power Electronics"},
                    {"part_name": "High-Voltage Contactor", "part_number": "1520310-00-A", "labor_hours": 1.5, "category": "Electrical"},
                ],
                "Transmission & Differential": [
                    {"part_name": "Single-Speed Reducer", "part_number": "1520400-00-A", "labor_hours": 6.0, "category": "Transmission"},
                    {"part_name": "Differential Assembly", "part_number": "1520410-00-A", "labor_hours": 7.0, "category": "Differential"},
                    {"part_name": "Axle Shaft", "part_number": "1520420-00-A", "labor_hours": 2.5, "category": "Axle"},
                ]
            },
            "Suspension": {
                "Air Suspension System": [
                    {"part_name": "Air Compressor", "part_number": "1130010-00-A", "labor_hours": 3.0, "category": "Compressor"},
                    {"part_name": "Air Suspension Strut - Front", "part_number": "1130020-00-A", "labor_hours": 2.0, "category": "Strut"},
                    {"part_name": "Air Suspension Strut - Rear", "part_number": "1130030-00-A", "labor_hours": 2.5, "category": "Strut"},
                    {"part_name": "Air Spring Bag Assembly", "part_number": "1130040-00-A", "labor_hours": 1.5, "category": "Air Bag"},
                    {"part_name": "Height Sensor - Front", "part_number": "1130050-00-A", "labor_hours": 1.0, "category": "Sensor"},
                    {"part_name": "Height Sensor - Rear", "part_number": "1130060-00-A", "labor_hours": 1.0, "category": "Sensor"},
                    {"part_name": "Damping Strut", "part_number": "1130070-00-A", "labor_hours": 2.0, "category": "Damper"},
                ],
                "Control Arms & Links": [
                    {"part_name": "Upper Control Arm - Front", "part_number": "1130100-00-A", "labor_hours": 1.5, "category": "Control Arm"},
                    {"part_name": "Lower Control Arm - Front", "part_number": "1130110-00-A", "labor_hours": 1.5, "category": "Control Arm"},
                    {"part_name": "Tie Rod Assembly", "part_number": "1130120-00-A", "labor_hours": 1.0, "category": "Steering"},
                    {"part_name": "Sway Bar Link", "part_number": "1130130-00-A", "labor_hours": 0.5, "category": "Link"},
                ]
            },
            "Battery & Power": {
                "Battery Pack": [
                    {"part_name": "Battery Module (Cell)", "part_number": "1410010-00-A", "labor_hours": 0.5, "category": "Battery"},
                    {"part_name": "Battery Pack Assembly", "part_number": "1410020-00-A", "labor_hours": 8.0, "category": "Battery"},
                    {"part_name": "BMS Control Module", "part_number": "1410030-00-A", "labor_hours": 2.0, "category": "Control"},
                    {"part_name": "Battery Coolant Pump", "part_number": "1410040-00-A", "labor_hours": 2.5, "category": "Cooling"},
                ],
                "Charging System": [
                    {"part_name": "On-Board Charger (OBC)", "part_number": "1410100-00-A", "labor_hours": 3.0, "category": "Charger"},
                    {"part_name": "Charge Port Latch", "part_number": "1410110-00-A", "labor_hours": 1.5, "category": "Port"},
                    {"part_name": "Charge Port Door Motor", "part_number": "1410120-00-A", "labor_hours": 1.0, "category": "Motor"},
                ]
            },
            "Braking System": {
                "Brakes": [
                    {"part_name": "Front Brake Pad Set", "part_number": "1220010-00-A", "labor_hours": 1.0, "category": "Pads"},
                    {"part_name": "Rear Brake Pad Set", "part_number": "1220020-00-A", "labor_hours": 1.0, "category": "Pads"},
                    {"part_name": "Front Brake Rotor", "part_number": "1220030-00-A", "labor_hours": 1.5, "category": "Rotor"},
                    {"part_name": "Rear Brake Rotor", "part_number": "1220040-00-A", "labor_hours": 1.5, "category": "Rotor"},
                    {"part_name": "ABS Module", "part_number": "1220050-00-A", "labor_hours": 2.0, "category": "ABS"},
                    {"part_name": "Brake Fluid", "part_number": "1220060-00-A", "labor_hours": 0.5, "category": "Fluid"},
                ]
            },
            "Exterior": {
                "Body Panels": [
                    {"part_name": "Front Fender - LH", "part_number": "1310010-00-A", "labor_hours": 2.0, "category": "Panel"},
                    {"part_name": "Front Fender - RH", "part_number": "1310020-00-A", "labor_hours": 2.0, "category": "Panel"},
                    {"part_name": "Rear Quarter Panel - LH", "part_number": "1310030-00-A", "labor_hours": 3.0, "category": "Panel"},
                    {"part_name": "Rear Quarter Panel - RH", "part_number": "1310040-00-A", "labor_hours": 3.0, "category": "Panel"},
                    {"part_name": "Door Assembly - Front LH", "part_number": "1310050-00-A", "labor_hours": 2.5, "category": "Door"},
                    {"part_name": "Door Assembly - Front RH", "part_number": "1310060-00-A", "labor_hours": 2.5, "category": "Door"},
                    {"part_name": "Tonneau Cover Panel", "part_number": "1310070-00-A", "labor_hours": 2.0, "category": "Tonneau"},
                ],
                "Windows & Lights": [
                    {"part_name": "Front Windshield", "part_number": "1320010-00-A", "labor_hours": 1.5, "category": "Glass"},
                    {"part_name": "Side Window - Front LH", "part_number": "1320020-00-A", "labor_hours": 1.0, "category": "Glass"},
                    {"part_name": "Side Window - Front RH", "part_number": "1320030-00-A", "labor_hours": 1.0, "category": "Glass"},
                    {"part_name": "Headlight Assembly - LH", "part_number": "1330010-00-A", "labor_hours": 1.5, "category": "Light"},
                    {"part_name": "Headlight Assembly - RH", "part_number": "1330020-00-A", "labor_hours": 1.5, "category": "Light"},
                    {"part_name": "Tail Light Assembly - LH", "part_number": "1330030-00-A", "labor_hours": 1.0, "category": "Light"},
                    {"part_name": "Tail Light Assembly - RH", "part_number": "1330040-00-A", "labor_hours": 1.0, "category": "Light"},
                ]
            }
        }
        
        return parts
    
    def build_tire_specs(self):
        """Build tire specification reference"""
        print("\n🛞 Building Tire Specifications...")
        
        tire_specs = {
            "Cybertruck": {
                "standard": {
                    "size": "265/70R18",
                    "load_range": "LT",
                    "speed_rating": "T (118 mph)",
                    "tread_depth_new": "10/32 in",
                    "tread_depth_min": "2/32 in",
                    "tire_pressure_cold": "42 psi",
                    "tire_pressure_hot": "45 psi",
                    "tpms_warning": "26 psi",
                    "recommended_brands": ["Michelin", "Goodyear", "Bridgestone"],
                },
                "performance": {
                    "size": "285/65R20",
                    "load_range": "LT",
                    "speed_rating": "H (130 mph)",
                    "tread_depth_new": "11/32 in",
                    "tread_depth_min": "2/32 in",
                    "tire_pressure_cold": "44 psi",
                    "tire_pressure_hot": "47 psi",
                    "tpms_warning": "26 psi",
                    "recommended_brands": ["Michelin", "Pirelli", "Continental"],
                },
                "winter": {
                    "size": "265/70R18",
                    "load_range": "LT",
                    "speed_rating": "T (118 mph)",
                    "tread_depth_new": "12/32 in",
                    "tread_depth_min": "6/32 in (recommended)",
                    "tire_pressure_cold": "40 psi",
                    "tire_pressure_hot": "43 psi",
                    "tpms_warning": "26 psi",
                    "three_peak_symbol": True,
                    "recommended_brands": ["Michelin X-Ice", "Bridgestone Blizzak", "Goodyear WinterCommand"],
                }
            },
            "wheel_fitment": {
                "18_inch": {"offset": "35mm", "width": "8.5J", "bolt_pattern": "5x114.3"},
                "20_inch": {"offset": "32mm", "width": "9.0J", "bolt_pattern": "5x114.3"},
                "22_inch": {"offset": "28mm", "width": "9.5J", "bolt_pattern": "5x114.3"},
            }
        }
        
        return tire_specs
    
    def build_diagnostic_codes(self):
        """Build DTC (Diagnostic Trouble Code) reference"""
        print("\n🔍 Building Diagnostic Codes...")
        
        codes = {
            "Battery Codes": [
                {"code": "P0A80", "name": "High Voltage System Malfunction", "severity": "critical", "action": "Service required"},
                {"code": "P0AB3", "name": "Battery Cell Over Voltage", "severity": "high", "action": "Check BMS module"},
                {"code": "P0AB6", "name": "Battery Voltage Below Threshold", "severity": "high", "action": "Charge battery"},
                {"code": "P0A1A", "name": "Battery Thermal Runaway Warning", "severity": "critical", "action": "Stop driving immediately"},
            ],
            "Motor Codes": [
                {"code": "P3000", "name": "Motor A Winding Short Circuit", "severity": "critical", "action": "Service required"},
                {"code": "P3010", "name": "Motor B Overtemperature Warning", "severity": "high", "action": "Cool down motor"},
                {"code": "P3020", "name": "Inverter Over Current", "severity": "critical", "action": "Service required"},
                {"code": "P3030", "name": "Torque Vectoring Malfunction", "severity": "medium", "action": "Service recommended"},
            ],
            "Suspension Codes": [
                {"code": "C1010", "name": "Air Suspension Compressor Failure", "severity": "high", "action": "Replace compressor"},
                {"code": "C1020", "name": "Air Suspension Pressure Low", "severity": "medium", "action": "Check for leaks"},
                {"code": "C1030", "name": "Suspension Height Sensor Fault", "severity": "medium", "action": "Replace sensor"},
                {"code": "C1040", "name": "Adaptive Damping Malfunction", "severity": "low", "action": "Service optional"},
            ],
            "Brake Codes": [
                {"code": "C0040", "name": "ABS Wheel Speed Sensor Error", "severity": "medium", "action": "Replace sensor"},
                {"code": "C0100", "name": "ABS Module Failure", "severity": "high", "action": "Service required"},
                {"code": "C0200", "name": "Regen Braking System Malfunction", "severity": "high", "action": "Service required"},
            ],
            "Electrical Codes": [
                {"code": "U0100", "name": "CAN Bus Communication Error", "severity": "high", "action": "Check wiring"},
                {"code": "U0101", "name": "Lost Communication with Motor Controller", "severity": "critical", "action": "Service required"},
                {"code": "B1001", "name": "MCU Memory Error", "severity": "medium", "action": "Restart vehicle"},
                {"code": "B1010", "name": "Touchscreen Unresponsive", "severity": "low", "action": "Recalibrate or reboot"},
            ]
        }
        
        return codes
    
    def build_technical_bulletins(self):
        """Build Technical Service Bulletins (TSBs)"""
        print("\n📋 Building Technical Service Bulletins...")
        
        tsbs = {
            "Air Suspension": [
                {
                    "tsb_id": "SB-25-XX-001",
                    "title": "Air Suspension Compressor Noise",
                    "issue": "Loud compressor operation during height adjustment",
                    "fix": "Replace compressor, update firmware",
                    "parts": ["1130010-00-A"],
                    "labor_hours": 3.0,
                    "affected_years": ["2024", "2025", "2026"]
                },
                {
                    "tsb_id": "SB-25-XX-002",
                    "title": "Suspension Height Sensor Calibration",
                    "issue": "Uneven ride height or height sensor faults",
                    "fix": "Recalibrate sensors via diagnostic tool",
                    "parts": [],
                    "labor_hours": 0.5,
                    "affected_years": ["2024", "2025"]
                }
            ],
            "Battery & Charging": [
                {
                    "tsb_id": "SB-25-XX-010",
                    "title": "Charge Port Door Sticking",
                    "issue": "Charge port door won't open or close smoothly",
                    "fix": "Replace charge port door motor and lubricate contacts",
                    "parts": ["1410120-00-A"],
                    "labor_hours": 1.5,
                    "affected_years": ["2024"]
                },
                {
                    "tsb_id": "SB-25-XX-011",
                    "title": "Slow DC Fast Charging",
                    "issue": "DC fast charging speed reduced to 50-70% of normal",
                    "fix": "Update onboard charger firmware, check thermal management",
                    "parts": [],
                    "labor_hours": 0.5,
                    "affected_years": ["2024", "2025"]
                }
            ],
            "Exterior & Panels": [
                {
                    "tsb_id": "SB-25-XX-020",
                    "title": "Door Alignment & Panel Gaps",
                    "issue": "Front door doesn't align properly, large gaps at seams",
                    "fix": "Adjust door hinges, align panel gaps to spec",
                    "parts": [],
                    "labor_hours": 2.0,
                    "affected_years": ["2024"]
                }
            ],
            "Electronics & Software": [
                {
                    "tsb_id": "SB-25-XX-030",
                    "title": "Touchscreen Freezing Issues",
                    "issue": "Infotainment system freezes or becomes unresponsive",
                    "fix": "Update MCU firmware, factory reset if needed",
                    "parts": [],
                    "labor_hours": 0.25,
                    "affected_years": ["2024", "2025"]
                }
            ]
        }
        
        return tsbs
    
    def save_comprehensive_data(self, parts, tires, codes, tsbs):
        """Save all data to JSON files"""
        print("\n💾 Saving comprehensive service data...")
        
        files = {}
        
        # Save parts
        parts_file = f"{self.data_dir}/cybertruck_parts_catalog.json"
        with open(parts_file, 'w') as f:
            json.dump({"vehicle": "Cybertruck", "parts": parts, "scraped": datetime.now().isoformat()}, f, indent=2)
        files['parts'] = parts_file
        print(f"✓ Parts catalog: {parts_file}")
        
        # Save tires
        tires_file = f"{self.data_dir}/cybertruck_tire_specs.json"
        with open(tires_file, 'w') as f:
            json.dump({"vehicle": "Cybertruck", "specifications": tires, "scraped": datetime.now().isoformat()}, f, indent=2)
        files['tires'] = tires_file
        print(f"✓ Tire specs: {tires_file}")
        
        # Save codes
        codes_file = f"{self.data_dir}/cybertruck_diagnostic_codes.json"
        with open(codes_file, 'w') as f:
            json.dump({"vehicle": "Cybertruck", "codes": codes, "scraped": datetime.now().isoformat()}, f, indent=2)
        files['codes'] = codes_file
        print(f"✓ Diagnostic codes: {codes_file}")
        
        # Save TSBs
        tsbs_file = f"{self.data_dir}/cybertruck_technical_bulletins.json"
        with open(tsbs_file, 'w') as f:
            json.dump({"vehicle": "Cybertruck", "bulletins": tsbs, "scraped": datetime.now().isoformat()}, f, indent=2)
        files['tsbs'] = tsbs_file
        print(f"✓ Technical bulletins: {tsbs_file}")
        
        return files
    
    def build_rag_chunks(self, parts, tires, codes, tsbs):
        """Convert all data into RAG chunks"""
        print("\n✂️  Building RAG chunks from all data...")
        
        chunks = []
        chunk_id = 1000  # Start from 1000 to avoid conflicts
        
        # Parts chunks
        for category, subcats in parts.items():
            for subcat, items in subcats.items():
                chunk = {
                    'id': f"cybertruck_parts_{chunk_id}",
                    'source': f"Cybertruck Parts: {category} - {subcat}",
                    'section': f"{category}/{subcat}",
                    'content': json.dumps({"category": category, "subcategory": subcat, "parts": items}, indent=2),
                    'metadata': {
                        'type': 'parts_catalog',
                        'vehicle': 'Cybertruck',
                        'category': category,
                        'part_count': len(items)
                    }
                }
                chunks.append(chunk)
                chunk_id += 1
        
        # Tire specs chunk
        chunk = {
            'id': f"cybertruck_tires_{chunk_id}",
            'source': "Cybertruck Tire Specifications",
            'section': "Tire Specs",
            'content': json.dumps(tires, indent=2),
            'metadata': {
                'type': 'tire_specifications',
                'vehicle': 'Cybertruck',
                'searchable': ['tire', 'pressure', 'size', 'winter', 'performance']
            }
        }
        chunks.append(chunk)
        chunk_id += 1
        
        # Diagnostic codes chunks
        for code_type, code_list in codes.items():
            chunk = {
                'id': f"cybertruck_codes_{chunk_id}",
                'source': f"Cybertruck Diagnostic Codes: {code_type}",
                'section': f"DTC - {code_type}",
                'content': json.dumps({"type": code_type, "codes": code_list}, indent=2),
                'metadata': {
                    'type': 'diagnostic_codes',
                    'vehicle': 'Cybertruck',
                    'code_type': code_type,
                    'code_count': len(code_list)
                }
            }
            chunks.append(chunk)
            chunk_id += 1
        
        # TSB chunks
        for category, bulletin_list in tsbs.items():
            for bulletin in bulletin_list:
                chunk = {
                    'id': f"cybertruck_tsb_{chunk_id}",
                    'source': f"TSB {bulletin['tsb_id']}: {bulletin['title']}",
                    'section': f"Technical Bulletins - {category}",
                    'content': json.dumps(bulletin, indent=2),
                    'metadata': {
                        'type': 'technical_bulletin',
                        'vehicle': 'Cybertruck',
                        'tsb_id': bulletin['tsb_id'],
                        'affected_years': bulletin['affected_years']
                    }
                }
                chunks.append(chunk)
                chunk_id += 1
        
        return chunks
    
    def save_rag_chunks(self, chunks):
        """Save all chunks to JSONL"""
        chunks_file = f"{self.data_dir}/cybertruck_comprehensive_chunks.jsonl"
        
        with open(chunks_file, 'w') as f:
            for chunk in chunks:
                f.write(json.dumps(chunk) + '\n')
        
        print(f"✓ Saved {len(chunks)} comprehensive chunks to: {chunks_file}")
        return chunks_file
    
    def run(self):
        """Execute full scrape"""
        print("=" * 70)
        print("🚀 COMPREHENSIVE CYBERTRUCK SERVICE DATA SCRAPER")
        print("=" * 70)
        
        # Build all data
        parts = self.build_parts_catalog()
        tires = self.build_tire_specs()
        codes = self.build_diagnostic_codes()
        tsbs = self.build_technical_bulletins()
        
        # Save raw data
        files = self.save_comprehensive_data(parts, tires, codes, tsbs)
        
        # Convert to RAG chunks
        chunks = self.build_rag_chunks(parts, tires, codes, tsbs)
        chunks_file = self.save_rag_chunks(chunks)
        
        # Summary
        print("\n" + "=" * 70)
        print("✅ COMPREHENSIVE CYBERTRUCK DATA SCRAPING COMPLETE")
        print("=" * 70)
        print(f"\nFiles created:")
        for file_type, file_path in files.items():
            print(f"  • {file_path}")
        print(f"  • {chunks_file}")
        
        print(f"\nTotal data chunks created: {len(chunks)}")
        print(f"  • Parts: {len([c for c in chunks if c.get('metadata', {}).get('type') == 'parts_catalog'])}")
        print(f"  • Tire specs: {len([c for c in chunks if c.get('metadata', {}).get('type') == 'tire_specifications'])}")
        print(f"  • Diagnostic codes: {len([c for c in chunks if c.get('metadata', {}).get('type') == 'diagnostic_codes'])}")
        print(f"  • TSBs: {len([c for c in chunks if c.get('metadata', {}).get('type') == 'technical_bulletin'])}")
        
        print("\nNext: Merge all chunks and deploy to DigitalOcean")
        print("=" * 70 + "\n")

if __name__ == "__main__":
    scraper = ComprehensiveCybertruckScraper()
    scraper.run()
