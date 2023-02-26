# Objective

Leverage GCP Services and Open Source tools to convert Audo to text and then extract text into key topics. The big idea is effectively identifying key concepts discussed on Podcast.

# High Level Design

## Dataflow Schema - Basic

![Basic Dataflow](./artifacts/designs/podcast_topic_extract_simple_data_flow.svg)

### RSS notes

- [RSS Schema](https://en.wikipedia.org/wiki/RSS_enclosure)

### Podcast Search

- [podsearch](https://pypi.org/project/podsearch/)
- [podsearch github](https://github.com/nalgeon/podsearch-py)
- [itune search api](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html)
  Media Type = 'podcast'
  Available Entities = [podcastAuthor, podcast]
  Potential Attributes = [titleTerm, languageTerm, authorTerm, genreIndex, artistTerm, ratingIndex, keywordsTerm, descriptionTerm]
- Note: Minor Surgery to add 'releaseDate' to podcast date

### Podcast Download

- [getpodcast](https://pypi.org/project/getpodcast/)
- [pyPodcastParser](https://pypi.org/project/pyPodcastParser/)
- [podcast-downloader](https://pypi.org/project/podcast-downloader/)
- [feedparser](https://pypi.org/project/feedparser/)
- [mutagen](https://mutagen.readthedocs.io/en/latest/index.html)

https://en.wikipedia.org/wiki/RSS_enclosure
length is size in bytes

### MP3 Audio to Text

- [GCP Speech-to-Text](https://cloud.google.com/speech-to-text)
- [GCP Speech-to-Text Docs](https://cloud.google.com/speech-to-text/docs)
- [GCP Python Client](https://cloud.google.com/python/docs/reference/speech/latest)
- [GCP Transcribe](https://cloud.google.com/speech-to-text/docs/transcribe-client-libraries)
- [HuggingFace Inference API Overview](https://huggingface.co/docs/api-inference/index)
- [HuggingFace Inference API Audio Example](https://huggingface.co/docs/api-inference/detailed_parameters#automatic-speech-recognition-task)
- [HuggingFace Speech2Text2](https://huggingface.co/docs/transformers/model_doc/speech_to_text_2)
- [HuggingFace Model Card](https://huggingface.co/facebook/wav2vec2-large-960h-lv60-self)

## Model Development

- Evaluate Transfer Learning
- Evaluate GCP UI
