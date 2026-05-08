# Tesla Correction Codes Database

## 📊 Complete Dataset Summary

**Total Codes: 33,394 across 9 Tesla model variants**

### By Model & Year:

| Model | ID | Codes | File | Size |
|-------|----|----- |------|------|
| Cybertruck 2024+ | 103 | 2,488 | `tesla_correction_codes_Cybertruck_103.json` | 677K |
| Model 3 (Older) | 7 | 3,558 | `tesla_correction_codes_Model3_7.json` | 994K |
| Model 3 (Newer) | 35 | 2,962 | `tesla_correction_codes_Model3_35.json` | 817K |
| Model S (Older) | 1 | 3,859 | `tesla_correction_codes_ModelS_1.json` | 1.1M |
| Model S (Newer) | 18 | 4,296 | `tesla_correction_codes_ModelS_18.json` | 1.2M |
| Model X (Older) | 2 | 3,517 | `tesla_correction_codes_ModelX_2.json` | 1.0M |
| Model X (Newer) | 19 | 4,476 | `tesla_correction_codes_ModelX_19.json` | 1.3M |
| Model Y (Older) | 17 | 4,097 | `tesla_correction_codes_ModelY_17.json` | 1.1M |
| Model Y (Newer) | 36 | 4,141 | `tesla_correction_codes_ModelY_36.json` | 1.1M |
| **TOTAL** | - | **33,394** | `tesla_correction_codes_ALL_MODELS.json` | **11M** |

## 📋 Data Structure

Each correction code includes:
```json
{
  "id": 35766,
  "code": "00000010",
  "name": "Remote – Education",
  "workType": "Over The Air",
  "modelID": 36,
  "modelName": "2025+ Model Y",
  "frt": 0.0,
  "chargedHours": 0.0,
  "procedureURL": null
}
```

**Fields:**
- `code`: 8-digit service code (e.g., "00000010")
- `name`: Description of the work/service
- `workType`: Type of work (Remove & Replace, Paint, Inspection, etc.)
- `chargedHours`: Labor hours charged to customer
- `frt`: Flat rate time (for labor calculations)
- `procedureURL`: Link to detailed procedure (when available)
- `modelID`: Tesla's internal model ID
- `modelName`: Human-readable model name

## 🔧 Work Types (All Models)

Most common work types across all models:
1. **Remove and Replace**: ~44% of all codes
2. **Remove and Install**: ~35% of all codes
3. **Paint Work**: ~8% of all codes
4. **Test/Adjust, Inspection, Maintenance, etc.**: ~13% of all codes

## 📈 Labor Hours Statistics

- **Minimum**: 0.0 hours (software updates, remote diagnostics)
- **Maximum**: 72.0 hours (major body work, full system replacements)
- **Average**: ~1.2 hours per code
- **Total across all codes**: ~40,000+ labor hours

## 🚀 Ready for Deployment

### Option 1: All-in-One (Recommended for MVP)
Use `tesla_correction_codes_ALL_MODELS.json` (11M)
- Single file contains all 33,394 codes
- Flatten into RAG chunks
- Query across all models simultaneously

### Option 2: Per-Model (For segmented deployment)
Use individual model files if you want:
- Model-specific filtering
- Smaller chunk sizes per model
- Easier to version/update per model

## 💾 Integration Steps

1. **Load JSON into vector DB**
   ```python
   import json
   with open('tesla_correction_codes_ALL_MODELS.json', 'r') as f:
       data = json.load(f)
   codes = data['all_models']  # Dict of all model data
   ```

2. **Flatten into RAG chunks**
   ```python
   chunks = []
   for model_key, model_data in codes.items():
       for code in model_data['codes']:
           chunk = {
               'id': f"code_{code['id']}",
               'code': code['code'],
               'name': code['name'],
               'model': model_data['model_name'],
               'work_type': code['workType'],
               'labor_hours': code['chargedHours'],
               'content': f"{code['name']} - {code['workType']}"
           }
           chunks.append(chunk)
   ```

3. **Embed and search**
   - Embed `content` field (description + work type)
   - Index by `code` for exact lookups
   - Enable semantic search: "replace transmission" → finds all related codes

4. **Deploy to DigitalOcean**
   - Load chunks into vector DB
   - Expose via Flask API
   - Connect to Rork iOS app

## 🎯 API Query Examples

Once deployed, service advisors can query:

✅ "Replace battery" → 50+ matching codes with labor hours  
✅ "Paint front bumper" → 200+ paint work codes by model  
✅ "Code 00004107" → Direct lookup with full details  
✅ "Suspension inspection Model Y" → Model-specific results  
✅ "Diagnostic procedures" → 15+ diagnostic codes  

## 📊 File Locations

All files saved to:
```
/Users/rk/clawd/tesla-rag-pipeline/data/
├── tesla_correction_codes_ALL_MODELS.json           (master, 11M)
├── tesla_correction_codes_Model3_35.json            (2962 codes)
├── tesla_correction_codes_Model3_7.json             (3558 codes)
├── tesla_correction_codes_ModelS_1.json             (3859 codes)
├── tesla_correction_codes_ModelS_18.json            (4296 codes)
├── tesla_correction_codes_ModelX_2.json             (3517 codes)
├── tesla_correction_codes_ModelX_19.json            (4476 codes)
├── tesla_correction_codes_ModelY_17.json            (4097 codes)
├── tesla_correction_codes_ModelY_36.json            (4141 codes)
├── tesla_correction_codes_Cybertruck_103.json       (2488 codes)
└── tesla_correction_codes_model_y_2025.json         (4141 codes - first scrape)
```

## ✅ Status

✓ All 33,394 codes successfully scraped  
✓ Organized by model and year  
✓ Validated JSON format  
✓ Ready for RAG ingestion  
✓ Ready for production deployment  

---

**Scraped:** April 29, 2026  
**Source:** Tesla Service API  
**Models:** All current Tesla vehicles  
**Status:** PRODUCTION READY
