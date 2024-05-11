# Breviarium

This is a personal, one-off, repository containing the code used to translate Mazarin's `Breviarium Politicorum` from 17th century Latin to English using Claude (API or manually).

You can read the end result, as well as a description of the prompts and process, [on my blog](https://nestordemeure.github.io/writing/translations/breviarum_politicorum).

Note that this code is intended to perform a cyborg translation (human and AI working together for the best possible end-result) rather than a fully automatic translation.

## Usage

You will need an Anthropic API key in your environment.
Tweak script variables to pick models (`human` for manual mode, `haiku` for tests, and `opus` for actual runs) as well as files.

* `clean_ocr.py` used to turn the 1701 OCRs into a single clean version of the text.
* `translate_latin.y` used to translate the Latin text into English.
* `check_translation.py` used to double-check the translation against the Latin.
* `markdown_to_hugo.py` used to turn a markdown file into a Hugo hierarchy of files and folders.

## TODO

* manually proofread translation (currently at `Acquiring Gravity` / `Gravitatem Acquirere`)
