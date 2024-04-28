Instructions to setup your development environment
==================================================

Installing dlib
---------------

- Install VSCode Community (C++ Desktop option), it must include cpp compiler and CMake
- Launch command prompt (not powershell, because of `vcvars64.bat`)
- activate venv, i.e. `.venv\Scripts\activate.bat`
- Make sure its bin dir is in the PATH, by launching  
  `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat`
- launch `pip install dlib`

Installing other dependencies
-----------------------------

Here, powershell is OK

- `pip install -e .`


How to use twin
===============

Common options
--------------

```shell
> twin --help
usage: twin [-h] [--version] [-v] [-vv] {show,capture} ...

Twin detection system

options:
  -h, --help           show this help message and exit
  --version            show program's version number and exit
  -v, --verbose        set loglevel to INFO
  -vv, --very-verbose  set loglevel to DEBUG

sub-command:
  {show,capture}
    show               Read image from file and display in popup
    capture            Read video from file or camera and display n-th frame in popup

Use `twin <sub-command> --help` to get help on sub-command
```

Show image
----------

### Usage

```shell
> twin show --help   
usage: twin show [-h] -i INPUT_FILE

Read image from file and display in popup

options:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
```

### Example

```shell
> twin -vv show -i .\tests\images\pil-pillow\lena.jpg
[2024-04-10 02:32:25] DEBUG:twin.cli:Launching command 'show'
[2024-04-10 02:32:25] DEBUG:twin.show:Loading image from file '.\\tests\\images\\pil-pillow\\lena.jpg'
[2024-04-10 02:32:25] DEBUG:twin.show:Displaying image
[2024-04-10 02:32:30] INFO:twin.cli:Command completed
```

Capture image from video
------------------------

### Usage

```shell
> twin capture --help
usage: twin capture [-h] (-i INPUT_FILE | -c) -n IMAGE_NUM

Read video from file or camera and display n-th frame in popup

options:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        Path of file from which to read the video
  -c, --camera
  -n IMAGE_NUM, --image-num IMAGE_NUM
                        Index of the frame to display
```

### Example (video file)

```shell
> twin -vv capture -i tests/videos/Hollywood2/scenes/AVIClipsScenes/sceneclipautoautotrain00133.avi -n 10
[2024-04-10 03:21:49] DEBUG:twin.cli:Launching command 'capture'
[2024-04-10 03:21:49] DEBUG:twin.capture:Capturing image from video file 'tests/videos/Hollywood2/scenes/AVIClipsScenes/sceneclipautoautotrain00133.avi'
[2024-04-10 03:21:49] DEBUG:twin.capture:Ignoring frame 1
[2024-04-10 03:21:49] DEBUG:twin.capture:Ignoring frame 2
[2024-04-10 03:21:49] DEBUG:twin.capture:Ignoring frame 3
[2024-04-10 03:21:49] DEBUG:twin.capture:Ignoring frame 4
[2024-04-10 03:21:49] DEBUG:twin.capture:Ignoring frame 5
[2024-04-10 03:21:49] DEBUG:twin.capture:Ignoring frame 6
[2024-04-10 03:21:49] DEBUG:twin.capture:Ignoring frame 7
[2024-04-10 03:21:49] DEBUG:twin.capture:Ignoring frame 8
[2024-04-10 03:21:49] DEBUG:twin.capture:Ignoring frame 9
[2024-04-10 03:21:49] DEBUG:twin.capture:Displaying frame
[2024-04-10 03:21:52] INFO:twin.cli:Command completed
```

(Frame opens in popup)

### Example (default camera)

```shell
> twin -vv capture --camera -n 10                                                   
[2024-04-10 03:22:26] DEBUG:twin.cli:Launching command 'capture'
[2024-04-10 03:22:26] DEBUG:twin.capture:Capturing image from default camera
[2024-04-10 03:24:34] DEBUG:twin.capture:Ignoring frame 1
[2024-04-10 03:24:34] DEBUG:twin.capture:Ignoring frame 2
[2024-04-10 03:24:34] DEBUG:twin.capture:Ignoring frame 3
[2024-04-10 03:24:34] DEBUG:twin.capture:Ignoring frame 4
[2024-04-10 03:24:34] DEBUG:twin.capture:Ignoring frame 5
[2024-04-10 03:24:34] DEBUG:twin.capture:Ignoring frame 6
[2024-04-10 03:24:34] DEBUG:twin.capture:Ignoring frame 7
[2024-04-10 03:24:34] DEBUG:twin.capture:Ignoring frame 8
[2024-04-10 03:24:34] DEBUG:twin.capture:Ignoring frame 9
[2024-04-10 03:24:34] DEBUG:twin.capture:Displaying frame
[2024-04-10 03:25:20] INFO:twin.cli:Command completed
```