# Deploy AP1 Evidence App (Streamlit Cloud)

Use this for sharing the app with colleagues (e.g. board demo). Takes ~15 minutes.

## Prerequisites

- GitHub repo pushed: `hakonbakke/ap1-curated-corpora` on branch `main`
- OpenAI API key with billing enabled
- Streamlit Cloud account (free): https://share.streamlit.io

## 1. Push latest code

From repo root:

```powershell
git push origin main
```

Cloud reads `data/corpus.parquet` from the repo — no separate database.

## 2. Create the app on Streamlit Cloud

1. Go to https://share.streamlit.io → **Create app**
2. **Repository:** `hakonbakke/ap1-curated-corpora`
3. **Branch:** `main`
4. **Main file path:** `app/app.py`
5. **App URL:** choose something short (e.g. `ap1-evidence`)

Click **Deploy**. First build may take 2–5 minutes.

## 3. Add secrets (required)

In the app → **Settings** → **Secrets**, paste:

```toml
OPENAI_API_KEY = "sk-proj-..."
```

Save → **Reboot app**.

Without this key the app shows an error and cannot answer questions.

## 4. Share the link

Public URL format:

`https://<your-app-name>.streamlit.app`

Send that link to Ragnar. He only needs a browser — no login for viewers on Community Cloud.

## 5. Demo tips for a board meeting

- Set language to **Norsk** if presenting in Norwegian
- **Audience:** «Fagperson» for detail, «Ikke-fagperson» for plain language
- Try example questions from the sidebar before the meeting
- Mention: **working MVP**, 27 curated papers, expert QA still in progress

Suggested demo questions:

- How robust is the Norwegian Traffic Light System as a regulatory framework?
- Which studies disagree most on lice impact magnitude?
- What evidence links lice-induced mortality to reduced adult returns?

## Costs

Each question calls OpenAI (embeddings + synthesis). Typical query: a few cents USD. Set usage limits in your OpenAI dashboard if needed.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| API key error | Check Secrets → Reboot app |
| Old corpus / 16 papers | Ensure latest `main` is deployed; Reboot app |
| App sleeps / slow first load | Normal on free tier after inactivity |
| Build fails | Check logs; confirm `requirements.txt` at repo root |

## Local vs cloud

| | Local | Streamlit Cloud |
|--|-------|-----------------|
| API key | `.env` | Secrets in Cloud UI |
| Corpus | `data/corpus.parquet` | Same file from GitHub |
| Updates | `git push` + Reboot app | |
