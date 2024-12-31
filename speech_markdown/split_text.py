from pathlib import Path


def split_text_file_to_chunks(txt_filepath: Path, separator="\n", chunk_size=1000):
    if not txt_filepath.exists():
        raise FileNotFoundError(txt_filepath)

    with open(txt_filepath, "r") as f:
        txt = f.read()

    split = txt.split(separator)
    chunks = []

    cur_chunk = ""
    for s in split:
        len_cur_chunk = len(cur_chunk)
        if len_cur_chunk == 0:
            cur_chunk = s
        elif len(s) + len_cur_chunk < chunk_size:
            cur_chunk += " " + s
        else:
            chunks.append(cur_chunk)
            cur_chunk = s

    chunks.append(cur_chunk)

    return chunks
