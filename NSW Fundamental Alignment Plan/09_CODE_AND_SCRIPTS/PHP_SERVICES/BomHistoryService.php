<?php

namespace App\Services;

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

/**
 * BomHistoryService
 * 
 * Purpose: Centralized service for recording BOM operation history
 * Reference: HISTORY_BACKUP_MIN_SPEC.md, BOM_ENGINE_BLUEPRINT.md
 * Phase: Phase-1 (P0) - Line Item Edit + History Foundation
 * 
 * This service handles all history recording for BOM operations:
 * - Line item edits (CREATE, UPDATE, DELETE, REPLACE)
 * - BOM node edits (future - Phase-3)
 * - Copy operations (future - Phase-2)
 */
class BomHistoryService
{
    /**
     * Record history for a line item operation
     * 
     * @param string $operation Operation type: 'CREATE', 'UPDATE', 'DELETE', 'REPLACE'
     * @param int $itemId QuotationSaleBomItemId
     * @param array|null $beforeSnapshot Complete state before operation (null for CREATE)
     * @param array|null $afterSnapshot Complete state after operation (null for DELETE)
     * @param array $changedFields Array of field names that changed
     * @param int|null $userId User who performed the operation
     * @param array|null $parentReference What it was copied from (optional)
     * @return int History record ID
     * @throws \Exception If history recording fails
     */
    public function recordItemHistory(
        string $operation,
        int $itemId,
        ?array $beforeSnapshot = null,
        ?array $afterSnapshot = null,
        array $changedFields = [],
        ?int $userId = null,
        ?array $parentReference = null
    ): int {
        // Validate operation type
        $validOperations = ['CREATE', 'UPDATE', 'DELETE', 'REPLACE'];
        if (!in_array($operation, $validOperations)) {
            throw new \InvalidArgumentException("Invalid operation: {$operation}. Must be one of: " . implode(', ', $validOperations));
        }

        // Validate snapshots based on operation
        if ($operation === 'CREATE' && $afterSnapshot === null) {
            throw new \InvalidArgumentException("CREATE operation requires after_snapshot");
        }
        if ($operation === 'DELETE' && $beforeSnapshot === null) {
            throw new \InvalidArgumentException("DELETE operation requires before_snapshot");
        }
        if (in_array($operation, ['UPDATE', 'REPLACE']) && ($beforeSnapshot === null || $afterSnapshot === null)) {
            throw new \InvalidArgumentException("{$operation} operation requires both before_snapshot and after_snapshot");
        }

        try {
            $historyId = DB::table('quotation_sale_bom_item_history')->insertGetId([
                'quotation_sale_bom_item_id' => $itemId,
                'operation' => $operation,
                'before_snapshot' => $beforeSnapshot ? json_encode($beforeSnapshot) : null,
                'after_snapshot' => $afterSnapshot ? json_encode($afterSnapshot) : null,
                'changed_fields' => json_encode($changedFields),
                'user_id' => $userId,
                'timestamp' => now(),
                'parent_reference' => $parentReference ? json_encode($parentReference) : null,
            ]);

            Log::info("BOM history recorded", [
                'history_id' => $historyId,
                'item_id' => $itemId,
                'operation' => $operation,
                'user_id' => $userId,
            ]);

            return $historyId;
        } catch (\Exception $e) {
            Log::error("Failed to record BOM history", [
                'item_id' => $itemId,
                'operation' => $operation,
                'error' => $e->getMessage(),
            ]);
            throw new \Exception("Failed to record BOM history: " . $e->getMessage(), 0, $e);
        }
    }

    /**
     * Capture complete snapshot of a line item
     * 
     * Phase-1: Store the entire DB row as-is (no custom remapping).
     * The snapshot contains all NEPL column names exactly as they appear in the database.
     * 
     * @param object|array $item QuotationSaleBomItem model or array
     * @return array Complete snapshot as array (full DB row with NEPL column names)
     */
    public function captureItemSnapshot($item): array
    {
        // Convert to array if it's a model
        if (is_object($item) && method_exists($item, 'toArray')) {
            // Use toArray() to get full DB row with NEPL column names
            $snapshot = $item->toArray();
        } elseif (is_object($item)) {
            $snapshot = (array) $item;
        } else {
            $snapshot = $item;
        }

        // Phase-1: Return full DB row as-is (no remapping)
        // Snapshots will contain NEPL column names: QuotationSaleBomItemId, QuotationSaleBomId, Qty, ProductId, Status, etc.
        return $snapshot;
    }

