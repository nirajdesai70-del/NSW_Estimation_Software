<?php

namespace App\Services;

use App\Models\QuotationSaleBomItem;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Auth;

/**
 * BomEngine
 * 
 * Purpose: Centralized service for all BOM operations enforcing BOM principles
 * Reference: BOM_ENGINE_BLUEPRINT.md, BOM_ENGINE_IMPLEMENTATION_PLAN.md, BOM_ENGINE_SCHEMA_MAP.md
 * Phase: Phase-1 (P0) - Line Item Edit + History Foundation
 * 
 * This service enforces:
 * - Rule 1: Copy → New Instance
 * - Rule 2: Full Editability
 * - Rule 3: Lookup Pipeline Preserved
 * - Rule 4: Backup & History (MANDATORY)
 * - Rule 5: Cross-Level Consistency
 * 
 * Phase-1 implements only line item operations. Copy operations come in Phase-2.
 * 
 * IMPORTANT: Uses NEPL column names (PascalCase) - see BOM_ENGINE_SCHEMA_MAP.md
 */
class BomEngine
{
    protected BomHistoryService $historyService;

    public function __construct(BomHistoryService $historyService)
    {
        $this->historyService = $historyService;
    }

    /**
     * Add new line item to BOM
     * 
     * @param int $bomId Target BOM ID
     * @param array $itemData {
     *   @var int $productId Product ID (must have full lookup context)
     *   @var float $quantity Item quantity
     *   @var int|null $makeId Make ID (required if ProductType=2)
     *   @var int|null $seriesId Series ID (required if ProductType=2)
     *   @var string|null $sku SKU/description
     *   @var array|null $attributes L0/L1/L2 attributes
     * }
     * @param array $options {
     *   @var bool $allowTransitionalState Allow generic products temporarily (default: false)
     *   @var int|null $userId User performing operation
     * }
     * @return array {
     *   @var int $itemId Created item ID
     *   @var string $historyId History record ID
     * }
     */
    public function addLineItem(int $bomId, array $itemData, array $options = []): array
    {
        $userId = $options['userId'] ?? Auth::id();

        DB::beginTransaction();
        try {
            // Map input data to NEPL column names
            // Accept both snake_case and PascalCase input, but write PascalCase
            $createData = [
                'QuotationSaleBomId' => $bomId,
                'ProductId' => $itemData['ProductId'] ?? $itemData['product_id'] ?? $itemData['productId'] ?? null,
                'Qty' => $itemData['Qty'] ?? $itemData['qty'] ?? $itemData['quantity'] ?? 1,
                'MakeId' => $itemData['MakeId'] ?? $itemData['make_id'] ?? $itemData['makeId'] ?? null,
                'SeriesId' => $itemData['SeriesId'] ?? $itemData['series_id'] ?? $itemData['seriesId'] ?? null,
                'Description' => $itemData['Description'] ?? $itemData['description'] ?? null,
                'Remark' => $itemData['Remark'] ?? $itemData['remark'] ?? null,
                'Status' => 0, // Active
            ];

            // Remove null values to let DB defaults apply
            $createData = array_filter($createData, function($value) {
                return $value !== null;
            });

            $item = QuotationSaleBomItem::create($createData);

            // Capture after snapshot (CREATE operation has no before)
            $afterSnapshot = $this->historyService->captureItemSnapshot($item);

            // Record history
            $historyId = $this->historyService->recordItemHistory(
                operation: 'CREATE',
                itemId: $item->QuotationSaleBomItemId, // NEPL PK
                beforeSnapshot: null,
                afterSnapshot: $afterSnapshot,
                changedFields: array_keys($createData), // All fields are "new"
                userId: $userId,
                parentReference: $itemData['parent_reference'] ?? $itemData['ParentReference'] ?? null
            );

            DB::commit();

            Log::info("BOM line item added", [
                'item_id' => $item->QuotationSaleBomItemId,
                'bom_id' => $bomId,
                'history_id' => $historyId,
            ]);

            return [
                'item_id' => $item->QuotationSaleBomItemId,
                'history_id' => $historyId,
            ];
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error("Failed to add BOM line item", [
                'bom_id' => $bomId,
                'error' => $e->getMessage(),
            ]);
            throw $e;
        }
    }

