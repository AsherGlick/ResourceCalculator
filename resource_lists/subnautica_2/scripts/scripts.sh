mkdir -p tmp ../items
cat list.txt | while read f; do curl "${f}" -o "tmp/$(basename "${f}")"; done

for img in tmp/*.png; do
  filename=$(basename "${img%.*}")
  newname=$(echo "$filename" | tr '[:upper:]' '[:lower:]' | tr -d '_.')
  magick "$img" -resize 50x50 -background none -gravity center -extent 50x50 "../items/$newname.png"
done

rm -rf tmp
