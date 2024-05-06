# Breviarium

Translating the Breviarium Politicorum using Claude (API or manually).

## Usage

You will need the API key in your environment. Tweak script variable to pick a model (`haiku` for tests and `opus` for actual runs).

* `clean_latin.py` can be used to turn the 1701 OCRs into a single clean version of the text.

## TODO

* create a `manual mode` (?):
  loading the prompt into the clipboard to be copied in the online UI, the result would be pasted back in the shell
  this would be the cheapest option (by far, book length inputs are long) but would require some manual work

* switch to AWS Bedrock for higher limits (?):
  this would be as expensive as using Anthropic while raising limitations
  a bit more complex but building some AWS experience
  * <https://aws.amazon.com/fr/bedrock/claude/>
  * <https://docs.anthropic.com/claude/reference/claude-on-amazon-bedrock>
