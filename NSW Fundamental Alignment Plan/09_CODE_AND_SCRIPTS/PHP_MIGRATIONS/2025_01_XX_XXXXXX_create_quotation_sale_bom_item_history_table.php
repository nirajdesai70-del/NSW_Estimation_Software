<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Migration: Create quotation_sale_bom_item_history table
 * 
 * Purpose: Store history/backup records for all line item edit operations
 * Reference: HISTORY_BACKUP_MIN_SPEC.md (Level 1, Table 1)
 * Phase: Phase-1 (P0) - Line Item Edit + History Foundation
 */
return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('quotation_sale_bom_item_history', function (Blueprint $table) {
            $table->id();
            
            // Reference to the item being edited
            // Stores QuotationSaleBomItemId (NEPL PK) from quotation_sale_bom_items table
            $table->unsignedBigInteger('quotation_sale_bom_item_id')->comment('Reference to quotation_sale_bom_items.QuotationSaleBomItemId (NEPL PK)');
            
            // Operation type
            $table->enum('operation', ['CREATE', 'UPDATE', 'DELETE', 'REPLACE'])->comment('Type of operation performed');
            
            // Snapshots (complete state before/after)
            $table->json('before_snapshot')->nullable()->comment('Complete JSON snapshot of item state before operation');
            $table->json('after_snapshot')->nullable()->comment('Complete JSON snapshot of item state after operation');
            
            // Changed fields tracking
            $table->json('changed_fields')->comment('Array of field names that changed (e.g., ["quantity", "product_id"])');
            
            // User context
            $table->unsignedBigInteger('user_id')->nullable()->comment('User who performed the operation');
            
            // Timestamp
            $table->timestamp('timestamp')->useCurrent()->comment('When the operation occurred');
            
            // Parent reference (for copied items)
            $table->json('parent_reference')->nullable()->comment('What it was copied from (e.g., {"copied_from_item_id": 111, "copied_from_bom_id": 222, "copied_at": "2025-01-01T10:00:00Z"})');
            
            // Indexes for performance
            $table->index('quotation_sale_bom_item_id', 'idx_item_id');
            $table->index('timestamp', 'idx_timestamp');
            $table->index('operation', 'idx_operation');
            $table->index('user_id', 'idx_user_id');
            
            // Foreign key (optional - depends on your FK policy)
            // $table->foreign('quotation_sale_bom_item_id')->references('id')->on('quotation_sale_bom_items')->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('quotation_sale_bom_item_history');
    }
};

