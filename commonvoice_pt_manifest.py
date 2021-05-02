import os
from pathlib import Path
import pandas as pd

# Download commonvoice ptbr from here and unzip it
# https://commonvoice.mozilla.org/

# !mv cv-corpus-6.1-2020-12-11/ commonvoice

# or wget from my github >> 
## Must do the ffmpeg part, since the original was in mp3 and its much more compressed than flac, so in order to reduce storage, we  kept as mp3

folder = Path('commonvoice/pt/')
paths = list(folder.glob('clips/*.mp3'))

train_df = pd.read_csv(folder.joinpath('train.tsv'), sep='\t', encoding='utf-8')[['path', 'sentence']]
dev_df = pd.read_csv(folder.joinpath('dev.tsv'), sep='\t', encoding='utf-8')[['path', 'sentence']]
test_df = pd.read_csv(folder.joinpath('test.tsv'), sep='\t', encoding='utf-8')[['path', 'sentence']]
pretrain_df = pd.read_csv(folder.joinpath('validated.tsv'), sep='\t', encoding='utf-8')[['path', 'sentence']]

dfs = [train_df, dev_df, test_df, pretrain_df]

for df in dfs:
    for i, audio in enumerate(df['path']):
        if not os.path.exists(folder.joinpath('audios/')):
            os.mkdir(folder.joinpath('audios/'))
        command = f"ffmpeg -i {folder.joinpath(f'clips/{audio}')} -ar 16000 {folder.joinpath(f'audios/{audio}').with_suffix('.flac')}"
        os.system(command)

# Removing older tsv files

# !rm -rf commonvoice/pt/clips
# !rm -rf commonvoice/pt/*.tsv

train_df.to_csv(f"{folder.joinpath('train.tsv')}", sep='\t', encoding='utf-8')
dev_df.to_csv(f"{folder.joinpath('dev.tsv')}", sep='\t', encoding='utf-8')
test_df.to_csv(f"{folder.joinpath('test.tsv')}", sep='\t', encoding='utf-8')
pretrain_df.to_csv(f"{folder.joinpath('validated.tsv')}", sep='\t', encoding='utf-8')