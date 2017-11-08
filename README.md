# Tempus [![PyPI](https://img.shields.io/pypi/v/tempus.svg)](https://pypi.python.org/pypi/tempus) [![Travis](https://img.shields.io/travis/chunkhang/tempus.svg)](https://travis-ci.org/chunkhang/tempus)

<img src="https://images.unsplash.com/photo-1501139083538-0139583c060f?auto=format&fit=crop&w=1950&q=60&ixid=dW5zcGxhc2guY29tOzs7Ozs%3D" alt="Hourglass" width=400/><br/>
***TEMPUS EST DE ESSENTIA*** <br/>
*Time is of the essence*

## Installation

```
$ pip install tempus
```

## Usage

### TIMER
**tempus timer \<duration\>** <br/>
tempus timer 1m | tempus timer 2m15s | tempus timer 30s | tempus timer 10000s
```
$ tempus timer 1m
<Enter> to start

|█████████████████████████████████▌                                     | 0:32 |
```

## Caveats

### FONT
The progress bar may appear distorted or unsmooth when filling up due to the terminal's font not displaying the unicode characters as intended. Hence, you may need to play around with your font to get the best experience.
```
$ tempus test
Ensure that the characters below are:
* Equal in height
* Forming a smooth gradient across
* Aesthetically pleasing

|█▉▊▋▌▍▎▏ |
|⣿⣷⣧⣇⡇⡆⡄⡀|

https://github.com/chunkhang/tempus/#font
```
**Recommended** <br/>
Menlo | SF Mono <br/>

### TERMINAL
The progress bar needs a certain amount of space to ensure proper printing. Therefore, you may get a message if your terminal size is too small. In that case, just adjust your terminal's window before executing the command again.
```
$ tempus timer 1m
The terminal is too small: 52 x 25
It needs to be at least  : 80 x 10
```
**Minimum Size** <br/>
80 x 10

## Releases

### 1.1.0
* Shiny new progress bar for timer

### 1.0.0
* Initial release

## Unlicense

```
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>
```

## Contact

Feel free to report bugs or suggest features <br/>
**[Marcus Mu](http://marcusmu.me)** | chunkhang@gmail.com
