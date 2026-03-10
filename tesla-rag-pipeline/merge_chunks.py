#!/usr/bin/env python3
"""
Merge all chunk sources into unified RAG dataset
"""

import json
import os

def merge_chunks():
    """Combine all JSONL chunk files"""
    print("=" * 70)
    print("🔗 MERGING ALL CHUNK SOURCES")
    print("=" * 70)
    
    chunk_files = [
        "./data/chunks_flows.jsonl",           # Original diagnostic flows
        "./data/cybertruck_service_chunks.jsonl"  # Cybertruck service sections
    ]
    
    all_chunks = []
    total_lines = 0
    
    for chunk_file in chunk_files:
        if os.path.exists(chunk_file):
            print(f"\n📚 Reading {chunk_file}...")
            with open(chunk_file) as f:
                for line in f:
                    chunk = json.loads(line)
                    all_chunks.append(chunk)
                    total_lines += 1
            print(f"  ✓ Loaded {total_lines} total chunks so far")
        else:
            print(f"  ⚠️  {chunk_file} not found")
    
    # Save merged file
    print(f"\n💾 Saving merged chunks...")
    merged_file = "./data/all_chunks_merged.jsonl"
    
    with open(merged_file, 'w') as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk) + '\n')
    
    print(f"✓ Merged {len(all_chunks)} chunks into {merged_file}")
    
    # Create summary
    summary = {
        "total_chunks": len(all_chunks),
        "sources": {
            "diagnostic_flows": len([c for c in all_chunks if c.get('metadata', {}).get('type') == 'diagnostic_flow']),
            "cybertruck_service": len([c for c in all_chunks if c.get('metadata', {}).get('vehicle') == 'Cybertruck']),
        },
        "file": merged_file
    }
    
    print("\n" + "=" * 70)
    print("✅ MERGE COMPLETE")
    print("=" * 70)
    print(f"\nTotal chunks: {summary['total_chunks']}")
    print(f"  • Diagnostic flows: {summary['sources']['diagnostic_flows']}")
    print(f"  • Cybertruck service sections: {summary['sources']['cybertruck_service']}")
    print(f"\nMerged file: {merged_file}")
    print("\nNext: Deploy merged RAG to DigitalOcean")
    print("=" * 70 + "\n")
    
    return merged_file, summary

if __name__ == "__main__":
    merge_chunks()
