# Stage 4 — WhatsApp Phone Automation

Automate first-touch sending on a connected Android device via ADB. This is the most error-prone stage — follow it precisely.

## Preconditions

- Android phone connected via ADB (`adb devices` shows a serial). USB or WiFi debugging both work; confirm connectivity before starting.
- WhatsApp (and/or WhatsApp Business) installed and logged in.
- Confirm package names on device (`pm list packages | grep whatsapp`) — `com.whatsapp` and/or `com.whatsapp.w4b`.
- ADB binary path and device serial are supplied by the user/config — **never hardcode a real serial or local path in shared artifacts**.
- Business card image pushed to the phone gallery if it will be sent.

## The one reliable input method: wa.me deep link

Do **not** use `adb shell input text` — it mangles long text, special characters, and non-ASCII; soft keyboards convert English to pinyin. Use a deep link that pre-fills the text:

```
https://wa.me/<digits>?text=<urlencoded message>
```

Open with:
```
adb -s <serial> shell am start -a android.intent.action.VIEW -d "<url>"
```

WhatsApp drops the user straight into the chat with the text sitting in the input box, byte-for-byte correct. Then tap send. This works even for messages containing em-dashes and apostrophes once URL-encoded.

## Core loop per lead

1. **Open chat + verify draft.** Force-stop **both** WhatsApp packages (ordinary + Business) before the first segment, so stale search/draft state is cleared. Open the wa.me URL with the first segment pre-filled. Poll a UI dump until the message text appears in an `EditText` node.
2. **Check invalid number.** If a "no WhatsApp account" / `AlertDialog` with a Cancel button appears, tap Cancel, log the number as invalid, and skip this lead.
3. **Save contact (if required).** Only after the number is confirmed valid, insert the contact with the agreed name via `content://com.android.contacts` (raw_contact → name + phone_v2). See notes below.
4. **Send segment 1** by tapping the send button (locate its bounds from a UI dump; do not assume fixed coordinates).
5. **Send remaining segments** in the same chat by reopening wa.me with each subsequent segment (hot start, no force-stop needed).
6. **Send website / card** if part of the agreed flow. For replies, skip these.
7. **Log result** (segments sent, website, card, contact saved, elapsed time) and pause a few seconds before the next lead.

## Waiting for the draft

- First-time lookup of a new number can be slow — allow ~14s, not 8s.
- Detect the pre-filled draft by checking the UI dump for a distinctive prefix of the message together with an `EditText` node. The dump stores the full sentence as the EditText `text`.
- Zero-width characters in UI text are `\u200b` (not `\u200e`) — account for this in string checks.

## Saving a contact via ContentProvider

Two-step insert (newer ADB `insert` does not return the row id):
1. Insert a `raw_contact` (`account_type=com.android.local`), then find its id by the max `_id` before/after.
2. Insert two `data` rows for that `raw_contact_id`: name (`vnd.android.cursor.item/name`, `data1=<name>`) and phone (`.../phone_v2`, `data1=+<number>`, `data2:i:2`).

Deduplicate by number; remove extra raw_contacts by id if a re-send created duplicates. Chinese/non-ASCII names pass through ADB args without corruption.

## Sending the business card image — dynamic location required

Gallery ordering changes as new screenshots/photos are added, so **never hardcode the thumbnail coordinates**.

Robust approach — locate every control by UI dump at runtime:
1. Push/re-push the card image to the gallery and `touch` it + broadcast `MEDIA_SCANNER_SCAN_FILE` so it is the newest (first tile).
2. Tap the attachment button — find the node by `content-desc="附件"`, take the one with the largest y (the input-bar one, not a header icon).
3. Tap the gallery holder by resource-id (`...:id/pickfiletype_gallery_holder`).
4. Select the first photo — nodes have `content-desc` like `照片，日期…` (may contain zero-width chars); sort by y/x and pick the top-left.
5. Tap send — find the node whose `content-desc` starts with `发送` and contains the item count (do **not** match the "HD image quality" setting button, which also mentions media).

Verify success by confirming the preview screen was left (`添加配文` no longer present) and, ideally, a screenshot check. A "card OK" reported without leaving the picker is a false positive.

## Invalid numbers

- Dialog: `没有 WhatsApp 账户` / AlertDialog + 取消. Tap `0.30, 0.536` (or the Cancel button's bounds).
- Log to `invalid_numbers.txt`: number, company, name, reason, date.
- Skip to next; one bad number must not stall the batch.

## Performance notes

- Native `uiautomator dump` is faster than a CLI `ui-tree` call (~2.6s vs ~3.3s).
- Hot-start subsequent segments (no force-stop) to save time.
- Short-poll the invalid dialog; it appears within ~3s.
- Move contact-save to after validity is confirmed.
- Typical cost: ~30–60s per lead with full flow.

## Pitfalls checklist (field-tested)

- Force-stop **both** WhatsApp packages or stale search state blocks the draft.
- After pre-fill, never press Delete/Back keys — an active IME inserts candidate characters and corrupts the draft.
- If using a helper IME for search input, switch back to the user's normal IME afterward.
- wa.me opening can race with a launch command → wait for the chat to actually open and verify the input box before tapping send.
- Adb absolute-coordinate taps can miss the gallery; prefer dump-derived bounds / normalized taps for the picker.
- Confirm the recipient chat header before sending (avoid sending to the wrong conversation).
- **Sending is irreversible — get user confirmation on recipients and exact text first.**
