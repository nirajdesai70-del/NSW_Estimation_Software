⚠️ DEPRECATED FOR EXECUTION / REFERENCE ONLY / NOT EXECUTED: Do not implement directly. Canonical execution is Controller(thin) → BomEngine → Gate-0/R1/S1/R2/S2 evidence.

---

# Feeder BOM Round-0: Complete applyFeederTemplate() Method

**File:** docs/FEEDER_BOM/FEEDER_BOM_ROUND0_COMPLETE_METHOD.md  
**Version:** v1.0_2025-12-19  
**Status:** 📋 READY FOR REVIEW

---

## Purpose

This is the complete method structure for review before implementation. Apply this to: `app/Http/Controllers/QuotationV2Controller.php`

---

## Key Features

- Re-apply to same feeder (detects existing feeder)
- Clear-before-copy (soft delete Status=1 when reusing feeder)
- Writer loop (valid implementation via ProposalBomItemWriter gateway)
- Comprehensive audit logging

---

## Complete Method

```php
public function applyFeederTemplate(Request $request)
{
    DB::beginTransaction();
    try {
        // ============================================
        // 1. Validate input
        // ============================================
        $quotationId = $request->input('quotation_id');
        $quotationSaleId = $request->input('quotation_sale_id'); // Panel ID
        $templateId = $request->input('template_id'); // MasterBomId
        $feederName = $request->input('feeder_name'); // Feeder name/identifier
        
        // Validate required fields
        if (!$quotationId || !$quotationSaleId || !$templateId) {
            DB::rollBack();
            return response()->json([
                'success' => false,
                'message' => 'quotation_id, quotation_sale_id, and template_id are required',
            ], 400);
        }
        
        // ============================================
        // 2. Re-apply to same feeder (CRITICAL)
        // ============================================
        // Detect if a feeder with the same characteristics already exists
        // If exists → reuse it and clear-before-copy
        // If not → create new feeder
        
        $existingFeeder = QuotationSaleBom::where('QuotationId', $quotationId)
            ->where('QuotationSaleId', $quotationSaleId)
            ->where('MasterBomId', $templateId)
            ->where('MasterBomName', $feederName) // Adjust field name as needed (may be 'Name' or other)
            ->where('Level', 0)
            ->whereNull('ParentBomId')
            ->where('Status', 0)
            ->first();
        
        if ($existingFeeder) {
            // Reuse existing feeder
            $feederId = $existingFeeder->QuotationSaleBomId;
            $feederReused = true;
            
            \Log::info('Feeder Template Apply: Reusing existing feeder', [
                'feeder_id' => $feederId,
                'template_id' => $templateId,
                'quotation_id' => $quotationId,
                'quotation_sale_id' => $quotationSaleId,
            ]);
        } else {
            // Create new feeder (Level=0, ParentBomId=NULL)
            $feeder = QuotationSaleBom::create([
                'QuotationId' => $quotationId,
                'QuotationSaleId' => $quotationSaleId,
                'MasterBomId' => $templateId,
                'MasterBomName' => $feederName,
                'Level' => 0,
                'ParentBomId' => null,
                'Status' => 0,
                // Add other required fields as needed
                // 'created_at' => now(),
                // 'updated_at' => now(),
            ]);
            
            $feederId = $feeder->QuotationSaleBomId;
            $feederReused = false;
            
            \Log::info('Feeder Template Apply: Created new feeder', [
                'feeder_id' => $feederId,
                'template_id' => $templateId,
                'quotation_id' => $quotationId,
                'quotation_sale_id' => $quotationSaleId,
            ]);
        }
        
        // ============================================
        // 3. Clear-before-copy (only when reusing feeder)
        // ============================================
        // Soft delete existing items (Status=1) before copying template items
        // This prevents duplicate stacking on repeated apply operations
        
        $deletedCount = 0;
        if ($feederReused) {
            $deletedCount = QuotationSaleBomItem::where('QuotationSaleBomId', $feederId)
                ->where('Status', 0)
                ->update(['Status' => 1]);
            
            \Log::info('Feeder Template Apply: Cleared existing items', [
                'feeder_id' => $feederId,
                'template_id' => $templateId,
                'deleted_count' => $deletedCount,
                'timestamp' => now()->toIso8601String(),
            ]);
        }
        
        // ============================================
        // 4. Copy template items via writer gateway
        // ============================================
        // Uses writer->create() in loop (valid implementation)
        // Copy-never-link: creates new independent rows
        
        $writer = app(ProposalBomItemWriter::class);
        $createdItems = [];
        
        // Load template items (adjust based on your template structure)
        // This assumes MasterBomItem table; adjust if your template structure differs
        $templateItems = MasterBomItem::where('MasterBomId', $templateId)
            ->where('Status', 0)
            ->get();
        
        foreach ($templateItems as $templateItem) {
            // Create item via writer gateway
            $item = $writer->create([
                'QuotationSaleBomId' => $feederId,
                'ProductId' => $templateItem->ProductId, // May be generic (ProductType=1)
                'MakeId' => 0, // Transitional state (will be resolved later)
                'SeriesId' => 0, // Transitional state (will be resolved later)
                'Qty' => $templateItem->Qty ?? 1,
                // Copy other fields from templateItem as needed
                // 'Rate' => $templateItem->Rate ?? 0,
                // 'Discount' => $templateItem->Discount ?? 0,
                // etc.
            ], [
                'allowTransitionalState' => true, // Allow generic items (L1→L2 resolution)
            ]);
            
            $createdItems[] = $item;
        }
        
        // ============================================
        // 5. Audit logging
        // ============================================
        \Log::info('Feeder Template Apply: Completed', [
            'feeder_id' => $feederId,
            'template_id' => $templateId,
            'quotation_id' => $quotationId,
            'quotation_sale_id' => $quotationSaleId,
            'feeder_reused' => $feederReused,
            'rows_soft_deleted' => $deletedCount,
            'rows_inserted' => count($createdItems),
            'items_created' => array_map(function($item) {
                return [
                    'id' => $item->QuotationSaleBomItemId ?? null,
                    'product_id' => $item->ProductId ?? null,
                    'make_id' => $item->MakeId ?? null,
                    'series_id' => $item->SeriesId ?? null,
                ];
            }, $createdItems),
            'timestamp' => now()->toIso8601String(),
        ]);
        
        DB::commit();
        
        // ============================================
        // 6. Return response
        // ============================================
        return response()->json([
            'success' => true,
            'feeder_id' => $feederId,
            'template_id' => $templateId,
            'feeder_reused' => $feederReused,
            'deleted_count' => $deletedCount,
            'inserted_count' => count($createdItems),
            'message' => 'Feeder template applied successfully',
        ]);
        
    } catch (\Exception $e) {
        DB::rollBack();
        
        \Log::error('Feeder Template Apply: Error', [
            'quotation_id' => $quotationId ?? null,
            'template_id' => $templateId ?? null,
            'error' => $e->getMessage(),
            'trace' => $e->getTraceAsString(),
        ]);
        
        return response()->json([
            'success' => false,
            'message' => 'Failed to apply feeder template: ' . $e->getMessage(),
        ], 500);
    }
}
```

---

## Required Imports

```php
use App\Models\QuotationSaleBom;
use App\Models\QuotationSaleBomItem;
use App\Models\MasterBomItem;
use App\Services\ProposalBomItemWriter;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
```

---

**END OF DOCUMENT**
