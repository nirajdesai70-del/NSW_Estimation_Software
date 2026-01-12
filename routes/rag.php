<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\RagController;

/*
|--------------------------------------------------------------------------
| RAG UI Routes
|--------------------------------------------------------------------------
|
| Routes for RAG UI integration. These routes provide a Laravel backend
| adapter for the RAG query service.
|
*/

Route::middleware(['auth'])->group(function () {
    Route::post('/ui/rag/query', [RagController::class, 'query'])
        ->middleware('throttle:30,1')
        ->name('rag.query');
    
    Route::post('/ui/rag/feedback', [RagController::class, 'feedback'])
        ->middleware('throttle:60,1')
        ->name('rag.feedback');
    
    // Example/test harness for RAG UI integration
    Route::get('/examples/rag-catalog', function () {
        return view('examples.rag-catalog-integration-example');
    })->name('examples.rag.catalog');
});

