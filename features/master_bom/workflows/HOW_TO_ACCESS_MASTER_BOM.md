> Source: source_snapshot/HOW_TO_ACCESS_MASTER_BOM.md
> Bifurcated into: features/master_bom/workflows/HOW_TO_ACCESS_MASTER_BOM.md
> Module: Master BOM > Workflows
> Date: 2025-12-17 (IST)

# How to Access Master BOM Selection
## Step-by-Step Guide

**Issue:** Master BOM tab/selection not visible on Create Quotation page  
**Solution:** Master BOM is on the Step/Components page, NOT the Create page

---

## ✅ CORRECT FLOW

### **Step 1: Create Quotation (You're Here Now)**

**Current Page:** `/quotation/create`

**What to do:**
1. Fill in all required fields:
   - Client* ✅ (You have: "Arcelor Mittal Nippon Steel India Ltd")
   - Project* ✅ (You have: "MARSHALLING YARD_PR-28027512")
   - Contact Person* ✅ (You have: "Ms. Pratibha Jain")
   - Sales Person* (Select from dropdown)
   - Employee* (Select from dropdown)
   - Quotation No (Auto Generate is fine)

2. **Click "Save" button** (blue button with checkmark)

3. **After saving**, you'll be redirected to the quotation Edit page or list

---

### **Step 2: Go to Step/Components Page**

**After saving the quotation:**

1. **Option A:** If redirected to Edit page
   - Look for tabs: "Details" | "Step" | "Components"
   - Click **"Step"** or **"Components"** tab
   - URL will be: `/quotation/{id}/step`

2. **Option B:** If redirected to list
   - Find your quotation in the list
   - Click **"Edit"** button
   - Then click **"Step"** or **"Components"** tab
   - URL will be: `/quotation/{id}/step`

---

### **Step 3: Add Sale Item (Panel)**

**On the Step page:**

1. Look for button: **"+ Add Sale Item"** or **"Add More"**
   - Usually at the top of the panel area
   - Or below the Category/Make/Series table

2. **Click "+ Add Sale Item"**
   - A new panel row will appear
   - You'll see fields like: Name, Qty, etc.

---

### **Step 4: Add BOM Row (Where Master BOM Appears)**

**On the panel row:**

1. Look for a **"+" button** or **"Add BOM"** button
   - Usually on the left side of the panel row
   - Or in a BOM section

2. **Click the "+" button** to add a BOM row
   - A new BOM row will appear under the panel
   - This is where Master BOM dropdown appears!

---

### **Step 5: Select Master BOM**

**On the BOM row:**

1. You'll see a **dropdown** that says:
   - "Master BOM" (for standard BOMs)
   - "Proposal BOM" (for project-specific BOMs)

2. **Click the dropdown**
   - You'll see list of Master BOMs
   - Select your test Master BOM (e.g. `TEST-STD-ACB-INCOMER-1600A`)

3. **Items will load automatically** under the BOM row

---

## 📍 QUICK REFERENCE

```
Create Quotation Page (/quotation/create)
    ↓ [Save]
Edit Quotation Page (/quotation/{id}/edit)
    ↓ [Click "Step" tab]
Step/Components Page (/quotation/{id}/step)
    ↓ [Click "+ Add Sale Item"]
Panel Row Appears
    ↓ [Click "+" to add BOM]
BOM Row Appears
    ↓ [Master BOM dropdown appears here!]
Select Master BOM
    ↓ [Items load automatically]
✅ DONE!
```

---

## 🔍 WHAT TO LOOK FOR

### **On Step Page, you should see:**

1. **Top Section:**
   - Client Name, Project Name, Quotation No
   - Category/Make/Series table

2. **Panel Section:**
   - "+ Add Sale Item" button
   - Panel rows (if any exist)

3. **On Each Panel Row:**
   - Panel Name field
   - Qty field
   - "+" button (to add BOM)
   - "-" button (to remove panel)

4. **On Each BOM Row:**
   - Master BOM dropdown ← **THIS IS WHERE IT IS!**
   - Custom Name field
   - Qty field
   - Item rows below

---

## ⚠️ COMMON ISSUES

### **Issue 1: "I don't see Step tab"**
- **Solution:** Make sure you SAVED the quotation first
- The Step tab only appears after quotation is created

### **Issue 2: "I don't see Add Sale Item button"**
- **Solution:** Scroll down on the Step page
- The button might be below the Category/Make/Series table

### **Issue 3: "I don't see Master BOM dropdown"**
- **Solution:** 
  1. First add a Sale Item (panel)
  2. Then click "+" on the panel to add a BOM row
  3. Master BOM dropdown appears on the BOM row

---

## ✅ NEXT STEPS FOR YOU

1. **Complete the Create Quotation form:**
   - Select Sales Person*
   - Select Employee*
   - Click "Save"

2. **Go to Step page:**
   - Click "Step" or "Components" tab

3. **Add Sale Item:**
   - Click "+ Add Sale Item"

4. **Add BOM:**
   - Click "+" on the panel row

5. **Select Master BOM:**
   - Click Master BOM dropdown
   - Select your test Master BOM

6. **Verify items load**

---

**Status:** Ready to continue! ✅

