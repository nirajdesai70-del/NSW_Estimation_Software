<?php

namespace App\Http\Controllers;

use App\Services\BomEngine;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

/**
 * Example Controller Integration - QuotationV2Controller
 * 
 * Purpose: Demonstrate how to integrate BomEngine into existing controller methods
 * Reference: BOM_ENGINE_BLUEPRINT.md, BOM_ENGINE_IMPLEMENTATION_PLAN.md
 * Phase: Phase-1 (P0) - Line Item Edit + History Foundation
 * 
 * This is an EXAMPLE file showing the integration pattern.
 * Replace your existing controller methods with this pattern.
 * 
 * IMPORTANT: This shows integration for ONE method (updateItem) as per Phase-1 requirements.
 * Other methods (addItem, deleteItem, replaceItem) should follow the same pattern.
 */
class QuotationV2Controller_Example_Integration extends Controller
{
    protected BomEngine $bomEngine;

    public function __construct(BomEngine $bomEngine)
    {
        $this->bomEngine = $bomEngine;
    }

    /**
     * Update line item (EXAMPLE - Phase-1 integration)
     * 
     * BEFORE (Direct DB write - violates Rule 4):
     * ```php
     * public function updateItem(Request $request, int $itemId)
     * {
     *     $item = QuotationSaleBomItem::findOrFail($itemId);
     *     $item->update($request->only(['quantity', 'product_id', 'make_id', 'series_id']));
     *     return response()->json($item);
     * }
     * ```
     * 
     * AFTER (Using BomEngine - enforces Rule 4):
     */
    public function updateItem(Request $request, int $itemId): JsonResponse
    {
        try {
            // Validate request
            // Accept both snake_case and PascalCase, BomEngine will map to NEPL columns
            $validated = $request->validate([
                'Qty' => 'sometimes|numeric|min:0',
                'qty' => 'sometimes|numeric|min:0', // Also accept snake_case
                'quantity' => 'sometimes|numeric|min:0', // Also accept common variation
                'ProductId' => 'sometimes|integer|exists:products,ProductId',
                'product_id' => 'sometimes|integer|exists:products,ProductId', // Also accept snake_case
                'MakeId' => 'sometimes|nullable|integer',
                'make_id' => 'sometimes|nullable|integer',
                'SeriesId' => 'sometimes|nullable|integer',
                'series_id' => 'sometimes|nullable|integer',
                'Description' => 'sometimes|nullable|string',
                'description' => 'sometimes|nullable|string',
                'Remark' => 'sometimes|nullable|string',
                'remark' => 'sometimes|nullable|string',
            ]);

            // Call BomEngine (automatically records history)
            $result = $this->bomEngine->updateLineItem(
                itemId: $itemId,
                updateData: $validated,
                options: [
                    'preserveLookupPipeline' => true,
                    'userId' => auth()->id(),
                ]
            );

            // Return success response with history info
            return response()->json([
                'success' => true,
                'message' => 'Item updated successfully',
                'data' => [
                    'item_id' => $result['item_id'],
                    'history_id' => $result['history_id'],
                    'changed_fields' => $result['changed_fields'],
                ],
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Failed to update item: ' . $e->getMessage(),
            ], 500);
        }
    }

    /**
     * Add line item (EXAMPLE - Phase-1 integration)
     * 
     * Pattern to follow for addItem() method:
     */
    public function addItem(Request $request): JsonResponse
    {
        try {
            // Accept both snake_case and PascalCase input
            $validated = $request->validate([
                'QuotationSaleBomId' => 'required|integer|exists:quotation_sale_boms,QuotationSaleBomId',
                'bom_id' => 'required|integer|exists:quotation_sale_boms,QuotationSaleBomId', // Also accept snake_case
                'ProductId' => 'required|integer|exists:products,ProductId',
                'product_id' => 'required|integer|exists:products,ProductId', // Also accept snake_case
                'Qty' => 'required|numeric|min:0',
                'qty' => 'required|numeric|min:0', // Also accept snake_case
                'quantity' => 'required|numeric|min:0', // Also accept common variation
                'MakeId' => 'sometimes|nullable|integer',
                'make_id' => 'sometimes|nullable|integer',
                'SeriesId' => 'sometimes|nullable|integer',
                'series_id' => 'sometimes|nullable|integer',
                'Description' => 'sometimes|nullable|string',
                'description' => 'sometimes|nullable|string',
            ]);
            
            // Map to bom_id for BomEngine (it will map to QuotationSaleBomId internally)
            if (isset($validated['QuotationSaleBomId'])) {
                $validated['bom_id'] = $validated['QuotationSaleBomId'];
            }

            $result = $this->bomEngine->addLineItem(
                bomId: $validated['bom_id'],
                itemData: $validated,
                options: [
                    'allowTransitionalState' => $request->input('allow_transitional_state', false),
                    'userId' => auth()->id(),
                ]
            );

            return response()->json([
                'success' => true,
                'message' => 'Item added successfully',
                'data' => [
                    'item_id' => $result['item_id'],
                    'history_id' => $result['history_id'],
                ],
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Failed to add item: ' . $e->getMessage(),
            ], 500);
        }
    }

    /**
     * Delete line item (EXAMPLE - Phase-1 integration)
     * 
     * Pattern to follow for deleteItem() method:
     */
    public function deleteItem(int $itemId): JsonResponse
    {
        try {
            $result = $this->bomEngine->deleteLineItem(
                itemId: $itemId,
                options: [
                    'userId' => auth()->id(),
                ]
            );

            return response()->json([
                'success' => true,
                'message' => 'Item deleted successfully',
                'data' => [
                    'item_id' => $result['item_id'],
                    'history_id' => $result['history_id'],
                ],
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Failed to delete item: ' . $e->getMessage(),
            ], 500);
        }
    }

    /**
     * Replace product in line item (EXAMPLE - Phase-1 integration)
     * 
     * Pattern to follow for replaceItem() method:
     */
    public function replaceItem(Request $request, int $itemId): JsonResponse
    {
        try {
            // Accept both snake_case and PascalCase input
            $validated = $request->validate([
                'ProductId' => 'required|integer|exists:products,ProductId',
                'product_id' => 'required|integer|exists:products,ProductId', // Also accept snake_case
                'MakeId' => 'sometimes|nullable|integer',
                'make_id' => 'sometimes|nullable|integer',
                'SeriesId' => 'sometimes|nullable|integer',
                'series_id' => 'sometimes|nullable|integer',
                'preserve_quantity' => 'sometimes|boolean',
            ]);

            $result = $this->bomEngine->replaceLineItem(
                itemId: $itemId,
                newProductId: $validated['product_id'],
                options: [
                    'make_id' => $validated['make_id'] ?? null,
                    'series_id' => $validated['series_id'] ?? null,
                    'preserveQuantity' => $validated['preserve_quantity'] ?? true,
                    'userId' => auth()->id(),
                ]
            );

            return response()->json([
                'success' => true,
                'message' => 'Product replaced successfully',
                'data' => [
                    'item_id' => $result['item_id'],
                    'history_id' => $result['history_id'],
                ],
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Failed to replace product: ' . $e->getMessage(),
            ], 500);
        }
    }
}

