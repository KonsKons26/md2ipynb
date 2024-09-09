# md2ipynb

**Markdown to ipynb converter that converts a markdown file to a notebook.**

Each line starting with a hastag (#) marks a new markdown cell in the resulting notebook. Hashtags inside codeblocks (sourrounded by triple backticks) are ignored so that comments in code blocks are not set as titles. A title depth (or threshold) can also be set so that titles over a certain limit are not placed in new markdown cells in the resulting notebook.

## Usage
The following command converts the file `input.md` to a notebook `output1.ipynb`.
```bash
$ md2ipynb.py input.md output1.ipynb
```

The user can specify a title depth `-d` as the maximum subtitle level that is allowed to create a new markdown cell in the resulting notebook. Lower level subtitles and the text under them are not added to a separate cell, they are appended to the above cell.

The following command takes the same input `input.md` and creates a new file, `output2.ipynb` where subtitles of level lower than 4 do not create new cells.
```bash
$ md2ipynb.py input.md output2.ipynb -d 4
```