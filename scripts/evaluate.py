import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.config import INDEX_DIR
from app.evaluation.datasets import load_local_dataset
from app.evaluation.evaluator import LocalEvaluator
from app.retrieval.index import IndexManager
from app.retrieval.search import CodeSearch

def main():
    parser=argparse.ArgumentParser(description="Evaluate CodeSeek retrieval strategies locally")
    parser.add_argument("--dataset",default=None); parser.add_argument("--output",default=None); parser.add_argument("--top-k",type=int,default=10); parser.add_argument("--model",default=None); parser.add_argument("--strategy",choices=["local","mteb"],default="local"); parser.add_argument("--batch-size",type=int,default=32)
    args=parser.parse_args()
    if args.strategy=="mteb":
        from app.evaluation.mteb_adapter import run_apps_retrieval
        try: print(json.dumps(run_apps_retrieval(args.model,args.output),indent=2,default=str)); return 0
        except Exception as exc: print(f"MTEB evaluation failed: {exc}",file=sys.stderr); return 1
    try: report=LocalEvaluator(CodeSearch(IndexManager(INDEX_DIR).load())).evaluate(load_local_dataset(args.dataset),args.top_k)
    except Exception as exc: print(f"Evaluation failed: {exc}",file=sys.stderr); return 1
    text=json.dumps(report,indent=2); print(text)
    if args.output: Path(args.output).write_text(text,encoding="utf-8")
    return 0
if __name__=="__main__": raise SystemExit(main())