    /**
     * Compare two snapshots and return changed fields
     * 
     * @param array|null $beforeSnapshot
     * @param array|null $afterSnapshot
     * @return array Array of field names that changed
     */
    public function getChangedFields(?array $beforeSnapshot, ?array $afterSnapshot): array
    {
        if ($beforeSnapshot === null || $afterSnapshot === null) {
            return [];
        }

        $changedFields = [];
        
        // Compare all top-level fields
        $allKeys = array_unique(array_merge(array_keys($beforeSnapshot), array_keys($afterSnapshot)));
        
        foreach ($allKeys as $key) {
            $beforeValue = $beforeSnapshot[$key] ?? null;
            $afterValue = $afterSnapshot[$key] ?? null;
            
            // Deep comparison for arrays/objects
            if (is_array($beforeValue) && is_array($afterValue)) {
                if (json_encode($beforeValue) !== json_encode($afterValue)) {
                    $changedFields[] = $key;
                }
            } elseif ($beforeValue !== $afterValue) {
                $changedFields[] = $key;
            }
        }
        
        return $changedFields;
    }

    /**
     * Record copy operation history
     * 
     * @param string $sourceType Source entity type (master_bom, proposal_bom, feeder, panel)
     * @param int $sourceId Source entity ID
     * @param string $targetType Target entity type
     * @param int $targetId Target entity ID
     * @param array|null $sourceSnapshot Complete source structure + items as JSON
     * @param array|null $targetSnapshot Complete target structure + items as JSON
     * @param array|null $idMapping ID mapping in standardized format: {"bom_mapping": {"<source_bom_id>": "<target_bom_id>"}, "item_mapping": {"<source_item_id>": "<target_item_id>"}}
     * @param string $operation Operation type (COPY_MASTER_TO_PROPOSAL, etc.)
     * @param int|null $userId User performing operation
     * @param array|null $metadata Additional context
     * @return int History record ID
     */
    public function recordCopyHistory(
        string $sourceType,
        int $sourceId,
        string $targetType,
        int $targetId,
        ?array $sourceSnapshot = null,
        ?array $targetSnapshot = null,
        ?array $idMapping = null,
        string $operation = 'COPY',
        ?int $userId = null,
        ?array $metadata = null
    ): int
    {
        try {
            $historyId = DB::table('bom_copy_history')->insertGetId([
                'SourceType' => $sourceType,
                'SourceId' => $sourceId,
                'TargetType' => $targetType,
                'TargetId' => $targetId,
                'SourceSnapshot' => $sourceSnapshot ? json_encode($sourceSnapshot) : null,
                'TargetSnapshot' => $targetSnapshot ? json_encode($targetSnapshot) : null,
                'IdMapping' => $idMapping ? json_encode($idMapping) : null,
                'Operation' => $operation,
                'UserId' => $userId,
                'Timestamp' => now(),
                'Metadata' => $metadata ? json_encode($metadata) : null,
            ]);

            Log::info("BOM copy history recorded", [
                'history_id' => $historyId,
                'source_type' => $sourceType,
                'source_id' => $sourceId,
                'target_type' => $targetType,
                'target_id' => $targetId,
                'operation' => $operation,
                'user_id' => $userId,
            ]);

            return $historyId;
        } catch (\Exception $e) {
            Log::error("Failed to record BOM copy history", [
                'source_type' => $sourceType,
                'source_id' => $sourceId,
                'target_type' => $targetType,
                'target_id' => $targetId,
                'operation' => $operation,
                'error' => $e->getMessage(),
            ]);
            throw new \Exception("Failed to record BOM copy history: " . $e->getMessage(), 0, $e);
        }
    }
}

