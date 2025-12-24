# librispeech-phone-alignments

Word- and phone-level timestamps for the LibriSpeech dataset.

- Source alignments produced with the Montreal Forced Aligner; [LibriSpeech Alignments](https://zenodo.org/records/2619474) were released in March 2019. 

## Differences in the current contribution
- The number of words returned as 'spn' (speech noise; whole-word failure to phonemize) is 6432, compared to 23018 in the original.
- Missing files were reduced from 51 (~0.02% of LibriSpeech) in the original to 0. 
- MFA's IPA-like phones are used, while the original used arpabet. This choice was made as the IPA-based english_us_mfa dictionary showed better performance (fewer whole-word failures). A script is provided to convert phones into arpabet, given the amount of research that has been carried out using the 2019 arpabet alignments.


## Alignment and models
- Primary alignment used MFA with the `english_mfa` acoustic + `english_us_mfa` dictionary models.
- Out-of-vocabulary words are handled with a G2P fallback pass.

## JSON schema (per file)

Each release asset (`*.tar.gz`) extracts to a directory with per-speaker subdirectories containing JSON files:

```
<extracted_root>/
├── 19/
│   ├── 19-198.json
│   ├── 19-227.json
│   └── ...
├── 26/
│   ├── 26-495.json
│   ├── 26-496.json
│   └── ...
└── ...
```

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
- Provide IPA-to-arpabet conversion script.

## References
- https://zenodo.org/records/2619474 (original 2019 LibriSpeech alignments)
- Michael McAuliffe, Michaela Socolof, Sarah Mihuc, Michael Wagner, and Morgan Sonderegger. "Montreal Forced Aligner: trainable text-speech alignment using Kaldi", Interspeech 2017.
