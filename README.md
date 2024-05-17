# Breviarium

This is a personal, one-off, repository containing the code used to translate Mazarin's `Breviarium Politicorum` from 17th century Latin to English using Claude (API or manually).

You can read the end result, as well as a description of the prompts and process, [on my blog](https://nestordemeure.github.io/writing/translations/breviarum_politicorum).

Note that this code is intended to perform a cyborg translation (human and AI working together for the best possible end-result) rather than a fully automatic translation.

## Usage

You will need an Anthropic API key in your environment.
Tweak script variables to pick models (`human` for manual mode, `haiku` for tests, and `opus` for actual runs) as well as files.

* `clean_ocr.py` used to turn the 1701 OCRs into a single clean version of the text.
* `translate_latin.y` used to translate the Latin text into English[^improvement].
* `check_translation.py` used to double-check the translation against the Latin.
* `check_readability.py` used to ensure that the text reads well, works as an editor[^edit].
* `markdown_to_hugo.py` used to turn a markdown file into a Hugo hierarchy of files and folders.

To produce a `.epub` file for easy reading, run:

```sh
pandoc data/english.md -o breviarium.epub --metadata title="Breviarium Politicorum" --metadata author="Mazarin" --metadata translator="Nestor D."
```

[^improvement]: If I were to do this again, I would provide the text of the section to be translated (extracted from the full text) inside the prompt to reduce likelihood of translating too much / not enough as well as reduce mental load for the model.

[^edit]: If I were to redo this, I would emphasize that the edit process should (while making the text accessible) preserve the flavor and texture of the 17th century original. Also keeping the emphasis on `will` rather than `may`.

## TODO

* do a full read through in another format
* produce new translation from latin+translation in order to preserve more of the 17th century flavor?
