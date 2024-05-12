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
* `check_readability.py` used to ensure that the text reads well.
* `markdown_to_hugo.py` used to turn a markdown file into a Hugo hierarchy of files and folders.

[^improvement]: If this were to do again, I would provide the section text to be translated (extracted from the text) inside the prompt to reduce likelihood of translating too much / not enough as well as reduce mental load for the model.

## TODO

* manually proofread translation (currently at `Conversing with Others`)

* improve formulation:
* `Use Venus` (when praying to venus?)
* `the Tribunes` (in the tribunals?)
* `he is not acting in those ways` (those are not his reasons)
* `remitting tributes` (pardonning criminals?)
* `first shake a wolf skin over them`

* revisit
  * `Acquiring Gravity`
  * `Cover what you have written in a book or another sheet of paper, or move the raised paper closer.`
  * `Consider what needs someone is compelled by...`
  * `do not praise places that are excessively high`
  * `you have soldiers in a sack`
  * `It is better, however, to know much, to see and hear, and to find this out, but circumspectly; for it is offensive to know that something is being sought about oneself, hence it must be sought in such a way that you do not seem to be seeking.`
  * `If you notice you can do everything with the powerful`
  * `lead him to see the fault as an example`
  * `Provide a bedroom, but in a bed made for this purpose with windows, and where it will rain, open them. The fireplace should be blocked so that it smokes; the furnace should be lit at first.`

* add a redeable.md file
