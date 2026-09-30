import ast
import hashlib
import re
from app.config import MIN_CHUNK_LINES, MAX_CHUNK_LINES, CHUNK_OVERLAP

def _chunk(file_path, language, symbol, start, end, lines):
    code = "\n".join(lines[start-1:end]).rstrip()
    key = f"{file_path}:{start}:{end}:{code}"
    return {"chunk_id": hashlib.sha1(key.encode()).hexdigest(), "file_path": file_path, "language": language, "symbol_name": symbol, "start_line": start, "end_line": end, "code": code}

def _python_ranges(source):
    tree = ast.parse(source)
    ranges = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            ranges.append((node.lineno, getattr(node, "end_lineno", node.lineno), node.name))
    return sorted(ranges)

def _brace_ranges(lines):
    ranges=[]; start=None; depth=0; symbol="module"
    for i, line in enumerate(lines, 1):
        if start is None and "{" in line:
            start=i
            m=re.search(r"(?:class|struct|interface|enum|function|def)\s+([\w$]+)|([\w$]+)\s*\([^;]*\)\s*\{", line)
            symbol=next((v for v in m.groups() if v), "block") if m else "block"
        if start is not None:
            depth += line.count("{") - line.count("}")
            if depth <= 0:
                ranges.append((start,i,symbol)); start=None; depth=0
    if start is not None: ranges.append((start,len(lines),symbol))
    return ranges

def chunk_file(source_file, min_lines=MIN_CHUNK_LINES, max_lines=MAX_CHUNK_LINES, overlap=CHUNK_OVERLAP):
    lines=source_file.source.splitlines()
    if not lines: return []
    try:
        ranges = _python_ranges(source_file.source) if source_file.language == "python" else _brace_ranges(lines)
    except (SyntaxError, ValueError):
        ranges=[]
    # Fall back to bounded logical line windows when parsing fails or no blocks are found.
    if not ranges:
        ranges=[(1,len(lines),"module")]
    result=[]
    for start,end,symbol in ranges:
        # Preserve named AST symbols (even compact accessors/handlers); the
        # minimum applies to anonymous fallback windows, not useful symbols.
        if end-start+1 < min_lines and len(ranges)>1 and symbol in ("module", "block"): continue
        cursor=start
        while cursor<=end:
            stop=min(end,cursor+max_lines-1)
            if stop-cursor+1>=min_lines or symbol not in ("module", "block") or not result:
                result.append(_chunk(source_file.file_path,source_file.language,symbol,cursor,stop,lines))
            if stop==end: break
            cursor=max(cursor+1,stop-overlap+1)
    return result or [_chunk(source_file.file_path,source_file.language,"module",1,min(len(lines),max_lines),lines)]

def chunk_files(files, **kwargs):
    return [chunk for f in files for chunk in chunk_file(f, **kwargs)]
