from pathlib import Path


def split_text_file_to_chuncks(txt_filepath: Path, separator="\n", chunck_size=1000):
    if not txt_filepath.exists():
        raise FileNotFoundError(txt_filepath)

    with open(txt_filepath, "r") as f:
        txt = f.read()

    split = txt.split(separator)
    chuncks = []

    cur_chunck = ""
    for s in split:
        len_cur_chunck = len(cur_chunck)
        if len_cur_chunck == 0:
            cur_chunck = s
        elif len(s) + len_cur_chunck < chunck_size:
            cur_chunck += " " + s
        else:
            chuncks.append(cur_chunck)
            cur_chunck = s

    chuncks.append(cur_chunck)

    return chuncks
