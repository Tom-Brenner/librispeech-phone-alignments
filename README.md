# librispeech-phone-alignments

Word- and phone-level timestamps for LibriSpeech.

- Source alignments produced with the Montreal Forced Aligner; [CorentinJ/librispeech-alignments](https://github.com/CorentinJ/librispeech-alignments) is acknowledged for producing word-level timestamps nearly a decade earlier.
- Archived json files will be attached as GitHub Release assets.
- A checksum (SHA-256) will be provided alongside each download link.

## Alignment and models
- Primary alignment used MFA with the `english_mfa` acoustic + `english_us_mfa` dictionary models.
- Out-of-vocabulary words are handled with a G2P fallback pass.

## JSON schema (per file)
- Top level: map of each per-speaker JSON name (e.g., `100-121669.json`) with audio filenames as keys mapping to `{ "words": {...}, "phones": {...} }`.
- `words`: map of string indices to `{ "xmin": float, "xmax": float, "text": str }` (seconds).
- `phones`: same structure for phone-level boundaries.
- Floats are in seconds.

## Downloads
- LibriSpeech train-clean-360 phones JSON (gzipped):  
  https://github.com/Tom-Brenner/librispeech-phone-alignments/releases/download/v1.0.0/LibriSpeech-aligned-train-clean-360.json.gz  
  SHA-256: `2b4b4165d789eb6961037baa0587b18c06b4b1466eb6eb810163e7ab5459adc4`
  
## ToDo
- Add remaining LibriSpeech datasets

