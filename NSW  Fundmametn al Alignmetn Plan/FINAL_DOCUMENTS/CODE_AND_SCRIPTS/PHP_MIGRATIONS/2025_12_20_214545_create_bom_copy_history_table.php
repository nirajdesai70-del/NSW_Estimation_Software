<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('bom_copy_history', function (Blueprint $table) {
            $table->id('BomCopyHistoryId'); // NEPL PascalCase PK
            $table->string('SourceType', 50); // 'master_bom', 'proposal_bom', 'feeder', 'panel'
            $table->unsignedBigInteger('SourceId');
            $table->string('TargetType', 50);
            $table->unsignedBigInteger('TargetId');
            $table->json('SourceSnapshot')->nullable(); // Complete source structure + items
            $table->json('TargetSnapshot')->nullable(); // Complete target structure + items
            $table->json('IdMapping')->nullable(); // Standardized format: {"bom_mapping": {"<source_bom_id>": "<target_bom_id>"}, "item_mapping": {"<source_item_id>": "<target_item_id>"}}
            $table->string('Operation', 50); // 'COPY_MASTER_TO_PROPOSAL', 'COPY_PROPOSAL_TO_PROPOSAL', 'COPY_FEEDER_TREE', 'COPY_FEEDER_REUSE', 'COPY_PANEL_TREE'
            $table->unsignedBigInteger('UserId')->nullable();
            $table->timestamp('Timestamp')->useCurrent();
            $table->json('Metadata')->nullable(); // Additional context (feeder_name, level, etc.)
            
            // Composite indexes (safer + fewer index names, avoids MySQL index name length issues)
            $table->index(['SourceType', 'SourceId'], 'idx_bom_copy_history_source');
            $table->index(['TargetType', 'TargetId'], 'idx_bom_copy_history_target');
            $table->index(['Operation', 'Timestamp'], 'idx_bom_copy_history_operation_time');
        });
    }

    public function down()
    {
        Schema::dropIfExists('bom_copy_history');
    }
};

