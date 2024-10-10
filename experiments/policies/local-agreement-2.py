# Path: experiments/policies/local-agreement-2.py
# Description: Experiments on local agreement policy.

class LocalAgreement:
    def __init__(self, model):
        self.model: MockWhisperModel = model
        self.previous_output = ""
        self.buffer = ""

    def process_chunk(self, new_chunk):
        # Append new chunk to buffer
        self.buffer += new_chunk
        
        # Get model output for current buffer
        current_output = self.model.transcribe(self.buffer)

        # Find longest common prefix
        common_prefix = self.get_longest_common_prefix(self.previous_output, current_output)

        # Update previous output
        self.previous_output = current_output

        # Return stable output
        stable_output = common_prefix[len(self.buffer):]
        self.buffer = common_prefix
        return stable_output

    def get_longest_common_prefix(self, str1, str2):
        i = 0
        while i < len(str1) and i < len(str2) and str1[i] == str2[i]:
            i += 1
        return str1[:i]

# Usage example
class MockWhisperModel:
    def transcribe(self, audio):
        # This is a mock implementation
        # In reality, this would use the Whisper model to transcribe audio
        return audio.lower().replace('?', '').replace('!', '')

model = MockWhisperModel()
local_agreement = LocalAgreement(model)

# Simulate streaming input
chunks = ["Hello", " how", "are", "you", "?"]
for chunk in chunks:
    output = local_agreement.process_chunk(chunk)
    print(f"Current buffer: {local_agreement.buffer}")
    if output:
        print(f"Stable output: {output}")

print(f"Final buffer: {local_agreement.buffer}")
