# CodeSeek Submission Pack

This directory records the reproducibility and submission materials included in the judged commit.

## Included in the repository

- Working FastAPI application and CodeSeek dashboard.
- CPU-friendly semantic retrieval with FAISS.
- Local BM25 keyword retrieval and hybrid score fusion.
- Optional reranking and retrieval timing diagnostics.
- Local NDCG@10 and MRR evaluation with ten development queries.
- MTEB `AppsRetrieval` adapter in `app/evaluation/mteb_adapter.py`.
- Presentation and demo-video links should be added by the submitter in the checklist below.
- Reproducible Python, Docker, and Docker Compose setup.

## External media checklist

The final PowerPoint deck and recorded demo video are presentation media rather than executable source files. They should be uploaded to the hackathon submission portal and must reference the repository URL and the immutable tag below. Their exact binary files are not invented or included here because no finished deck or recording was supplied to this workspace.

| Submission item | Repository reference | Status |
|---|---|---|
| Source code | Entire repository | Included |
| Setup documentation | `README.md` | Included |
| Presentation link | `[Add PPT or Slides link here]` | To be added by submitter |
| Recorded demo video | External portal upload | Must be uploaded by submitter |
| PowerPoint file | External portal upload | Must be uploaded by submitter |
| Judged source snapshot | `PRISM_GENAI_HACKATHON_Y2026` | Required tag |

## Final verification

Run the commands in the root README, then verify the tagged commit:

```powershell
git checkout PRISM_GENAI_HACKATHON_Y2026
python -m pytest
```

The tag must remain on the final commit submitted for judging.