    /**
     * Update existing line item
     * 
     * @param int $itemId Item ID to update
     * @param array $updateData {
     *   @var float|null $quantity New quantity
     *   @var int|null $productId New product ID (replacement)
     *   @var int|null $makeId New make ID
     *   @var int|null $seriesId New series ID
     *   @var string|null $sku New SKU/description
     *   @var array|null $attributes New attributes
     * }
     * @param array $options {
     *   @var bool $preserveLookupPipeline Ensure lookup chain remains intact (default: true)
     *   @var int|null $userId User performing operation
     * }
     * @return array {
     *   @var int $itemId Updated item ID
     *   @var string $historyId History record ID
     *   @var array $changedFields List of fields that changed
     * }
     */
    public function updateLineItem(int $itemId, array $updateData, array $options = []): array
    {
        $userId = $options['userId'] ?? Auth::id();
        $preserveLookupPipeline = $options['preserveLookupPipeline'] ?? true;

        DB::beginTransaction();
        try {
            // Load existing item using NEPL PK
            $item = QuotationSaleBomItem::findOrFail($itemId);
            
            if ($item->Status !== 0) {
                throw new \Exception("Cannot update soft-deleted item (Status != 0)");
            }

            // Capture before snapshot
            $beforeSnapshot = $this->historyService->captureItemSnapshot($item);

            // Map input data to NEPL column names
            // Accept both snake_case and PascalCase input, but write PascalCase
            $mappedData = [];
            if (isset($updateData['Qty']) || isset($updateData['qty']) || isset($updateData['quantity'])) {
                $mappedData['Qty'] = $updateData['Qty'] ?? $updateData['qty'] ?? $updateData['quantity'];
            }
            if (isset($updateData['ProductId']) || isset($updateData['product_id']) || isset($updateData['productId'])) {
                $mappedData['ProductId'] = $updateData['ProductId'] ?? $updateData['product_id'] ?? $updateData['productId'];
            }
            if (isset($updateData['MakeId']) || isset($updateData['make_id']) || isset($updateData['makeId'])) {
                $mappedData['MakeId'] = $updateData['MakeId'] ?? $updateData['make_id'] ?? $updateData['makeId'];
            }
            if (isset($updateData['SeriesId']) || isset($updateData['series_id']) || isset($updateData['seriesId'])) {
                $mappedData['SeriesId'] = $updateData['SeriesId'] ?? $updateData['series_id'] ?? $updateData['seriesId'];
            }
            if (isset($updateData['Description']) || isset($updateData['description'])) {
                $mappedData['Description'] = $updateData['Description'] ?? $updateData['description'];
            }
            if (isset($updateData['Remark']) || isset($updateData['remark'])) {
                $mappedData['Remark'] = $updateData['Remark'] ?? $updateData['remark'];
            }
            if (isset($updateData['Rate']) || isset($updateData['rate'])) {
                $mappedData['Rate'] = $updateData['Rate'] ?? $updateData['rate'];
            }
            if (isset($updateData['Discount']) || isset($updateData['discount'])) {
                $mappedData['Discount'] = $updateData['Discount'] ?? $updateData['discount'];
            }
            if (isset($updateData['NetRate']) || isset($updateData['net_rate']) || isset($updateData['netRate'])) {
                $mappedData['NetRate'] = $updateData['NetRate'] ?? $updateData['net_rate'] ?? $updateData['netRate'];
            }
            if (isset($updateData['Amount']) || isset($updateData['amount'])) {
                $mappedData['Amount'] = $updateData['Amount'] ?? $updateData['amount'];
            }

            if (empty($mappedData)) {
                throw new \Exception("No valid fields to update");
            }

            $item->update($mappedData);
            $item->refresh();

            // Capture after snapshot
            $afterSnapshot = $this->historyService->captureItemSnapshot($item);

            // Determine changed fields
            $changedFields = $this->historyService->getChangedFields($beforeSnapshot, $afterSnapshot);

            // Record history
            $historyId = $this->historyService->recordItemHistory(
                operation: 'UPDATE',
                itemId: $item->QuotationSaleBomItemId, // NEPL PK
                beforeSnapshot: $beforeSnapshot,
                afterSnapshot: $afterSnapshot,
                changedFields: $changedFields,
                userId: $userId
            );

            DB::commit();

            Log::info("BOM line item updated", [
                'item_id' => $item->QuotationSaleBomItemId,
                'history_id' => $historyId,
                'changed_fields' => $changedFields,
            ]);

            return [
                'item_id' => $item->QuotationSaleBomItemId,
                'history_id' => $historyId,
                'changed_fields' => $changedFields,
            ];
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error("Failed to update BOM line item", [
                'item_id' => $itemId,
                'error' => $e->getMessage(),
            ]);
            throw $e;
        }
    }

    /**
     * Replace product in line item (with full lookup)
     * 
     * @param int $itemId Item ID to replace
     * @param int $newProductId New product ID
     * @param array $options {
     *   @var int|null $makeId New make ID (if ProductType=2)
     *   @var int|null $seriesId New series ID (if ProductType=2)
     *   @var bool $preserveQuantity Preserve existing quantity (default: true)
     *   @var bool $preserveAttributes Preserve existing attributes (default: true)
     *   @var int|null $userId User performing operation
     * }
     * @return array {
     *   @var int $itemId Updated item ID
     *   @var string $historyId History record ID
     * }
     */
    public function replaceLineItem(int $itemId, int $newProductId, array $options = []): array
    {
        $userId = $options['userId'] ?? Auth::id();
        $preserveQuantity = $options['preserveQuantity'] ?? true;

        DB::beginTransaction();
        try {
            // Load existing item using NEPL PK
            $item = QuotationSaleBomItem::findOrFail($itemId);
            
            if ($item->Status !== 0) {
                throw new \Exception("Cannot replace product in soft-deleted item (Status != 0)");
            }

            // Capture before snapshot
            $beforeSnapshot = $this->historyService->captureItemSnapshot($item);

            // Build update data with NEPL column names
            $updateData = [
                'ProductId' => $newProductId,
            ];

            if (isset($options['MakeId']) || isset($options['make_id']) || isset($options['makeId'])) {
                $updateData['MakeId'] = $options['MakeId'] ?? $options['make_id'] ?? $options['makeId'];
            }
            if (isset($options['SeriesId']) || isset($options['series_id']) || isset($options['seriesId'])) {
                $updateData['SeriesId'] = $options['SeriesId'] ?? $options['series_id'] ?? $options['seriesId'];
            }

            if (!$preserveQuantity) {
                $updateData['Qty'] = $options['Qty'] ?? $options['qty'] ?? $options['quantity'] ?? $item->Qty;
            }

            $item->update($updateData);
            $item->refresh();

            // Capture after snapshot
            $afterSnapshot = $this->historyService->captureItemSnapshot($item);

            // Determine changed fields
            $changedFields = $this->historyService->getChangedFields($beforeSnapshot, $afterSnapshot);

            // Record history
            $historyId = $this->historyService->recordItemHistory(
                operation: 'REPLACE',
                itemId: $item->QuotationSaleBomItemId, // NEPL PK
                beforeSnapshot: $beforeSnapshot,
                afterSnapshot: $afterSnapshot,
                changedFields: $changedFields,
                userId: $userId
            );

            DB::commit();

            Log::info("BOM line item product replaced", [
                'item_id' => $item->QuotationSaleBomItemId,
                'old_product_id' => $beforeSnapshot['ProductId'] ?? null,
                'new_product_id' => $newProductId,
                'history_id' => $historyId,
            ]);

            return [
                'item_id' => $item->QuotationSaleBomItemId,
                'history_id' => $historyId,
            ];
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error("Failed to replace BOM line item product", [
                'item_id' => $itemId,
                'new_product_id' => $newProductId,
                'error' => $e->getMessage(),
            ]);
            throw $e;
        }
    }

