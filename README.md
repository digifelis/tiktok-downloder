# tiktok downloder
 you can download videos from tiktok which you selected hashtag and upload them to the youtube


## usage
python hashtag.py -t <task> -k <keyword>

 ### -t option is download,merge,delete,upload
 ### -k word of hashtag
 
 ### option download => it downloads videos from Tiktok
 ### option merge => it merges videos that downloaded then you can find outfile in out directory
 ### option delete => it deletes videos that downloaded. recommend => use this with merge
 ### option upload => it uploads outfile to youtube if you filled tube.json file.
 
 example
 python hashtag.py -t download,merge,delete -k challenge
 
 ## if you fill tube.json you can upload videos to youtube via API
 
