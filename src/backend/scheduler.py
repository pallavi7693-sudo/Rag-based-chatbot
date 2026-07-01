import asyncio
import os
import time
import datetime
from typing import Optional

# Interval in seconds: 24 hours (86,400 seconds)
DAILY_INTERVAL_SECONDS = 86400

async def run_daily_ingestion_cycle(force: bool = False):
    """
    Executes the automated daily ingestion cycle:
    1. Regenerates corpus embeddings & Apache Parquet dataset.
    2. Hot-reloads the RAG retriever memory index without API downtime.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[SCHEDULER] [TIME] Triggering Daily Ingestion Cycle at {timestamp}...")
    
    try:
        # Step 1: Run Parquet export script to sync latest chunk vectors
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        export_script = os.path.join(project_root, "export_to_parquet.py")
        
        if os.path.exists(export_script):
            # Execute synchronously in threadpool to avoid blocking async event loop
            def _run_export():
                import subprocess
                res = subprocess.run(["python", export_script], capture_output=True, text=True, cwd=project_root)
                return res
            
            res = await asyncio.to_thread(_run_export)
            if res.returncode == 0:
                print(f"[SCHEDULER] [OK] Parquet dataset refreshed successfully:\n{res.stdout.strip()}")
            else:
                print(f"[SCHEDULER] [WARN] Parquet export warning/error: {res.stderr.strip()}")
        else:
            print(f"[SCHEDULER] [WARN] export_to_parquet.py not found at {export_script}")
            
        # Step 2: Hot-reload retriever cache
        from src.backend.retriever import get_retriever
        retriever = get_retriever()
        retriever.load_corpus()
        print(f"[SCHEDULER] [RELOAD] RAG Memory Index Hot-Reloaded! Now serving freshest mutual fund facts.")
        
    except Exception as e:
        print(f"[SCHEDULER] [ERROR] Daily ingestion cycle failed with exception: {e}")

async def start_ingestion_daemon(interval_seconds: int = DAILY_INTERVAL_SECONDS):
    """
    Long-running async daemon task that sleeps and triggers daily ingestion.
    Mounted in FastAPI startup lifecycle.
    """
    print(f"[SCHEDULER] [START] Daily Ingestion Daemon Started. Next cycle in {interval_seconds / 3600:.1f} hours.")
    while True:
        try:
            await asyncio.sleep(interval_seconds)
            await run_daily_ingestion_cycle()
        except asyncio.CancelledError:
            print("[SCHEDULER] [STOP] Ingestion Daemon gracefully shut down.")
            break
        except Exception as e:
            print(f"[SCHEDULER] [WARN] Daemon loop encountered error: {e}. Retrying in 60s...")
            await asyncio.sleep(60)