    /**
     * Delete line item (soft delete)
     * 
     * @param int $itemId Item ID to delete
     * @param array $options {
     *   @var int|null $userId User performing operation
     * }
     * @return array {
     *   @var int $itemId Deleted item ID
     *   @var string $historyId History record ID
     * }
     */
    public function deleteLineItem(int $itemId, array $options = []): array
    {
        $userId = $options['userId'] ?? Auth::id();

        DB::beginTransaction();
        try {
            // Load existing item using NEPL PK
            $item = QuotationSaleBomItem::findOrFail($itemId);
            
            if ($item->Status !== 0) {
                throw new \Exception("Item is already soft-deleted (Status != 0)");
            }

            // Capture before snapshot
            $beforeSnapshot = $this->historyService->captureItemSnapshot($item);

            // Soft delete (Status 0 → 1) using NEPL column name
            $item->update(['Status' => 1]);
            $item->refresh();

            // Capture after snapshot (status changed)
            $afterSnapshot = $this->historyService->captureItemSnapshot($item);

            // Record history
            $historyId = $this->historyService->recordItemHistory(
                operation: 'DELETE',
                itemId: $item->QuotationSaleBomItemId, // NEPL PK
                beforeSnapshot: $beforeSnapshot,
                afterSnapshot: $afterSnapshot,
                changedFields: ['Status'], // Status changed from 0 to 1
                userId: $userId
            );

            DB::commit();

            Log::info("BOM line item deleted", [
                'item_id' => $item->QuotationSaleBomItemId,
                'history_id' => $historyId,
            ]);

            return [
                'item_id' => $item->QuotationSaleBomItemId,
                'history_id' => $historyId,
            ];
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error("Failed to delete BOM line item", [
                'item_id' => $itemId,
                'error' => $e->getMessage(),
            ]);
            throw $e;
        }
    }

    /**
     * Copy Master BOM to Proposal BOM (creates new instance)
     * 
     * @param int $masterBomId Master BOM template ID
     * @param int $quotationId Target quotation ID
     * @param int $quotationSaleId Target panel ID
     * @param int|null $parentBomId Parent BOM ID (if nested)
     * @param int $level BOM level (0=feeder, 1=BOM1, 2=BOM2)
     * @param array $options {
     *   @var bool $clearBeforeCopy Clear existing items before copy (default: true)
     *   @var bool $reuseExistingBom Reuse existing BOM if found (default: true)
     *   @var int|null $userId User performing operation
     * }
     * @return array {
     *   @var int $bomId Created/reused BOM ID
     *   @var bool $bomReused Whether existing BOM was reused
     *   @var int $itemsCreated Number of items created
     *   @var int $itemsDeleted Number of items soft-deleted (if clear-before-copy)
     *   @var string $copyHistoryId Copy history record ID
     * }
     */
    public function copyMasterBomToProposal(
        int $masterBomId,
        int $quotationId,
        int $quotationSaleId,
        ?int $parentBomId = null,
        int $level = 0,
        array $options = []
    ): array
    {
        $userId = $options['userId'] ?? Auth::id();
        $clearBeforeCopy = $options['clearBeforeCopy'] ?? true;
        $reuseExistingBom = $options['reuseExistingBom'] ?? true;

        DB::beginTransaction();
        try {
            // Load Master BOM and all items
            $masterBom = DB::table('quotation_sale_boms')
                ->where('QuotationSaleBomId', $masterBomId)
                ->first();
            
            if (!$masterBom) {
                throw new \Exception("Master BOM not found: {$masterBomId}");
            }

            $masterItems = DB::table('quotation_sale_bom_items')
                ->where('QuotationSaleBomId', $masterBomId)
                ->where('Status', 0)
                ->get()
                ->toArray();

            // Check for existing Proposal BOM (if reuse enabled)
            $existingBom = null;
            $bomReused = false;
            if ($reuseExistingBom) {
                $query = DB::table('quotation_sale_boms')
                    ->where('QuotationId', $quotationId)
                    ->where('QuotationSaleId', $quotationSaleId)
                    ->where('MasterBomId', $masterBomId)
                    ->where('Level', $level)
                    ->where('Status', 0);
                
                if ($parentBomId !== null) {
                    $query->where('ParentBomId', $parentBomId);
                } else {
                    $query->whereNull('ParentBomId');
                }
                
                $existingBom = $query->first();
            }

            $targetBomId = null;
            $itemsDeleted = 0;

            if ($existingBom) {
                // Reuse existing BOM
                $targetBomId = $existingBom->QuotationSaleBomId;
                $bomReused = true;

                // If clear-before-copy: soft-delete existing items
                if ($clearBeforeCopy) {
                    $itemsDeleted = DB::table('quotation_sale_bom_items')
                        ->where('QuotationSaleBomId', $targetBomId)
                        ->where('Status', 0)
                        ->update(['Status' => 1]);
                }
            } else {
                // Create new Proposal BOM (new ID)
                $targetBomId = DB::table('quotation_sale_boms')->insertGetId([
                    'QuotationSaleId' => $quotationSaleId,
                    'QuotationId' => $quotationId,
                    'MasterBomId' => $masterBom->MasterBomId ?? null,
                    'MasterBomName' => $masterBom->MasterBomName ?? null,
                    'Qty' => $masterBom->Qty ?? 1,
                    'Status' => 0,
                    'Level' => $level,
                    'ParentBomId' => $parentBomId,
                    'FeederName' => $masterBom->FeederName ?? null,
                ]);
            }

            // Copy all items (new IDs, copy-never-link)
            $itemsCreated = 0;
            $idMapping = [
                'bom_mapping' => [(string)$masterBomId => (string)$targetBomId],
                'item_mapping' => [],
            ];

            foreach ($masterItems as $sourceItem) {
                $newItemId = DB::table('quotation_sale_bom_items')->insertGetId([
                    'QuotationSaleBomId' => $targetBomId,
                    'QuotationSaleId' => $quotationSaleId,
                    'QuotationId' => $quotationId,
                    'ProductId' => $sourceItem->ProductId ?? null,
                    'Qty' => $sourceItem->Qty ?? 1,
                    'MakeId' => $sourceItem->MakeId ?? null,
                    'SeriesId' => $sourceItem->SeriesId ?? null,
                    'Description' => $sourceItem->Description ?? null,
                    'Remark' => $sourceItem->Remark ?? null,
                    'Rate' => $sourceItem->Rate ?? null,
                    'Discount' => $sourceItem->Discount ?? null,
                    'NetRate' => $sourceItem->NetRate ?? null,
                    'Amount' => $sourceItem->Amount ?? null,
                    'Status' => 0,
                ]);

                $idMapping['item_mapping'][(string)($sourceItem->QuotationSaleBomItemId ?? $sourceItem->quotation_sale_bom_item_id)] = (string)$newItemId;
                $itemsCreated++;
            }

            // Capture source snapshot (Master BOM + items)
            $sourceSnapshot = [
                'bom' => (array)$masterBom,
                'items' => array_map(fn($item) => (array)$item, $masterItems),
            ];

            // Capture target snapshot (Proposal BOM + items)
            $targetBom = DB::table('quotation_sale_boms')
                ->where('QuotationSaleBomId', $targetBomId)
                ->first();
            $targetItems = DB::table('quotation_sale_bom_items')
                ->where('QuotationSaleBomId', $targetBomId)
                ->where('Status', 0)
                ->get()
                ->toArray();
            $targetSnapshot = [
                'bom' => (array)$targetBom,
                'items' => array_map(fn($item) => (array)$item, $targetItems),
            ];

            // Record copy history
            $copyHistoryId = $this->historyService->recordCopyHistory(
                sourceType: 'master_bom',
                sourceId: $masterBomId,
                targetType: 'proposal_bom',
                targetId: $targetBomId,
                sourceSnapshot: $sourceSnapshot,
                targetSnapshot: $targetSnapshot,
                idMapping: $idMapping,
                operation: 'COPY_MASTER_TO_PROPOSAL',
                userId: $userId,
                metadata: ['level' => $level, 'parent_bom_id' => $parentBomId]
            );

            DB::commit();

            Log::info("Master BOM copied to Proposal BOM", [
                'master_bom_id' => $masterBomId,
                'target_bom_id' => $targetBomId,
                'bom_reused' => $bomReused,
                'items_created' => $itemsCreated,
                'items_deleted' => $itemsDeleted,
                'copy_history_id' => $copyHistoryId,
            ]);

            return [
                'bom_id' => $targetBomId,
                'bom_reused' => $bomReused,
                'items_created' => $itemsCreated,
                'items_deleted' => $itemsDeleted,
                'copy_history_id' => $copyHistoryId,
                'id_mapping' => $idMapping,
            ];
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error("Failed to copy Master BOM to Proposal BOM", [
                'master_bom_id' => $masterBomId,
                'error' => $e->getMessage(),
            ]);
            throw $e;
        }
    }

