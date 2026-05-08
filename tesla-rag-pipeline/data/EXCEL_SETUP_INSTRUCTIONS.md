# Tesla Correction Codes - Excel Setup Instructions

## 📊 What to Do With These Files

Since we can't create native .xlsx files on this Mac, we provide CSV files that open perfectly in Excel with all the functionality you need.

### Option 1: Quick Start (Recommended)

**Use this file:**
- `Tesla_Correction_Codes_Master_with_Universal.csv`

**In Excel:**
1. Open the file in Excel
2. Select all data (Ctrl+A)
3. Click **Data** → **AutoFilter**
4. Use dropdown arrows to filter:
   - Filter by **Universal** column (YES/NO)
   - Filter by **Model** (Cybertruck, Model Y, etc.)
   - Filter by **Work_Type** (Remove and Replace, Paint, etc.)
   - Filter by **Labor_Hours** (find quick jobs vs. long jobs)

**Columns Available:**
- `Universal` - YES if code works on all models, NO if model-specific
- `Model` - Which Tesla model
- `Model_ID` - Tesla's internal ID
- `Code` - The 8-digit correction code
- `Description` - What the code does
- `Work_Type` - Type of work
- `Labor_Hours` - How long it takes
- `FRT` - Flat rate time

---

### Option 2: Separate Views (Organized)

**Universal codes only:**
- `Tesla_Correction_Codes_UNIVERSAL.csv` (330 codes used on ALL models)
  - Software updates, diagnostics, administrative codes
  - Same labor hours/procedure across all models

**Individual model codes:**
- `Tesla_CorrectionCodes_Cybertruck.csv`
- `Tesla_CorrectionCodes_Model3.csv`
- `Tesla_CorrectionCodes_ModelS.csv`
- `Tesla_CorrectionCodes_ModelX.csv`
- `Tesla_CorrectionCodes_ModelY.csv`

**How to use:**
1. Open `Tesla_Correction_Codes_UNIVERSAL.csv` for codes that work everywhere
2. Open specific model file when working on a customer's vehicle
3. Combine them mentally: "What codes are available for this job on this model?"

---

## 🎯 Common Work Scenarios

### Scenario 1: Customer brings in Cybertruck for service
1. Open `Tesla_CorrectionCodes_Cybertruck.csv`
2. Search (Ctrl+F) for the part they want replaced
3. Filter by `Work_Type` = "Remove and Replace"
4. Get the exact code and labor hours

### Scenario 2: Same service on different models
1. Open `Tesla_Correction_Codes_UNIVERSAL.csv` first
   - Check if the code is universal (same labor hours for all models)
2. If not found, open individual model files
   - Compare labor hours and procedures across models
   - Example: Battery replacement takes 3.2 hrs on Model Y, 4.0 hrs on Model S

### Scenario 3: Quick lookup of what code means
1. Use Find (Ctrl+F) in `Tesla_Correction_Codes_Master_with_Universal.csv`
2. Search by code number
3. See description, work type, labor hours, and which model it applies to

### Scenario 4: Find all paint work for Model S
1. Open `Tesla_Correction_Codes_ModelS.csv`
2. Filter `Work_Type` = "Paint Work"
3. View all paint codes and hours
4. Or use `Master_with_Universal.csv` and filter by both Model S AND Paint Work

---

## 📋 Universal Codes Breakdown (330 codes)

These work the same way on ALL Tesla models:

| Work Type | Count | Examples |
|-----------|-------|----------|
| Test/Adjust | 48 | Diagnostics, inspections, testing |
| Inspection | 36 | Pre-delivery, safety inspections |
| Remove and Replace | 36 | Generic parts (tires, brakes) |
| Restore | 23 | Cosmetic restoration |
| Fee | 20 | Administrative fees |
| Remove and Install | 19 | Installation codes |
| Maintenance | 17 | Maintenance procedures |
| General Diagnosis | 15 | Diagnostic procedures |
| Other | 116 | Sublet, retrofit, tire repair, paint, etc. |

**Key insight:** Most universal codes are diagnostic/administrative. They have the SAME labor hours across all models.

**Model-specific codes:** 10,141 unique codes (97% of all codes) that differ per model due to different architectures, parts, and procedures.

---

## 💡 Pro Tips for Excel

### Freeze the header row
1. Click cell A2
2. Go to **View** → **Freeze Panes**
3. Header row stays visible when scrolling

### Sort by labor hours
1. Click any cell in the data
2. Go to **Data** → **Sort**
3. Sort by `Labor_Hours` (ascending = quick jobs first)
4. Find 0-hour codes (admin/remote work)

### Custom filter
1. Click Data → **Advanced Filter**
2. Create complex filters like:
   - Model = "Cybertruck" AND Work_Type = "Paint Work" AND Labor_Hours < 2

### Add a helper column
1. Create new column "Scope"
2. Formula: =IF(D2<1,"Quick",IF(D2<4,"Medium","Long"))
3. Now you can see job scope at a glance

### Search/Replace
- Need to find all battery codes? Use Find (Ctrl+F)
- Search: "battery"
- Instantly see all matching codes across all models

---

## 🔄 How to Update Files

When I scrape new codes (quarterly or as needed):
1. I'll create new CSV files with timestamp
2. You can either:
   - Replace old files with new ones (keep in sync)
   - Keep multiple versions and compare changes

---

## 📱 Mobile Access

Want to use on your phone at the service bay?
1. Upload CSV to Google Drive or OneDrive
2. Open in Google Sheets or Excel Online
3. Use phone browser to search/filter while working

---

## ✅ File Locations

```
/Users/rk/clawd/tesla-rag-pipeline/data/

PRIMARY FILES (Use these):
├── Tesla_Correction_Codes_Master_with_Universal.csv    (Main - all codes)
├── Tesla_Correction_Codes_UNIVERSAL.csv                 (330 universal codes)

BY MODEL (Choose what you need):
├── Tesla_CorrectionCodes_Cybertruck.csv                 (2,488 codes)
├── Tesla_CorrectionCodes_Model3.csv                     (6,520 codes)
├── Tesla_CorrectionCodes_ModelS.csv                     (8,155 codes)
├── Tesla_CorrectionCodes_ModelX.csv                     (7,993 codes)
├── Tesla_CorrectionCodes_ModelY.csv                     (8,238 codes)

FOR MY LOOKUPS:
└── Tesla_Codes_Index.json                               (Fast search)
```

---

## 🆘 Troubleshooting

**Q: File is slow to load?**
A: The master file has 33k rows. Use individual model files instead for faster Excel performance.

**Q: Can't find a code?**
A: It might be model-specific. Try:
1. Searching the Universal file first
2. Then search the specific model file
3. Ask me to search - I can find it in seconds

**Q: Labor hours don't match what I expect?**
A: Different models may have different hours for the same service. Check both the universal file AND the model-specific file.

**Q: Want to convert to .xlsx?**
A: You can easily do this in Excel:
1. Open CSV file
2. File → Save As
3. Choose "Excel Workbook (.xlsx)"
4. Add tabs yourself or ask me

---

**Status:** ✅ Ready to use immediately
**Total Codes:** 33,394
**Universal Codes:** 330 (work on all models)
**Model-Specific:** 10,141 (97% vary by model)

---

Just open the CSV files in Excel and start searching!
