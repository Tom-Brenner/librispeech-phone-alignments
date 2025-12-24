# librispeech-phone-alignments

Word- and phone-level timestamps for the LibriSpeech dataset.

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
- LibriSpeech dev-clean (tar.gz):  
  https://github.com/Tom-Brenner/librispeech-phone-alignments/releases/download/v1.0.0/LibriSpeech-aligned-dev-clean.tar.gz  
  SHA-256: `41d156c92c0e316b20cb9a11426e480ac05cdaf2fd34846e05bdb0423c42d792`
- LibriSpeech dev-other (tar.gz):  
  https://github.com/Tom-Brenner/librispeech-phone-alignments/releases/download/v1.0.0/LibriSpeech-aligned-dev-other.tar.gz  
  SHA-256: `f0040c44871b71b5286c94de3969097eca1e765fb2136b1bbf9dfa45e95c75a3`
- LibriSpeech test-clean (tar.gz):  
  https://github.com/Tom-Brenner/librispeech-phone-alignments/releases/download/v1.0.0/LibriSpeech-aligned-test-clean.tar.gz  
  SHA-256: `0b361593d13f850d5f69530d270b7ec6b5bf3fef315d68f6632e11b220d92921`
- LibriSpeech test-other (tar.gz):  
  https://github.com/Tom-Brenner/librispeech-phone-alignments/releases/download/v1.0.0/LibriSpeech-aligned-test-other.tar.gz  
  SHA-256: `751fbb81f4fa10208a792c6a6e8f064f07cf4ef9ffa85737358a711597be4e2b`
- LibriSpeech train-clean-100 (tar.gz):  
  https://github.com/Tom-Brenner/librispeech-phone-alignments/releases/download/v1.0.0/LibriSpeech-aligned-train-clean-100.tar.gz  
  SHA-256: `edaf7f8207b2a9a65d81c8d65a92ced9095d2de70cce71bdccad36f7a9f3800c`
- LibriSpeech train-clean-360 (tar.gz):  
  https://github.com/Tom-Brenner/librispeech-phone-alignments/releases/download/v1.0.0/LibriSpeech-aligned-train-clean-360.tar.gz  
  SHA-256: `769f3b010a4bfc65f2494e76c47d278dc40da5a68f9be2e8aeef50ebc232e0d8`
- LibriSpeech train-other-500 (tar.gz):  
  https://github.com/Tom-Brenner/librispeech-phone-alignments/releases/download/v1.0.0/LibriSpeech-aligned-train-other-500.tar.gz  
  SHA-256: `92962f7c990c02379ed265775ccfcbabb1a4bb955cea7e145f44e2eb0eb2e808`

## ToDo
- Add remaining LibriSpeech datasets

