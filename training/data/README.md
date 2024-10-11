# Dataset Format for Audio Files

This is the format for the audio files in the dataset. We'll open-source the dataset soon.

## Gender

- `M` - Male
- `F` - Female

## Age Group

- `CH` - Child (0-12)
- `TE` - Teenager (13-19)
- `AD` - Adult (20-60)
- `SE` - Senior (60+)
- `UNK` - Unknown

## Utterance Type

- `SEN`: Sentence
- `WOR`: Word
- `PHR`: Phrase

## Sentence

- `DFA`: "Don't Forget A jacket"
- `IEO`: "It's Eleven O' Clock"
- `IOM`: "I'm On My way to the meeting"
- `KTD`: "Kids are talking by the door"
- `DSD`: "Dogs are sitting by the door"

## Word

- refer `words.txt`

## Emotion

- `ANG`: Anger
- `DIS`: Disgust
- `FEA`: Fear
- `HAP`: Happy
- `NEU`: Neutral
- `SAD`: Sad
- `CAL`: Calm
- `SUR`: Surprised

## Emotion Intensity

- `LO`: Low intensity
- `MD`: Medium intensity
- `HI`: High intensity
- `UNK`: Unknown intensity

## Dataset

- `CREMA-D`: CREMA-D dataset
- `RAVDESS`: RAVDESS dataset
- `SAVEE`: SAVEE dataset
- `TESS`: TESS dataset

## File name format

```bash
<Emotion>_<EmotionIntensity>_<Gender>_<AgeGroup>_<Dataset>_<SpeakerID>_<UtteranceType>_<Sentence/Word>_<UtteranceNumber>.wav
```

Note: `Sentence` is written in short form and `Word` is written in full form (small case).

### Note: metadata will be provided with all files
