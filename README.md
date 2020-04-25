# libva-log-parser
This is a script to parse libva logs and calculate FPS and average frame width
How to use this script:
python3 parser.gyp -i <input folder which contains libva logs> -o <output csv file name>

Exmaple:
$python3 parser.gyp -i ./libva -o output.csv

The output csv format is:
Time(seconds)	Average FPS 	Average frame width

By end of this script, something will be printed:
1. Total seconds reocrd in the file
2. Average FPS accross the time in files
3. Average frame width accross the time in files
