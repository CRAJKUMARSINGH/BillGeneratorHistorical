# 📦 How to Archive Apps - Simple Guide

## Method 1: Automatic (Recommended) ⭐

### Step 1: Open Command Prompt
```
Press Windows Key + R
Type: cmd
Press Enter
```

### Step 2: Navigate to Main App
```bash
cd C:\Users\Rajkumar\Stream-Bill-App_Main
```

### Step 3: Run Archive Script
```bash
python scripts\consolidate_apps.py
```

### Step 4: Confirm
```
When asked "Continue? (yes/no):"
Type: yes
Press Enter
```

### What Happens:
1. ✅ Creates folder: `C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\`
2. ✅ Copies all 7 apps to archive folder
3. ✅ Creates detailed report
4. ✅ Takes 5-10 minutes
5. ✅ Original folders stay untouched

---

## Method 2: Manual (If you prefer)

### Step 1: Create Archive Folder
```bash
mkdir C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED
```

### Step 2: Copy Each App
```bash
# Copy app 1
xcopy "C:\Users\Rajkumar\Stream-Bill-FIRST-ONE" "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Stream-Bill-FIRST-ONE" /E /I /H

# Copy app 2
xcopy "C:\Users\Rajkumar\Stream-Bill-Generator-SAPNA" "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Stream-Bill-Generator-SAPNA" /E /I /H

# Copy app 3
xcopy "C:\Users\Rajkumar\Stream-Bill-INIT-PY" "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Stream-Bill-INIT-PY" /E /I /H

# Copy app 4
xcopy "C:\Users\Rajkumar\Stream-Bill-generator-main" "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Stream-Bill-generator-main" /E /I /H

# Copy app 5
xcopy "C:\Users\Rajkumar\Stream-Bill-generator-main2" "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Stream-Bill-generator-main2" /E /I /H

# Copy app 6
xcopy "C:\Users\Rajkumar\Streamlit_Bill_Historical" "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Streamlit_Bill_Historical" /E /I /H

# Copy app 7
xcopy "C:\Users\Rajkumar\Streamlit_Bill_New" "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Streamlit_Bill_New" /E /I /H
```

**Flags Explained**:
- `/E` = Copy all subdirectories (including empty ones)
- `/I` = Create destination folder if it doesn't exist
- `/H` = Copy hidden and system files too

---

## Method 3: Using Windows Explorer (Easiest)

### Step 1: Create Archive Folder
1. Open File Explorer
2. Navigate to `C:\Users\Rajkumar\`
3. Right-click → New → Folder
4. Name it: `Stream-Bill-Apps-ARCHIVED`

### Step 2: Copy Apps
For each of the 7 apps:
1. Right-click on app folder
2. Click "Copy"
3. Open `Stream-Bill-Apps-ARCHIVED` folder
4. Right-click → "Paste"
5. Wait for copy to complete

**Apps to copy**:
- Stream-Bill-FIRST-ONE
- Stream-Bill-Generator-SAPNA
- Stream-Bill-INIT-PY
- Stream-Bill-generator-main
- Stream-Bill-generator-main2
- Streamlit_Bill_Historical
- Streamlit_Bill_New

---

## After Archiving

### Verify Archive
```bash
# Check archive exists
dir C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED

# Should show 7 folders
```

### Test Main App
```bash
cd C:\Users\Rajkumar\Stream-Bill-App_Main
python scripts\test_pdf_generation_comprehensive.py
```

**Expected**: 125/125 tests pass ✅

### Delete Originals (Optional - Wait 1 Week)
**⚠️ ONLY after verifying everything works!**

```bash
# After 1 week of successful use
rmdir /s /q "C:\Users\Rajkumar\Stream-Bill-FIRST-ONE"
rmdir /s /q "C:\Users\Rajkumar\Stream-Bill-Generator-SAPNA"
rmdir /s /q "C:\Users\Rajkumar\Stream-Bill-INIT-PY"
rmdir /s /q "C:\Users\Rajkumar\Stream-Bill-generator-main"
rmdir /s /q "C:\Users\Rajkumar\Stream-Bill-generator-main2"
rmdir /s /q "C:\Users\Rajkumar\Streamlit_Bill_Historical"
rmdir /s /q "C:\Users\Rajkumar\Streamlit_Bill_New"
```

---

## To Restore (If Needed)

### Restore Single App
```bash
xcopy "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\[APP_NAME]" "C:\Users\Rajkumar\[APP_NAME]" /E /I /H
```

### Example:
```bash
xcopy "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Stream-Bill-FIRST-ONE" "C:\Users\Rajkumar\Stream-Bill-FIRST-ONE" /E /I /H
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| **Archive (Auto)** | `python scripts\consolidate_apps.py` |
| **Check Archive** | `dir C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED` |
| **Test Main App** | `python scripts\test_pdf_generation_comprehensive.py` |
| **Delete Original** | `rmdir /s /q "C:\Users\Rajkumar\[APP_NAME]"` |
| **Restore App** | `xcopy "[ARCHIVE]\[APP]" "C:\Users\Rajkumar\[APP]" /E /I /H` |

---

## ✅ Recommended: Use Method 1 (Automatic)

**Why?**
- ✅ Safest
- ✅ Creates detailed report
- ✅ Verifies each step
- ✅ Handles errors
- ✅ Timestamps everything
- ✅ One command

**Just run**:
```bash
cd C:\Users\Rajkumar\Stream-Bill-App_Main
python scripts\consolidate_apps.py
```

Type `yes` when asked. Done! 🎉
