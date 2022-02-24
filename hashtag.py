# -*- coding: utf-8 -*-
from TikTokAPI import TikTokAPI
import os
import json
from upload import upload_youtube
import sys, getopt
import socket
socket.setdefaulttimeout(30000)
#kullanımı
#python hashtag.py -i setting.json -o tube.json -t download,merge,delete,upload
# yüklenecek dosyanın temel bilgileri
setting_file = "setting.json"
# youtube api bilgileri
credential_file = "tube.json"
task = "download,merge,delete,upload"
argv = sys.argv[1:]
try:
  opts, args = getopt.getopt(argv,"hi:o:t:k:",["ifile=","ofile=", "tfile=", "kfile="])
except getopt.GetoptError:
  print("hashtag.py -i <inputfile> -o <outputfile> -t <task> -k <keyword>")
  sys.exit(2)
for opt, arg in opts:
  if opt == '-h':
      print('hashtag.py -i <inputfile> -o <outputfile> -t <task> -k <keyword>')
      sys.exit()
  elif opt in ("-i", "--ifile"):
      setting_file = arg
  elif opt in ("-o", "--ofile"):
      credential_file = arg
  elif opt in ("-t", "--tfile"):
      task = arg
  elif opt in ("-k", "--kfile"):
      keyword = arg
print('setting file is =>', setting_file)
print('credential file is =>', credential_file)
print('task is =>', task)
task = task.split(",")
# ffmpeg kurulacak
def clean_hashtag(hastag):
    hashtag_download = hash_tag.replace(" ", "")
    hashtag_download = hashtag_download.encode("ascii", "ignore")
    hashtag_download = hashtag_download.decode()
    return hashtag_download

def birlestir(hashtag):
  hashtag_download = clean_hashtag(hashtag)
  #indirilen dosyaları birleştir
  list_file = "./"+hashtag_download+"/f1.txt"
  hashtag_out = clean_hashtag(hashtag)
  out_file="./out/"+hashtag_out+".mp4"
  if os.path.exists(list_file):
      os.remove(list_file)
  if os.path.exists(out_file):
      os.remove(out_file)
  f = open(list_file, "a")
  dosya_listesi = ""
  for root, dirs, files in os.walk("./"+hashtag_download):
      for file in files:
          if os.path.splitext(file)[1] == '.ts':
              f.write("file '"+file+"'\n")
              dosya_listesi = "./"+hashtag_download+"/"+file+"|"+dosya_listesi
  f.close()
  os.system('ffmpeg -i "concat:'+dosya_listesi+'" -c copy -bsf:a aac_adtstoasc '+out_file)

def dosyalari_sil(hashtag):
  hashtag_download = clean_hashtag(hashtag)
  for f in os.listdir("./"+hashtag_download+"_temp"):
      os.remove(os.path.join("./"+hashtag_download+"_temp", f))
  for f in os.listdir("./"+hashtag_download):
      os.remove(os.path.join("./"+hashtag_download, f))
  os.rmdir("./"+hashtag_download+"_temp")
  os.rmdir("./"+hashtag_download)
  #klasörlerin içindeki dosyaları silme


with open(setting_file) as f:
    d = json.load(f)
cookie = {
  "s_v_web_id": d["s_v_web_id"],
  "tt_webid": d["tt_webid"]
}


def dosyalari_indirme(hash_tag, cookie):
  #hashtag alınıyor klasörler yoksa oluşturuluyor
  #videolar temp alanına iniyor
  #sonra video dönüştürülüyor ve hastag klasörüne taşınıyor
  hashtag_download = clean_hashtag(hash_tag)
  if not os.path.exists(hashtag_download):
    os.makedirs(hashtag_download)
  if not os.path.exists(hashtag_download+"_temp"):
    os.makedirs(hashtag_download+"_temp")
  api = TikTokAPI(cookie=cookie)
  retval = api.getVideosByHashTag(hash_tag, count=30)
  #dosyaları indirme
  for tiktok in retval["itemList"]:
      # Prints the text of the tiktok
      print(tiktok["video"]["id"])
      api.downloadVideoById( tiktok["video"]["id"], "./"+hashtag_download+"_temp/"+tiktok["video"]["id"]+".mp4")
      file_name = tiktok["video"]["id"]+".mp4"
      os.system("ffmpeg -i ./"+hashtag_download+"_temp/"+file_name+" -map 0:a -map 0:v -c:v libx264 -profile:v main -c:a aac -ar 48000 -video_track_timescale 2500 ./"+hashtag_download+"/"+tiktok["video"]["id"]+".ts")
  return retval



if keyword == "":
    hash_tag = d["hashtag"]
else:
    hash_tag = keyword

if "download" in task:
    retval = dosyalari_indirme(hash_tag, cookie)
if "merge" in task:
    birlestir(hash_tag)
if "delete" in task:
    dosyalari_sil(hash_tag)
if "upload" in task:
    upload_youtube(setting_file, credential_file)
