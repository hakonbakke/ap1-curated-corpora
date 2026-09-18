# Deploy AP1 Evidence App (Streamlit Cloud)

Share the live Evidensrom with colleagues (Ragnar only needs a browser).

## Prerequisites

- GitHub repo: `hakonbakke/ap1-curated-corpora` on `main`
- OpenAI API key with billing enabled
- Streamlit Cloud account: https://share.streamlit.io (sign in with GitHub)

## 1. Push latest code

Cloud reads `data/corpus.parquet` and `data/area-and-aquaculture.parquet` from GitHub. No separate database.

```powershell
git push origin main
```

## 2. Create or update the app

**First time:** open this prefilled deploy page (sign in with GitHub if asked):

https://share.streamlit.io/deploy?repository=hakonbakke/ap1-curated-corpora&branch=main&mainModule=app/app.py&subdomain=ap1-evidensrom

Confirm:

- Repository: `hakonbakke/ap1-curated-corpora`
- Branch: `main`
- Main file: `app/app.py`
- App URL: `ap1-evidensrom` so the link becomes `https://ap1-evidensrom.streamlit.app`

Click **Deploy**. First build takes a few minutes.

**Later updates:** `git push origin main`. Cloud redeploys from `main` automatically. Reboot only if secrets or a stuck build need a kick.

The home page lists evidence rooms. Open **Lakselus og villaks** or **Areal og havbruk**. Each has orientation (A-C) plus live Ask (D).

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

Send that link to Ragnar. He only needs a browser. Viewers on Community Cloud do not log in.

## 5. Demo tips for a board meeting

- Set language to **Norsk** if presenting in Norwegian
- **Audience:** «Fagperson» for detail, «Ikke-fagperson» for plain language
- Try example questions from the sidebar before the meeting
- Mention: **working draft**. Villaks: 27 papers. Areal: 39 documents. Priority questions in the areal room are not confirmed by the three selectors.

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
| Updates | `git push origin main` (Cloud redeploys) |
