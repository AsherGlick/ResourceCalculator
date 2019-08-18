#!/bin/bash

mogrify -path ../items -resize 100x -format png raw-material-images/*
mkdir raw-weapon-images-tmp

mogrify -path raw-weapon-images-tmp -resize 100x -format png raw-weapon-images/*

overlay_level() {
	filename=$(basename -- "$1")
	filename="${filename%.*}"

	echo $filename
	composite lv4.png raw-weapon-images-tmp/"$filename".png ../items/"$filename"lv4.png;
	composite lv3.png raw-weapon-images-tmp/"$filename".png ../items/"$filename"lv3.png;
	composite lv2.png raw-weapon-images-tmp/"$filename".png ../items/"$filename"lv2.png;
	cp raw-weapon-images-tmp/"$filename".png ../items/"$filename"lv1.png;
	# composite lv1.png raw-weapon-images-tmp/"$filename".png ../items/"$filename"lv1.png;
}

for filename in raw-weapon-images-tmp/*; do
	overlay_level $filename
done

rm -rf raw-weapon-images-tmp