    /**
     * Copy Proposal BOM to another Proposal BOM (reuse)
     * 
     * @param int $sourceBomId Source Proposal BOM ID
     * @param int $targetQuotationId Target quotation ID
     * @param int $targetQuotationSaleId Target panel ID
     * @param int|null $targetParentBomId Target parent BOM ID (if nested)
     * @param int $targetLevel Target BOM level
     * @param array $options {
     *   @var bool $clearBeforeCopy Clear existing items before copy (default: true)
     *   @var bool $copyRecursive Copy nested BOMs recursively (default: true)
     *   @var int|null $userId User performing operation
     * }
     * @return array {
     *   @var int $bomId Created BOM ID
     *   @var int $itemsCreated Number of items created
     *   @var int $nestedBomsCreated Number of nested BOMs created
     *   @var string $copyHistoryId Copy history record ID
     * }
     */
    public function copyProposalBomToProposal(
        int $sourceBomId,
        int $targetQuotationId,
        int $targetQuotationSaleId,
        ?int $targetParentBomId = null,
        int $targetLevel = 0,
        array $options = []
    ): array
    {
        $userId = $options['userId'] ?? Auth::id();
        $clearBeforeCopy = $options['clearBeforeCopy'] ?? true;
        $copyRecursive = $options['copyRecursive'] ?? true;

        DB::beginTransaction();
        try {
            // Load source Proposal BOM and all items
            $sourceBom = DB::table('quotation_sale_boms')
                ->where('QuotationSaleBomId', $sourceBomId)
                ->first();
            
            if (!$sourceBom) {
                throw new \Exception("Source Proposal BOM not found: {$sourceBomId}");
            }

            $sourceItems = DB::table('quotation_sale_bom_items')
                ->where('QuotationSaleBomId', $sourceBomId)
                ->where('Status', 0)
                ->get()
                ->toArray();

            // Always create new Proposal BOM (never reuse)
            $targetBomId = DB::table('quotation_sale_boms')->insertGetId([
                'QuotationSaleId' => $targetQuotationSaleId,
                'QuotationId' => $targetQuotationId,
                'MasterBomId' => $sourceBom->MasterBomId ?? null,
                'MasterBomName' => $sourceBom->MasterBomName ?? null,
                'Qty' => $sourceBom->Qty ?? 1,
                'Status' => 0,
                'Level' => $targetLevel,
                'ParentBomId' => $targetParentBomId,
                'FeederName' => $sourceBom->FeederName ?? null,
            ]);

            // If clear-before-copy: soft-delete existing items (shouldn't exist for new BOM, but safe)
            if ($clearBeforeCopy) {
                DB::table('quotation_sale_bom_items')
                    ->where('QuotationSaleBomId', $targetBomId)
                    ->where('Status', 0)
                    ->update(['Status' => 1]);
            }

            // Copy all items (new IDs)
            $itemsCreated = 0;
            $idMapping = [
                'bom_mapping' => [(string)$sourceBomId => (string)$targetBomId],
                'item_mapping' => [],
            ];

            foreach ($sourceItems as $sourceItem) {
                $newItemId = DB::table('quotation_sale_bom_items')->insertGetId([
                    'QuotationSaleBomId' => $targetBomId,
                    'QuotationSaleId' => $targetQuotationSaleId,
                    'QuotationId' => $targetQuotationId,
                    'ProductId' => $sourceItem->ProductId ?? null,
                    'Qty' => $sourceItem->Qty ?? 1,
                    'MakeId' => $sourceItem->MakeId ?? null,
                    'SeriesId' => $sourceItem->SeriesId ?? null,
                    'Description' => $sourceItem->Description ?? null,
                    'Remark' => $sourceItem->Remark ?? null,
                    'Rate' => $sourceItem->Rate ?? null,
                    'Discount' => $sourceItem->Discount ?? null,
                    'NetRate' => $sourceItem->NetRate ?? null,
                    'Amount' => $sourceItem->Amount ?? null,
                    'Status' => 0,
                ]);

                $idMapping['item_mapping'][(string)($sourceItem->QuotationSaleBomItemId ?? $sourceItem->quotation_sale_bom_item_id)] = (string)$newItemId;
                $itemsCreated++;
            }

            // If recursive: copy nested BOMs recursively
            $nestedBomsCreated = 0;
            if ($copyRecursive) {
                $nestedBoms = DB::table('quotation_sale_boms')
                    ->where('ParentBomId', $sourceBomId)
                    ->where('Status', 0)
                    ->get();
                
                foreach ($nestedBoms as $nestedBom) {
                    $nestedResult = $this->copyProposalBomToProposal(
                        sourceBomId: $nestedBom->QuotationSaleBomId,
                        targetQuotationId: $targetQuotationId,
                        targetQuotationSaleId: $targetQuotationSaleId,
                        targetParentBomId: $targetBomId,
                        targetLevel: $targetLevel + 1,
                        options: [
                            'clearBeforeCopy' => $clearBeforeCopy,
                            'copyRecursive' => true,
                            'userId' => $userId,
                        ]
                    );
                    $nestedBomsCreated += 1 + ($nestedResult['nested_boms_created'] ?? 0);
                    // Merge nested ID mappings directly from return value
                    if (isset($nestedResult['id_mapping']) && is_array($nestedResult['id_mapping'])) {
                        $nestedMapping = $nestedResult['id_mapping'];
                        $idMapping['bom_mapping'] = array_merge($idMapping['bom_mapping'], $nestedMapping['bom_mapping'] ?? []);
                        $idMapping['item_mapping'] = array_merge($idMapping['item_mapping'], $nestedMapping['item_mapping'] ?? []);
                    }
                }
            }

            // Capture source/target snapshots
            $sourceSnapshot = [
                'bom' => (array)$sourceBom,
                'items' => array_map(fn($item) => (array)$item, $sourceItems),
            ];

            $targetBom = DB::table('quotation_sale_boms')
                ->where('QuotationSaleBomId', $targetBomId)
                ->first();
            $targetItems = DB::table('quotation_sale_bom_items')
                ->where('QuotationSaleBomId', $targetBomId)
                ->where('Status', 0)
                ->get()
                ->toArray();
            $targetSnapshot = [
                'bom' => (array)$targetBom,
                'items' => array_map(fn($item) => (array)$item, $targetItems),
            ];

            // Record copy history
            $copyHistoryId = $this->historyService->recordCopyHistory(
                sourceType: 'proposal_bom',
                sourceId: $sourceBomId,
                targetType: 'proposal_bom',
                targetId: $targetBomId,
                sourceSnapshot: $sourceSnapshot,
                targetSnapshot: $targetSnapshot,
                idMapping: $idMapping,
                operation: 'COPY_PROPOSAL_TO_PROPOSAL',
                userId: $userId,
                metadata: ['level' => $targetLevel, 'parent_bom_id' => $targetParentBomId, 'recursive' => $copyRecursive]
            );

            DB::commit();

            Log::info("Proposal BOM copied to Proposal BOM", [
                'source_bom_id' => $sourceBomId,
                'target_bom_id' => $targetBomId,
                'items_created' => $itemsCreated,
                'nested_boms_created' => $nestedBomsCreated,
                'copy_history_id' => $copyHistoryId,
            ]);

            return [
                'bom_id' => $targetBomId,
                'items_created' => $itemsCreated,
                'nested_boms_created' => $nestedBomsCreated,
                'copy_history_id' => $copyHistoryId,
                'id_mapping' => $idMapping,
            ];
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error("Failed to copy Proposal BOM to Proposal BOM", [
                'source_bom_id' => $sourceBomId,
                'error' => $e->getMessage(),
            ]);
            throw $e;
        }
    }

