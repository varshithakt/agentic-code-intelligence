import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.utils.helpers import build_code_index

def main():
    parser=argparse.ArgumentParser(description="Build a local semantic code index")
    parser.add_argument("--path",required=True,help="Source code folder")
    args=parser.parse_args()
    try:
        result=build_code_index(args.path)
        print(f"Files indexed: {result['files_indexed']}\nCode chunks: {result['chunks_indexed']}\nIndex status: Ready")
    except Exception as exc:
        print(f"Index build failed: {exc}",file=sys.stderr); return 1
    return 0
if __name__=="__main__": raise SystemExit(main())
