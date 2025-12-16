> Source: source_snapshot/PROJECT_QUOTATION_API_USAGE.md
> Bifurcated into: features/project/quotation_linkage/PROJECT_QUOTATION_API_USAGE.md
> Module: Project > Quotation Linkage
> Date: 2025-12-17 (IST)

# Project Quotation API - Usage Guide

## Overview
This document explains how to retrieve full project quotation details from the database, either for a single project or by searching for projects by name.

## Available Endpoints

### 1. Search Projects by Name
**URL:** `GET /quotation/search-projects?q={search_term}`

**Description:** Search for projects by name, location, or client name.

**Example:**
```
GET /quotation/search-projects?q=essenn
GET /quotation/search-projects?q=MARSHALLING
```

**Response:**
```json
{
    "success": true,
    "message": "Projects found: 2",
    "data": [
        {
            "ProjectId": 8,
            "Name": "MARSHALLING YARD_PR-28027512",
            "Location": "HAZIRA SURAT",
            "ClientName": "Arcelor Mittal Nippon Steel India Ltd",
            "QuotationCount": 10
        }
    ]
}
```

### 2. Get Full Project Quotation Details
**URL:** `GET /quotation/project/{projectIdOrName}`

**Description:** Get complete quotation details for a project, including all panels, BOMs, and items.

**Parameters:**
- `projectIdOrName`: Project ID (numeric) or Project Name (partial match)

**Examples:**
```
GET /quotation/project/8
GET /quotation/project/MARSHALLING
GET /quotation/project/essenn
```

**Response Structure:**
```json
{
    "success": true,
    "message": "Project quotation details retrieved successfully",
    "data": {
        "ProjectId": 8,
        "ProjectName": "MARSHALLING YARD_PR-28027512",
        "Location": "HAZIRA SURAT",
        "ClientName": "Arcelor Mittal Nippon Steel India Ltd",
        "TotalQuotations": 10,
        "Quotations": [
            {
                "QuotationId": 37,
                "QuotationNo": "220420001",
                "ClientName": "Arcelor Mittal Nippon Steel India Ltd",
                "CreatedAt": "2022-04-20 18:01:50",
                "Panels": [
                    {
                        "QuotationSaleId": 123,
                        "SaleCustomName": "Panel 1",
                        "Qty": 1,
                        "Rate": 1000.00,
                        "Amount": 1000.00,
                        "Margin": 10,
                        "MarginAmount": 1100.00,
                        "MarginTotal": 1100.00,
                        "BOMs": [
                            {
                                "QuotationSaleBomId": 456,
                                "MasterBomId": 789,
                                "MasterBomName": "Main BOM",
                                "Qty": 1,
                                "Rate": 500.00,
                                "Amount": 500.00,
                                "Items": [
                                    {
                                        "QuotationSaleBomItemId": 789,
                                        "ProductId": 101,
                                        "ProductName": "Product Name",
                                        "CategoryId": 5,
                                        "MakeId": 10,
                                        "SeriesId": 15,
                                        "Description": "Product Description",
                                        "Remark": "Remarks",
                                        "SKU": "SKU123",
                                        "Qty": 2,
                                        "Rate": 250.00,
                                        "Discount": 5,
                                        "NetRate": 237.50,
                                        "Amount": 475.00
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
}
```

## Usage Examples

### Example 1: Search for "essenn" project
```bash
curl "http://127.0.0.1:8000/quotation/search-projects?q=essenn"
```

### Example 2: Get full details for Project ID 8
```bash
curl "http://127.0.0.1:8000/quotation/project/8"
```

### Example 3: Get full details by project name
```bash
curl "http://127.0.0.1:8000/quotation/project/MARSHALLING"
```

## Data Hierarchy

The response follows this hierarchy:
```
Project
  └── Quotations (multiple)
      └── Panels / Sale Items (multiple)
          └── BOMs / Feeders (multiple)
              └── Items / Products (multiple)
```

## Notes

1. **Search is case-insensitive** - "essenn", "Essenn", "ESSENN" will all match
2. **Partial matching** - Searching "MARSHALLING" will find "MARSHALLING YARD_PR-28027512"
3. **Only active records** - Only returns quotations, panels, BOMs, and items with `Status = 0`
4. **Memory limit** - Method sets memory limit to 256MB for large projects

## Current Database Status

**Search Results for "essenn":**
- Projects: 0 found
- Clients: 0 found

**Sample Projects Available:**
- Project ID 8: "MARSHALLING YARD_PR-28027512" (10 quotations)
- Project ID 15: "SMPS  PCC & APFC    PANEL"
- Project ID 16: "AGL CAPEX PROJECT"
- And more...

## Testing

You can test these endpoints using:
1. Browser: `http://127.0.0.1:8000/quotation/search-projects?q=essenn`
2. Browser: `http://127.0.0.1:8000/quotation/project/8`
3. cURL or Postman
4. JavaScript fetch() in browser console

