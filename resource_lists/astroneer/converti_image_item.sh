#! /bin/bash

rep_image=/home/orgams/git/ResourceCalculator/resource_lists/astroneer

# Récuperer la liste de toutes les nouvelles image d'item
for image in `find $rep_image/new_items/* -type f`
do
	resolution=64x64
	convert $image -gravity Center -resize $resolution^ -extent $resolution -transparent white $rep_image/items/${image##*/}
done

# convertir en png de résolution 64x64 en zoomant si ce n'est pas carrer et l'enregister avec le même nom .png dans le rep item