    /**
     * Copy Feeder Template or Reuse Existing Feeder
     * 
     * @param int $masterBomId Feeder template ID (Master BOM with TemplateType=FEEDER)
     * @param int $quotationId Target quotation ID
     * @param int $quotationSaleId Target panel ID
     * @param string $feederName Feeder name/identifier
     * @param array $options {
     *   @var bool $clearBeforeCopy Clear existing items before copy (default: true)
     *   @var bool $reuseExistingFeeder Reuse existing feeder if found (default: true)
     *   @var int|null $userId User performing operation
     * }
     * @return array {
     *   @var int $feederId Created/reused feeder ID
     *   @var bool $feederReused Whether existing feeder was reused
     *   @var int $itemsCreated Number of items created
     *   @var int $itemsDeleted Number of items soft-deleted (if clear-before-copy)
     *   @var string $copyHistoryId Copy history record ID
     * }
     */
    public function copyFeederTree(
        int $masterBomId,
        int $quotationId,
        int $quotationSaleId,
        string $feederName,
        array $options = []
    ): array
    {
        $userId = $options['userId'] ?? Auth::id();
        $clearBeforeCopy = $options['clearBeforeCopy'] ?? true;
        $reuseExistingFeeder = $options['reuseExistingFeeder'] ?? true;

        DB::beginTransaction();
        try {
            // Load Master BOM (feeder template)
            $masterBom = DB::table('quotation_sale_boms')
                ->where('QuotationSaleBomId', $masterBomId)
                ->first();
            
            if (!$masterBom) {
                throw new \Exception("Master BOM (feeder template) not found: {$masterBomId}");
            }

            $masterItems = DB::table('quotation_sale_bom_items')
                ->where('QuotationSaleBomId', $masterBomId)
                ->where('Status', 0)
                ->get()
                ->toArray();

            // CRITICAL: Detect existing feeder by identity (detect column existence first)
            $existingFeeder = null;
            $feederReused = false;
            if ($reuseExistingFeeder) {
                // Base match: QuotationId, QuotationSaleId, MasterBomId, Level=0, ParentBomId=NULL, Status=0
                $query = DB::table('quotation_sale_boms')
                    ->where('QuotationId', $quotationId)
                    ->where('QuotationSaleId', $quotationSaleId)
                    ->where('MasterBomId', $masterBomId)
                    ->where('Level', 0)
                    ->whereNull('ParentBomId')
                    ->where('Status', 0);

                // Identity field detection (check which columns exist)
                $hasFeederName = DB::getSchemaBuilder()->hasColumn('quotation_sale_boms', 'FeederName');
                $hasMasterBomName = DB::getSchemaBuilder()->hasColumn('quotation_sale_boms', 'MasterBomName');

                if ($hasFeederName) {
                    // Prefer FeederName for identity match
                    $query->where('FeederName', $feederName);
                } elseif ($hasMasterBomName) {
                    // Use MasterBomName if FeederName doesn't exist
                    $query->where('MasterBomName', $feederName);
                }
                // If both exist, prefer FeederName (already handled above)

                $existingFeeder = $query->first();
            }

            $targetFeederId = null;
            $itemsDeleted = 0;

            if ($existingFeeder) {
                // Reuse existing feeder
                $targetFeederId = $existingFeeder->QuotationSaleBomId;
                $feederReused = true;

                // CRITICAL: If clear-before-copy: soft-delete existing items BEFORE copying new items
                if ($clearBeforeCopy) {
                    $itemsDeleted = DB::table('quotation_sale_bom_items')
                        ->where('QuotationSaleBomId', $targetFeederId)
                        ->where('Status', 0)
                        ->update(['Status' => 1]);
                }
            } else {
                // Create new feeder (new ID)
                $insertData = [
                    'QuotationSaleId' => $quotationSaleId,
                    'QuotationId' => $quotationId,
                    'MasterBomId' => $masterBom->MasterBomId ?? null,
                    'Qty' => $masterBom->Qty ?? 1,
                    'Status' => 0,
                    'Level' => 0,
                    'ParentBomId' => null,
                ];

                // Add identity fields if they exist
                $hasFeederName = DB::getSchemaBuilder()->hasColumn('quotation_sale_boms', 'FeederName');
                $hasMasterBomName = DB::getSchemaBuilder()->hasColumn('quotation_sale_boms', 'MasterBomName');

                if ($hasFeederName) {
                    $insertData['FeederName'] = $feederName;
                }
                if ($hasMasterBomName && !$hasFeederName) {
                    $insertData['MasterBomName'] = $feederName;
                } elseif ($hasMasterBomName) {
                    $insertData['MasterBomName'] = $masterBom->MasterBomName ?? null;
                }

                $targetFeederId = DB::table('quotation_sale_boms')->insertGetId($insertData);
            }

            // Copy all items (new IDs) using NEPL PascalCase columns
            $itemsCreated = 0;
            $idMapping = [
                'bom_mapping' => [(string)$masterBomId => (string)$targetFeederId],
                'item_mapping' => [],
            ];

            foreach ($masterItems as $sourceItem) {
                $newItemId = DB::table('quotation_sale_bom_items')->insertGetId([
                    'QuotationSaleBomId' => $targetFeederId,
                    'QuotationSaleId' => $quotationSaleId,
                    'QuotationId' => $quotationId,
                    'ProductId' => $sourceItem->ProductId ?? null,
                    'Qty' => $sourceItem->Qty ?? 1,
                    'MakeId' => $sourceItem->MakeId ?? null,
                    'SeriesId' => $sourceItem->SeriesId ?? null,
                    'Description' => $sourceItem->Description ?? null,
                    'Remark' => $sourceItem->Remark ?? null,
                    'Rate' => $sourceItem->Rate ?? null,
                    'Discount' => $sourceItem->Discount ?? null,
                    'NetRate' => $sourceItem->NetRate ?? null,
                    'Amount' => $sourceItem->Amount ?? null,
                    'Status' => 0,
                ]);

                $idMapping['item_mapping'][(string)($sourceItem->QuotationSaleBomItemId ?? $sourceItem->quotation_sale_bom_item_id)] = (string)$newItemId;
                $itemsCreated++;
            }

            // Capture source/target snapshots using NEPL PascalCase columns
            $sourceSnapshot = [
                'bom' => (array)$masterBom,
                'items' => array_map(fn($item) => (array)$item, $masterItems),
            ];

            $targetFeeder = DB::table('quotation_sale_boms')
                ->where('QuotationSaleBomId', $targetFeederId)
                ->first();
            $targetItems = DB::table('quotation_sale_bom_items')
                ->where('QuotationSaleBomId', $targetFeederId)
                ->where('Status', 0)
                ->get()
                ->toArray();
            $targetSnapshot = [
                'bom' => (array)$targetFeeder,
                'items' => array_map(fn($item) => (array)$item, $targetItems),
            ];

            // Record copy history
            $copyHistoryId = $this->historyService->recordCopyHistory(
                sourceType: 'feeder',
                sourceId: $masterBomId,
                targetType: 'feeder',
                targetId: $targetFeederId,
                sourceSnapshot: $sourceSnapshot,
                targetSnapshot: $targetSnapshot,
                idMapping: $idMapping,
                operation: 'COPY_FEEDER_TREE',
                userId: $userId,
                metadata: ['feeder_name' => $feederName, 'reused' => $feederReused]
            );

            DB::commit();

            Log::info("Feeder tree copied", [
                'master_bom_id' => $masterBomId,
                'target_feeder_id' => $targetFeederId,
                'feeder_reused' => $feederReused,
                'items_created' => $itemsCreated,
                'items_deleted' => $itemsDeleted,
                'copy_history_id' => $copyHistoryId,
            ]);

            return [
                'feeder_id' => $targetFeederId,
                'feeder_reused' => $feederReused,
                'items_created' => $itemsCreated,
                'items_deleted' => $itemsDeleted,
                'copy_history_id' => $copyHistoryId,
                'id_mapping' => $idMapping,
            ];
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error("Failed to copy feeder tree", [
                'master_bom_id' => $masterBomId,
                'feeder_name' => $feederName,
                'error' => $e->getMessage(),
            ]);
            throw $e;
        }
    }

