# CodeSeek Submission Pack

This directory records the reproducibility and submission materials included in the judged commit.

## Included in the repository

- Working FastAPI application and CodeSeek dashboard.
- CPU-friendly semantic retrieval with FAISS.
- Local BM25 keyword retrieval and hybrid score fusion.
- Optional reranking and retrieval timing diagnostics.
- Local NDCG@10 and MRR evaluation with ten development queries.
- MTEB `AppsRetrieval` adapter in `app/evaluation/mteb_adapter.py`.
- Presentation and demo-video links are included in the checklist below.
- Reproducible Python, Docker, and Docker Compose setup.

## External media checklist

The final PowerPoint deck and recorded demo video are presentation media hosted on Google Drive. They reference the repository URL and the immutable tag below.

| Submission item | Repository reference | Status |
|---|---|---|
| Source code | Entire repository | Included |
| Setup documentation | `README.md` | Included |
| Presentation link | [Google Drive presentation](https://drive.google.com/file/d/1uQgVzY08diWlhM5EVGB6Vn_llDu_s26C/view?usp=drivesdk) | Included |
| Recorded demo video | [Google Drive demo video](https://drive.google.com/file/d/1f1Rzo-E4eMA0EKGDSEMAVfxkrFoCsLIa/view?usp=drivesdk) | Included |
| PowerPoint file | [Google Drive PowerPoint](https://drive.google.com/file/d/1uQgVzY08diWlhM5EVGB6Vn_llDu_s26C/view?usp=drivesdk) | Included |
| Judged source snapshot | `PRISM_GENAI_HACKATHON_Y2026` | Required tag |

## Final verification

Run the commands in the root README, then verify the tagged commit:

```powershell
git checkout PRISM_GENAI_HACKATHON_Y2026
python -m pytest
```

The tag must remain on the final commit submitted for judging.
