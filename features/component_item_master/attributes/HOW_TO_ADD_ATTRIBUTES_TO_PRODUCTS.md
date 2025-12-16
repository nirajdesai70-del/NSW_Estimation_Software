> Source: source_snapshot/HOW_TO_ADD_ATTRIBUTES_TO_PRODUCTS.md
> Bifurcated into: features/component_item_master/attributes/HOW_TO_ADD_ATTRIBUTES_TO_PRODUCTS.md
> Module: Component / Item Master > Attributes
> Date: 2025-12-17 (IST)

# How to See Products and Add Attributes

## 📍 Where to Find Products

### Option 1: Generic Products (ProductType = 1)
**Route:** `/generic` or click "Generic" in the menu  
**Page:** Generic Product List  
**Edit Page:** `/generic/{id}/edit` (Generic Product Edit)

### Option 2: Specific Products (ProductType = 2)
**Route:** `/product` or click "Product" in the menu  
**Page:** Product List  
**Edit Page:** `/product/{id}/edit` (Specific Product Edit)

---

## 🎯 How to Add Attributes to a Product

### Step 1: Ensure Attributes Exist with Proper Mapping

1. **Go to Attribute Master**
   - Route: `/attribute` or click "Attribute" in menu
   - Click "Add New Attribute" (+ icon)

2. **Create an Attribute**
   - Fill in: Name (e.g., "Voltage Rating"), Code (e.g., "VOLT"), Unit (e.g., "V")
   - Select ValueType: number, text, or enum
   - **IMPORTANT:** Add at least one mapping:
     - Select **Category** (required)
     - Optionally select **SubCategory**
     - Optionally select **Item/ProductType**
   - Click "Save"

3. **Verify Mapping**
   - The attribute must be mapped to the same Category (and optionally SubCategory/Item) as your product
   - Example: If product is in "ACB" category, attribute must have mapping for "ACB" category

---

### Step 2: Edit the Product

1. **Navigate to Product List**
   - Go to `/generic` (for Generic Products) or `/product` (for Specific Products)
   - Find your product in the list
   - Click the **Edit** button (pencil icon)

2. **Scroll to "Product Attributes" Section**
   - On the product edit page, scroll down past the basic fields
   - You'll see a section titled **"Product Attributes"**
   - This section shows all applicable attributes based on the product's Category/SubCategory/Item

---

### Step 3: Add/Edit Attribute Values

1. **Find the Attribute**
   - The table shows all applicable attributes
   - Each row has:
     - **Attribute Name** (and Code)
     - **Unit** (e.g., "V", "A", "kW")
     - **Value** input field
     - **Display Value** input field
     - **Type** badge (Number/Text/Enum)

2. **Enter the Value**
   - Click in the **Value** field
   - Enter the value (e.g., "415" for voltage)
   - **For number attributes:** Only numeric values allowed
   - **For text attributes:** Any text allowed

3. **Display Value (Auto-Formatted)**
   - When you click away from the Value field, **Display Value** auto-fills
   - Example: Value = "415", Unit = "V" → Display Value = "415 V"
   - You can override the Display Value with a custom format if needed

4. **Save the Product**
   - Click the **Save** button at the bottom
   - Attribute values are saved with the product

---

## 🔍 Troubleshooting

### "No applicable attributes found"
**Problem:** The attributes section shows "No applicable attributes found"

**Solutions:**
1. **Check Attribute Mapping:**
   - Go to `/attribute` and edit the attribute
   - Verify it has a mapping for your product's Category
   - Add mapping if missing

2. **Check Product Category:**
   - On the product edit page, verify the Category is set correctly
   - Attributes are matched based on Category/SubCategory/Item

3. **Create Attribute Mapping:**
   - If no attributes exist for this Category, create one:
     - Go to Attribute Master
     - Create new attribute
     - Add mapping for the product's Category

---

### "Attribute doesn't appear in the list"
**Problem:** You created an attribute but it doesn't show on the product edit page

**Check:**
1. Attribute has mapping for product's Category? ✅
2. Attribute is Active (IsActive = 1)? ✅
3. Product's Category matches attribute mapping? ✅
4. Refresh the product edit page after creating attribute

---

### "Can't enter text in number attribute"
**Problem:** Getting error when entering text in a number attribute

**Solution:**
- Number attributes only accept numeric values
- Check the attribute's ValueType in Attribute Master
- Use numeric values only (e.g., "415" not "four hundred")

---

## 📋 Quick Reference

### Routes:
- **Attribute Master:** `/attribute`
- **Generic Products:** `/generic`
- **Specific Products:** `/product`

### Key Pages:
- **Create Attribute:** `/attribute/create`
- **Edit Attribute:** `/attribute/{id}/edit`
- **Edit Generic Product:** `/generic/{id}/edit`
- **Edit Specific Product:** `/product/{id}/edit`

### Attribute Flow:
```
1. Create Attribute → Add Category Mapping
2. Edit Product → Scroll to Attributes Section
3. Enter Values → Auto-format Display Value
4. Save Product → Attributes Saved
```

---

## ✨ Tips

1. **Auto-Formatting:** Display Value auto-fills when you leave the Value field. You can override it with custom format.

2. **Multiple Attributes:** You can assign multiple attributes to one product. Just fill in the values you need.

3. **Optional Values:** Attributes are optional. You can leave values empty if not applicable.

4. **Number Validation:** Number attributes validate on blur. Invalid numbers show an alert.

5. **Category Matching:** Attributes must be mapped to the product's Category (at minimum) to appear.