    /**
     * Copy Existing Feeder from Another Panel (always creates new instance)
     * 
     * @param int $sourceFeederId Source feeder ID
     * @param int $targetQuotationId Target quotation ID
     * @param int $targetQuotationSaleId Target panel ID
     * @param array $options {
     *   @var bool $copyRecursive Copy nested BOMs recursively (default: true)
     *   @var int|null $userId User performing operation
     * }
     * @return array {
     *   @var int $feederId Created feeder ID
     *   @var int $itemsCreated Number of items created
     *   @var int $nestedBomsCreated Number of nested BOMs created
     *   @var string $copyHistoryId Copy history record ID
     * }
     */
    public function copyFeederReuse(
        int $sourceFeederId,
        int $targetQuotationId,
        int $targetQuotationSaleId,
        array $options = []
    ): array
    {
        $userId = $options['userId'] ?? Auth::id();
        $copyRecursive = $options['copyRecursive'] ?? true;

        DB::beginTransaction();
        try {
            // Load source feeder and all items
            $sourceFeeder = DB::table('quotation_sale_boms')
                ->where('QuotationSaleBomId', $sourceFeederId)
                ->first();
            
            if (!$sourceFeeder) {
                throw new \Exception("Source feeder not found: {$sourceFeederId}");
            }

            $sourceItems = DB::table('quotation_sale_bom_items')
                ->where('QuotationSaleBomId', $sourceFeederId)
                ->where('Status', 0)
                ->get()
                ->toArray();

            // Always create new feeder (never reuse)
            $insertData = [
                'QuotationSaleId' => $targetQuotationSaleId,
                'QuotationId' => $targetQuotationId,
                'MasterBomId' => $sourceFeeder->MasterBomId ?? null,
                'Qty' => $sourceFeeder->Qty ?? 1,
                'Status' => 0,
                'Level' => 0,
                'ParentBomId' => null,
            ];

            // Add identity fields if they exist
            $hasFeederName = DB::getSchemaBuilder()->hasColumn('quotation_sale_boms', 'FeederName');
            $hasMasterBomName = DB::getSchemaBuilder()->hasColumn('quotation_sale_boms', 'MasterBomName');

            if ($hasFeederName) {
                $insertData['FeederName'] = $sourceFeeder->FeederName ?? null;
            }
            if ($hasMasterBomName) {
                $insertData['MasterBomName'] = $sourceFeeder->MasterBomName ?? null;
            }

            $targetFeederId = DB::table('quotation_sale_boms')->insertGetId($insertData);

            // Copy all items (new IDs)
            $itemsCreated = 0;
            $idMapping = [
                'bom_mapping' => [(string)$sourceFeederId => (string)$targetFeederId],
                'item_mapping' => [],
            ];

            foreach ($sourceItems as $sourceItem) {
                $newItemId = DB::table('quotation_sale_bom_items')->insertGetId([
                    'QuotationSaleBomId' => $targetFeederId,
                    'QuotationSaleId' => $targetQuotationSaleId,
                    'QuotationId' => $targetQuotationId,
                    'ProductId' => $sourceItem->ProductId ?? null,
                    'Qty' => $sourceItem->Qty ?? 1,
                    'MakeId' => $sourceItem->MakeId ?? null,
                    'SeriesId' => $sourceItem->SeriesId ?? null,
                    'Description' => $sourceItem->Description ?? null,
                    'Remark' => $sourceItem->Remark ?? null,
                    'Rate' => $sourceItem->Rate ?? null,
                    'Discount' => $sourceItem->Discount ?? null,
                    'NetRate' => $sourceItem->NetRate ?? null,
                    'Amount' => $sourceItem->Amount ?? null,
                    'Status' => 0,
                ]);

                $idMapping['item_mapping'][(string)($sourceItem->QuotationSaleBomItemId ?? $sourceItem->quotation_sale_bom_item_id)] = (string)$newItemId;
                $itemsCreated++;
            }

            // If recursive: copy nested BOMs recursively
            $nestedBomsCreated = 0;
            if ($copyRecursive) {
                $nestedBoms = DB::table('quotation_sale_boms')
                    ->where('ParentBomId', $sourceFeederId)
                    ->where('Status', 0)
                    ->get();
                
                foreach ($nestedBoms as $nestedBom) {
                    $nestedResult = $this->copyProposalBomToProposal(
                        sourceBomId: $nestedBom->QuotationSaleBomId,
                        targetQuotationId: $targetQuotationId,
                        targetQuotationSaleId: $targetQuotationSaleId,
                        targetParentBomId: $targetFeederId,
                        targetLevel: 1,
                        options: [
                            'clearBeforeCopy' => false,
                            'copyRecursive' => true,
                            'userId' => $userId,
                        ]
                    );
                    $nestedBomsCreated += 1 + ($nestedResult['nested_boms_created'] ?? 0);
                    // Merge nested ID mappings directly from return value
                    if (isset($nestedResult['id_mapping']) && is_array($nestedResult['id_mapping'])) {
                        $nestedMapping = $nestedResult['id_mapping'];
                        $idMapping['bom_mapping'] = array_merge($idMapping['bom_mapping'], $nestedMapping['bom_mapping'] ?? []);
                        $idMapping['item_mapping'] = array_merge($idMapping['item_mapping'], $nestedMapping['item_mapping'] ?? []);
                    }
                }
            }

            // Capture source/target snapshots using NEPL PascalCase columns
            $sourceSnapshot = [
                'bom' => (array)$sourceFeeder,
                'items' => array_map(fn($item) => (array)$item, $sourceItems),
            ];

            $targetFeeder = DB::table('quotation_sale_boms')
                ->where('QuotationSaleBomId', $targetFeederId)
                ->first();
            $targetItems = DB::table('quotation_sale_bom_items')
                ->where('QuotationSaleBomId', $targetFeederId)
                ->where('Status', 0)
                ->get()
                ->toArray();
            $targetSnapshot = [
                'bom' => (array)$targetFeeder,
                'items' => array_map(fn($item) => (array)$item, $targetItems),
            ];

            // Record copy history
            $copyHistoryId = $this->historyService->recordCopyHistory(
                sourceType: 'feeder',
                sourceId: $sourceFeederId,
                targetType: 'feeder',
                targetId: $targetFeederId,
                sourceSnapshot: $sourceSnapshot,
                targetSnapshot: $targetSnapshot,
                idMapping: $idMapping,
                operation: 'COPY_FEEDER_REUSE',
                userId: $userId,
                metadata: ['recursive' => $copyRecursive]
            );

            DB::commit();

            Log::info("Feeder reused (copied)", [
                'source_feeder_id' => $sourceFeederId,
                'target_feeder_id' => $targetFeederId,
                'items_created' => $itemsCreated,
                'nested_boms_created' => $nestedBomsCreated,
                'copy_history_id' => $copyHistoryId,
            ]);

            return [
                'feeder_id' => $targetFeederId,
                'items_created' => $itemsCreated,
                'nested_boms_created' => $nestedBomsCreated,
                'copy_history_id' => $copyHistoryId,
                'id_mapping' => $idMapping,
            ];
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error("Failed to copy feeder reuse", [
                'source_feeder_id' => $sourceFeederId,
                'error' => $e->getMessage(),
            ]);
            throw $e;
        }
    }

