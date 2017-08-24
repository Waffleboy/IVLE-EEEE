# IVLEDownloader written in Python

As the saying goes, necessity is the mother of invention. Yj's original IVLEDownloader did not work for me on Ubuntu 16.04. Hence, I wrote this for anyone else who's suffering from the same problem, and cannot live without this amazingly helpful tool.

It's pretty basic now (without any fancy UI) but I'll get to that when I have time, or if someone requests it.

Also, the code is not very clean and properly documented because it was done in a rush, will update when time is available. (Not like anyone is going to read this anyway)

## Instructions

```
git clone git@github.com:Waffleboy/IVLE-EEEE.git
```

Then, set the `FOLDER_DOWNLOAD_LOCATION` to your specified folder, fill in your `LAPI API` key, `IVLE username` and `password`, then just run

```
python main.py
```

A LAPI API key can be obtained by: 

`Going to IVLE, log in, then enter this URL: http://ivle.nus.edu.sg/LAPI/default.aspx`

## Random notes

If you just want to get an IVLE token to play with LAPI yourself and cant seem to figure out how, feel free to use ivle_token_generator.py. I'm surprised there isn't something like this already.

At some point, I might just create a python wrapper for LAPI, depending on time available.
