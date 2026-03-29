import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from module.scorer import analyze_chunk
from database.database import save_analysis_results

def run_processing_pipeline(data_list):
    # 1. CHUNKING LOGIC
    chunk_size = 10000
    chunks = [
        (i, data_list[i : i + chunk_size]) 
        for i in range(0, len(data_list), chunk_size)
    ]
    
    # 2. CORE ALLOCATION
    num_workers = max(1, multiprocessing.cpu_count() - 1)
    
    final_results = []

    # 3. PARALLEL EXECUTION 
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        for result_chunk in executor.map(analyze_chunk, chunks):
            final_results.extend(result_chunk)

    # 4. DATA FORMATTING
    db_payload = [
        (data_list[r[0]], r[1], r[2], r[3]) 
        for r in final_results
    ]

    # 5. PERSISTENCE
    save_analysis_results(db_payload)
    
    return len(db_payload)