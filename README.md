# Markov Music Generator

[![Satie Example](http://img.youtube.com/vi/H3xgdDTvvlc/0.jpg)](http://www.youtube.com/watch?v=H3xgdDTvvlc "Markov Music Generator: Satie")

## Setup
```
brew install portmidi
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Options
```
$ ./play.py --help
usage: play.py [-h] [--input PATH] [--chain-len LENGTH] [--time-scale SCALE]
               [--port NAME] [--list-ports]

optional arguments:
  -h, --help          show this help message and exit
  --input PATH        MIDI input, either a single file or a directory
  --chain-len LENGTH  Length of Markov chains to generate
  --time-scale SCALE  Temporal scale
  --port NAME         Output MIDI port name
  --list-ports        List available MIDI ports
```

## License
```
Copyright (c) 2015 Rob Hardwick

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```
