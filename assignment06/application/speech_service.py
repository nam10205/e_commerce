class SpeechService:
    def transcribe(self,audio_input):
        # Assignment permits a transcript to simulate speech-to-text.
        if not isinstance(audio_input,str) or not audio_input.strip():
            raise ValueError('Provide a nonempty simulated transcript')
        return audio_input.strip()
