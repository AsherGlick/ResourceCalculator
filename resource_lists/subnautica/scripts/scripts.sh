cat list.txt | while read f; do curl "${f}" -O; done;

for img in *.png; do filename=${img%.*}; magick convert "$filename.png" -resize 50x50 -background none -gravity center -extent 50x50 "out/$filename.png"; done
