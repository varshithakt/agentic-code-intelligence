"""Optional adapter for the installed MTEB AppsRetrieval task.

The dependency is intentionally optional; local evaluation remains available
without downloading the official benchmark.
"""
def run_apps_retrieval(model_name=None, output_folder=None):
    try:
        import mteb
    except ImportError as exc:
        raise RuntimeError("Install mteb to run the official AppsRetrieval benchmark") from exc
    model = model_name or "BAAI/bge-small-en-v1.5"
    task = mteb.get_task("AppsRetrieval")
    evaluation = mteb.MTEB(tasks=[task])
    return evaluation.run(model, output_folder=output_folder)
