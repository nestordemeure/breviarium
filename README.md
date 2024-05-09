# Breviarium

This is a personal, one-off, repository containing the code used to translate Mazarin's `Breviarium Politicorum` from 17th century Latin to English using Claude (API or manually).

You can read the end result, as well as a description of the prompts and process, [on my blog](https://nestordemeure.github.io/writing/translations/).

## Usage

You will need an Anthropic API key in your environment.
Tweak script variables to pick models (`human` for manual mode, `haiku` for tests, and `opus` for actual runs) as well as files.

* `clean_ocr.py` used to turn the 1701 OCRs into a single clean version of the text.
* `translate_latin.y` used to translate the Latin text into English.
* `markdown_to_hugo.py` used to turn a markdown file into a Hugo hierarchy of files and folders.

## TODO

* improve paragraph breakdown (starting at `Traveling to Provinces`)
* check translation against Latin (for additional / lost parts) and other references

Good prompt to freshen up the translation: `Can you simplify the formulations to make it easier to read for a contemporary reader?`
