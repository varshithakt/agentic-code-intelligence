import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.retrieval.index import IndexManager
from app.retrieval.search import CodeSearch
from app.config import INDEX_DIR

def main():
    p=argparse.ArgumentParser(description="Search an indexed codebase")
    p.add_argument("query",help="Natural-language code question");p.add_argument("--top-k",type=int,default=5)
    a=p.parse_args()
    try: search=CodeSearch(IndexManager(INDEX_DIR).load());results,elapsed=search.search(a.query,a.top_k)
    except Exception as exc: print(f"Search failed: {exc}",file=sys.stderr);return 1
    for i,r in enumerate(results,1):
        print("="*60+f"\nRESULT #{i}\nScore: {r['score']:.4f}\nFile: {r['file_path']}\nSymbol: {r['symbol_name']}\nLines: {r['start_line']}-{r['end_line']}\n"+"="*60+f"\n\n{r['code']}\n")
    print(f"Search completed in {elapsed:.1f} ms")
    return 0
if __name__=="__main__": raise SystemExit(main())
