# speech-markdown

Get the speech from audio (or video), and turn this into markdown. Mainly designed for serious / educational purposes.
Disclaimer : currently, this is NOT really generating a markdown, but a plain text file.

## Requirements

Tested with Python 3.11.

If you want the extracted text from audio to be corrected/surfaced/rephrased, you need to have [ollama](https://ollama.com/) installed and working.

## Installation

Create a python virtual environment.

Clone this repository :

```
git clone https://github.com/borisboc/speech-mardown.git
cd speech-mardown
```

Install the requirements from the file `requirements.txt`. E.g. assuming you are in the cloned folder : 

```
python pip install -r requirements.txt
```

## Usage

You can use the provided script `speech_markdown.py`. E.g. the minimal use is : 

```
python speech_markdown/speech_mardown.py path/to/video_or_audio_file
```

It will use the default parameters, and default configuration files. Which are meant for **French** speech to text.
If you want to have an **English** setup, you will need to pass some additional optional arguments. For example :

```
python speech_markdown/speech_mardown.py path/to/video_or_audio_file --lang-settings En
```

Which will overwrite the arguments to have default values that are appropriate for English.

Of course, you can have a finer granularity if you pass all the arguments yourself. Here is an example for English : 


```
python speech_markdown/speech_mardown.py path/to/video_or_audio_file -sn vosk-model-en-us-0.22 --system-message speech_markdown/prompts/system_message_En.txt --user-message-template speech_markdown/prompts/user_message_template_En.txt
```


If you want explanations concerning the arguments, you may read the code or type

```
python speech_markdown/speech_mardown.py -h
```

which will return something like : 

```
usage: speech_mardown.py [-h] [--o O] [--lang-settings LANG_SETTINGS] [--speech-model-name SPEECH_MODEL_NAME] [--chunk-size CHUNK_SIZE] [--llm-model LLM_MODEL] [--system-message SYSTEM_MESSAGE]
                         [--user-message-template USER_MESSAGE_TEMPLATE]
                         filepath

Get the speech from audio (or video), and turn this into markdown. Mainly designed for serious / educational purposes

positional arguments:
  filepath              Path to you video or audio file

options:
  -h, --help            show this help message and exit
  --o O                 Path to the output text file
  --lang-settings LANG_SETTINGS, -ls LANG_SETTINGS
                        If Fr or En, it will overwrite speech-model-name, system-message, user-message-template values with default models and files appropriate for provided language (i.e. French or
                        English). Default is None : in this case, it does not overwrite the above mentioned arguments.
  --speech-model-name SPEECH_MODEL_NAME, -sn SPEECH_MODEL_NAME
                        Speech (audio to text) model name. See VOSK documentation. Default is vosk-model-fr-0.22
  --chunk-size CHUNK_SIZE
                        Size of chunks of characters (from audio) to pass to LLM for rephrasing / surfacing. Default is 1000.
  --llm-model LLM_MODEL
                        LLM model to use for surfacing / rephrasing (post audio to text).
  --system-message SYSTEM_MESSAGE
                        Path to the text file containing the system message (prompt) for surfacing with LLM.
  --user-message-template USER_MESSAGE_TEMPLATE
                        Path to the text file containing the user system message (prompt) templated (e.g. with $USER_MESSAGE) for surfacing with LLM.
```


## How does it work internally

The code does the following : 
 * Get audio file. Either : 
   * it extracts the audio from video file if provided input is a video file. It will generate a `.aac` file close to your video file, with same file name.
   * or it uses directly the audio file if provided input is an audio file.
 * Perform "speech to text" task using [VOSK](https://alphacephei.com/vosk/) library. It will generate a text file close to your video or audio file, with same file name.
 * Read the generated file and extract "chunks" of a given max size, to be sure to fit within the context window of the following LLM.
 * Correct / surface / rephrase the extracted text from speech, thanks to a provided LLM using the [ollama](https://ollama.com/) API. The generated generate a text file close to your video or audio file, with same file name including suffix `_surfaced`.

## Vosk bug in v0.3.45 if you want to use JSON export

In Vosk version v0.3.45 there is a bug for JSON export in `transcriber.py`.
At line 102, please change
```python
                    monologue["text"] += part["text"]
```
into 
```python
                    monologues["text"] += part["text"]
```
`monologues` with `s` otherwise the wrong variable is used.

This is corrected in version v0.3.50 but PyPi has until v0.3.45.