    /**
     * Copy Entire Panel Tree (all feeders + nested BOMs + items)
     * 
     * @param int $sourceQuotationSaleId Source panel ID
     * @param int $targetQuotationId Target quotation ID
     * @param int $targetQuotationSaleId Target panel ID
     * @param array $options {
     *   @var bool $copyRecursive Copy all nested structures (default: true)
     *   @var int|null $userId User performing operation
     * }
     * @return array {
     *   @var int $feedersCreated Number of feeders created
     *   @var int $bomsCreated Number of BOMs created
     *   @var int $itemsCreated Number of items created
     *   @var string $copyHistoryId Copy history record ID
     * }
     */
    public function copyPanelTree(
        int $sourceQuotationSaleId,
        int $targetQuotationId,
        int $targetQuotationSaleId,
        array $options = []
    ): array
    {
        $userId = $options['userId'] ?? Auth::id();
        $copyRecursive = $options['copyRecursive'] ?? true;

        DB::beginTransaction();
        try {
            // Load source panel and all feeders (Level=0, ParentBomId=NULL)
            $sourceFeeders = DB::table('quotation_sale_boms')
                ->where('QuotationSaleId', $sourceQuotationSaleId)
                ->where('Level', 0)
                ->whereNull('ParentBomId')
                ->where('Status', 0)
                ->get();

            $feedersCreated = 0;
            $bomsCreated = 0;
            $itemsCreated = 0;
            $idMapping = [
                'bom_mapping' => [],
                'item_mapping' => [],
            ];

            $sourceSnapshots = [];
            $targetSnapshots = [];

            // For each feeder: call copyFeederReuse() recursively
            foreach ($sourceFeeders as $sourceFeeder) {
                $feederResult = $this->copyFeederReuse(
                    sourceFeederId: $sourceFeeder->QuotationSaleBomId,
                    targetQuotationId: $targetQuotationId,
                    targetQuotationSaleId: $targetQuotationSaleId,
                    options: [
                        'copyRecursive' => $copyRecursive,
                        'userId' => $userId,
                    ]
                );

                $feedersCreated++;
                $itemsCreated += $feederResult['items_created'];
                $bomsCreated += $feederResult['nested_boms_created'] ?? 0;

                // Merge ID mappings directly from return value
                if (isset($feederResult['id_mapping']) && is_array($feederResult['id_mapping'])) {
                    $feederMapping = $feederResult['id_mapping'];
                    $idMapping['bom_mapping'] = array_merge($idMapping['bom_mapping'], $feederMapping['bom_mapping'] ?? []);
                    $idMapping['item_mapping'] = array_merge($idMapping['item_mapping'], $feederMapping['item_mapping'] ?? []);
                }

                // Capture snapshots from feeder result (if available) or fetch from history
                // Note: We still need snapshots for panel-level history, so we fetch from history table
                // This is acceptable as it's for final panel-level aggregation, not nested merge
                $feederHistory = DB::table('bom_copy_history')
                    ->where('BomCopyHistoryId', $feederResult['copy_history_id'])
                    ->first();
                if ($feederHistory) {
                    $sourceSnapshots[] = json_decode($feederHistory->SourceSnapshot, true);
                    $targetSnapshots[] = json_decode($feederHistory->TargetSnapshot, true);
                }
            }

            // Capture complete source/target snapshots (complete tree)
            $sourceSnapshot = [
                'panel_id' => $sourceQuotationSaleId,
                'feeders' => $sourceSnapshots,
            ];

            $targetFeeders = DB::table('quotation_sale_boms')
                ->where('QuotationSaleId', $targetQuotationSaleId)
                ->where('Level', 0)
                ->whereNull('ParentBomId')
                ->where('Status', 0)
                ->get();
            $targetSnapshot = [
                'panel_id' => $targetQuotationSaleId,
                'feeders' => $targetSnapshots,
            ];

            // Record copy history
            $copyHistoryId = $this->historyService->recordCopyHistory(
                sourceType: 'panel',
                sourceId: $sourceQuotationSaleId,
                targetType: 'panel',
                targetId: $targetQuotationSaleId,
                sourceSnapshot: $sourceSnapshot,
                targetSnapshot: $targetSnapshot,
                idMapping: $idMapping,
                operation: 'COPY_PANEL_TREE',
                userId: $userId,
                metadata: ['recursive' => $copyRecursive, 'feeders_count' => $feedersCreated]
            );

            DB::commit();

            Log::info("Panel tree copied", [
                'source_panel_id' => $sourceQuotationSaleId,
                'target_panel_id' => $targetQuotationSaleId,
                'feeders_created' => $feedersCreated,
                'boms_created' => $bomsCreated,
                'items_created' => $itemsCreated,
                'copy_history_id' => $copyHistoryId,
            ]);

            return [
                'feeders_created' => $feedersCreated,
                'boms_created' => $bomsCreated,
                'items_created' => $itemsCreated,
                'copy_history_id' => $copyHistoryId,
                'id_mapping' => $idMapping,
            ];
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error("Failed to copy panel tree", [
                'source_panel_id' => $sourceQuotationSaleId,
                'error' => $e->getMessage(),
            ]);
            throw $e;
        }
    }
}

