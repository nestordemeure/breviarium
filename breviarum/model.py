import os
import time
from typing import List
from anthropic import Anthropic
from anthropic.types import Usage

#----------------------------------------------------------------------------------------
# THROTTLER

class Throttler:
    """Keeps tokens per minute to the given bounds"""
    def __init__(self, tokenPerMinute:int):
        self.tokenPerMinute: int = tokenPerMinute
        self.last_start_time: float = time.time()
        self.last_token_usage: int = 0
    
    def start(self):
        """Waits until we are back to 0 TPM"""
        # computes wait time
        time_to_wait = 60 * (self.last_token_usage / self.tokenPerMinute)
        time_waited = time.time() - self.last_start_time
        actual_time_to_wait = max(0, time_to_wait - time_waited)
        # display and wait
        if actual_time_to_wait > 60: 
            minutes_to_waits, seconds_to_wait = divmod(int(actual_time_to_wait), 60)
            print(F"Waiting {minutes_to_waits}min{seconds_to_wait}.")
        elif actual_time_to_wait > 1: 
            print(F"Waiting {int(actual_time_to_wait)} seconds.")
        time.sleep(actual_time_to_wait)
        # records this starting time
        self.last_token_usage = 0
        self.last_start_time = time.time()

    def stop(self, usage:Usage):
        """Records usage for the next call"""
        self.last_token_usage = usage.input_tokens + usage.output_tokens

#----------------------------------------------------------------------------------------
# MODEL

class Model:
    """
    Encapsulates a client to a model as well as the corresponding rate limit and other common logic.

    For rate limits, see:
    * https://docs.anthropic.com/claude/docs/models-overview#claude-3-a-new-generation-of-ai
    * https://docs.anthropic.com/claude/reference/rate-limits
    * https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html
    """
    def __init__(self, name:str, max_tokens:int, token_per_minute:int):
        self.name = name
        self.max_tokens = max_tokens
        self.client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'), max_retries=4)
        self.throttler = Throttler(token_per_minute)

    def chat(self, prompt:str, documents:List[str]=[], answer_prefix='<response>', stop_sequences=['</response>']) -> str:
        """
        Queries the model with, optionally, some documents and a prefix / stop criteria.
        This function takes care of throttling as well as looping when the output is too long for the maximum number of tokens produceable.
        """
        # assembles the inputs
        inputs = documents + [prompt]
        # iterates until we have completed our generation
        output = ""
        stop_reason = 'max_tokens'
        while (stop_reason == 'max_tokens'):
            # queries the model
            self.throttler.start()
            answer = self.client.messages.create(
                model=self.name,
                max_tokens=self.max_tokens,
                messages=[
                    # passes the two documents as well as the prompt
                    {"role": "user", "content": [{"type": "text", "text": input} for input in inputs]},
                    # primes the model to start transcribing
                    {"role": "assistant", "content": answer_prefix + output}
                ],
                stop_sequences=stop_sequences
            )
            self.throttler.stop(answer.usage)
            # updates our stopping criteria
            stop_reason = answer.stop_reason
            if (stop_reason == 'max_tokens'): print(f"WARNING: stopped due to max tokens, will take further iterations.")
            # updates our extracted latin
            if (len(answer.content) > 1): print(f"WARNING: `answer.content` is of length {len(answer.content)}: {answer.content}")
            output += answer.content[0].text
        # strips any unneeded spaces and returns
        return output.strip()

class Haiku(Model):
    """
    The Haiku Model: Quick, cheap, great for debugging.
    """
    def __init__(self):
        super().__init__(name='claude-3-haiku-20240307', max_tokens=4096, token_per_minute=50000)

class Opus(Model):
    """
    The Opus Model: Slow, expensive, very good, for final runs.
    """
    def __init__(self):
        super().__init__(name='claude-3-opus-20240229', max_tokens=4096, token_per_minute=20000)

#----------------------------------------------------------------------------------------
# MANUAL MODE

class Human(Model):
    """
    Calls a human to get an answer.
    """
    def __init__(self):
        super().__init__(name='human', max_tokens=None, token_per_minute=None)

    def chat(self, prompt:str, documents:List[str]=[], answer_prefix='<response>', stop_sequences=['</response>']):
        """
        Queries the model with, optionally, some documents and a prefix / stop criteria.
        This function asks the human user for an answer.
        """
        # displays the prompt to the user
        print(f"<prompt>\n{prompt}\n,/prompt>")
        # TODO put prompt in clipboard
        # TODO gets result from user
        output = None
        # TODO cut answer from the first occurence to answer prefix to the first occurence of stop_sequence
        return output