/**
 * Google Apps Script web app: receives JSON POSTs from the Evidensrom app
 * (app/feedback.py) and appends one row per event.
 *
 * Setup: Google Sheet → Extensions → Apps Script → paste this file → Deploy →
 * New deployment → Web app, Execute as: Me, Who has access: Anyone → copy the
 * /exec URL into the Streamlit secret FEEDBACK_WEBHOOK_URL.
 *
 * Tabs "answers" and "ratings" are created with a header row on first use.
 */

const COLUMNS = {
  answer: [
    'ts', 'session_id', 'answer_id', 'room', 'question', 'mode', 'language',
    'model', 'top_k', 'n_active_docs', 'retrieved', 'answer', 'latency_s',
    'cached', 'error',
  ],
  rating: [
    'ts', 'session_id', 'answer_id', 'thumbs', 'answered_question',
    'fair_disagreement', 'comment',
  ],
};
const TAB = { answer: 'answers', rating: 'ratings' };

// Sheets rejects cells over 50,000 characters.
const MAX_CELL = 49000;

function cell(value) {
  if (value === undefined || value === null) return '';
  if (typeof value !== 'string') return value;
  const text = value.slice(0, MAX_CELL);
  // A leading = + - @ would be read as a formula; store user text as text.
  return /^[=+\-@]/.test(text) ? "'" + text : text;
}

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const data = JSON.parse(e.postData.contents);
    const columns = COLUMNS[data.type];
    if (!columns) return ContentService.createTextOutput('unknown type');

    const book = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = book.getSheetByName(TAB[data.type]) || book.insertSheet(TAB[data.type]);
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(columns);
      sheet.setFrozenRows(1);
    }
    sheet.appendRow(columns.map((name) => cell(data[name])));
    return ContentService.createTextOutput('ok');
  } finally {
    lock.releaseLock();
  }
}
