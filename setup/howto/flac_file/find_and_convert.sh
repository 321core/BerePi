find ./ -type f -name *.ape | while read file; do
DIR=`dirname "$file"`
NAME=`basename "$file" .ape`
#cuebreakpoints "${DIR}/${NAME}.cue" | shnsplit -o flac "$file" -d "$DIR"
CUR=`pwd`
cd "$DIR"
rm *.flac
shnsplit -f CDImage.cue -t %n-%t -o flac CDImage.ape
cuetag "${NAME}.cue" *.flac
cd "$CUR"
done
