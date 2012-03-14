for file_name in *.jpg
do
  echo $file_name
  convert -rotate -90 $file_name `basename $file_name .jpg`out.jpg
done
