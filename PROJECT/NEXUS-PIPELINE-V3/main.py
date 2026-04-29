import asyncio
import argparse
import logging
from pathlib import Path
from core.orchestrator import MasterOrchestrator
from core.io_utils import ResultAggregator, OutputWriter, StateStore

async def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Pipeline v3")
    parser.add_argument("--dir", default=".", help="Directory to scan")
    parser.add_argument("--threshold", type=float, default=7.0, help="Quality threshold")
    parser.add_argument("--output", default="./reports", help="Output directory")
    parser.add_argument("--max-files", type=int, default=10, help="Max files to process")
    args = parser.parse_args()

    # Logging setup
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    
    # 1. Collect files
    target_dir = Path(args.dir)
    py_files = [str(f) for f in target_dir.glob("**/*.py") if f.is_file()][:args.max_files]
    
    if not py_files:
        print("No Python files found.")
        return

    # 2. Run Orchestrator
    orchestrator = MasterOrchestrator(threshold=args.threshold)
    raw_results = await orchestrator.run(py_files)
    
    # 3. Aggregate
    aggregator = ResultAggregator()
    final_results = aggregator.aggregate(raw_results)
    
    # 4. Save Output
    writer = OutputWriter()
    writer.write(final_results, args.output)
    
    # 5. Update State
    store = StateStore()
    store.save_run(final_results)
    
    print(f"\nDone. Processed {len(final_results)} files. Report saved to {args.output}")

if __name__ == "__main__":
    asyncio.run(main())
