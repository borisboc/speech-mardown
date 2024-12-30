# speech-mardown
Get the speech from audio (or video), and turn this into markdown. Mainly designed for serious / educational purposes 

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