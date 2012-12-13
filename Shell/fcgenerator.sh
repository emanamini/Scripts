#!/bin/bash
# To get more information: http://bit.ly/Td2Y02
# Translation target:
TARGETT="fa"
# Translate from:
FROMT="en"
readonly URL="http://translate.google.com/translate_tts?tl=${FROMT}&q="

# By default use google translate to translate and pronouncement
GTranslate=true
GEspeak=true


function usage
{
    echo "You can use $0 like this:
   ${0} -w <WORD> -d <DECKNAME>
You also can use this options:
   -i <DECKNAME>     Copy <DECKNAME>s media files to your
                     anki path.
   -t <translation>  To give it an manual translation insteat
                     of using google translation.
   -e                Disable google translation pronouncement
                     and use installed espeak program. requires: espeak
   -d <DECKNAME>     Specify Deck name.
   -T <TARGET>       Specify target language. something like en, fa...
   -F <FROM>         Which language the script have to translate from.
                     default value is auto.
    To get more information: http://bit.ly/Td2Y02"
    exit 0
}

# Dependency check function:
# I used this function: http://www.snabelb.net/content/bash_support_function_check_dependencies
function deps(){
    DEPENDENCIES=$@    
    deps_ok=YES
    for dep in $DEPENDENCIES
    do
	if ! which $dep &>/dev/null;  then
	    echo "$dep is not installed. please install it and try again."
	    deps_ok=NO
	fi
    done
    if [[ "$deps_ok" == "NO" ]]; then
        echo -e "Unmet dependencies ^"
	echo -e "Aborting!"
        exit 1
    else
        return 0
    fi
}

# Check requires dependency:
deps fribidi ffmpeg curl html2text

function checkDKPATH
{
    [ ! -d ~/.anki/decks/ ] || {
	echo "error: I can't find ~/.anki/decks.
please install copy media files manually"
	exit 1
    }
}

# Scan arguments:
while getopts "heTFi:w:t:d:" opt; do
    case $opt in
	i)
	    DECKNAME=$OPTARG
	    [ -d ${DECKNAME}.media ] && cp -r ${DECKNAME}.media ~/.anki/decks/ && \
		echo "${DECKNAME} media files installed." \
		|| echo "I can't find ${DECKNAME.media}" && exit 1
	    exit 0
	    ;;
	w)
	    WORD="$OPTARG"
	    SOUNDF=${WORD// /_}
	    echo $SOUNDF
	    ;;
	t)
	    TRANSLATION=$OPTARG
	    ;;
	e)
	    deps espeak
	    GEspeak=false
	    echo "Sound will generate with your installed espeak program."
	    ;;
	d)
	    DECKNAME=$OPTARG
	    ;;
	T)
	    TARGETT=$OPTARG
	    ;;
	F)
	    FROMT=$OPTARG
	    ;;
	h)
	    usage
	    exit 0
	    ;;
    esac
done

# Check if WORD and DECKNAME is specified.
[ ! "$WORD" ] && echo "What I have to translate for you? huh? say it to me
with -w option :D" && exit 1
[ ! "$DECKNAME" ] && echo "You have to use -d option to specify deck name." && exit 1

# Make Decks media directory.
DECKMedia=${DECKNAME}.media
[ ! -d $DECKMedia ] && mkdir $DECKMedia \
    && echo "Deck media directory created."

# If the translation didn't pass, find translation on google translation website
if [ ! "$TRANSLATION" ]; then
    # I used this script: http://crunchbang.org/forums/viewtopic.php?id=17034
    result=$(curl -s -i --user-agent "" -d "sl=$FROMT" -d "tl=$TARGETT" --data-urlencode "text=$WORD" http://translate.google.com)
    encoding=$(awk '/Content-Type: .* charset=/ {sub(/^.*charset=["'\'']?/,""); sub(/[ "'\''].*$/,""); print}' <<<"$result")
    TRANSLATION=$(iconv -f $encoding <<<"$result" |  awk 'BEGIN {RS="</div>"};/<span[^>]* id=["'\'']?result_box["'\'']?/' | html2text)
fi

# Generate/Download pronouncement sound file.
if ! $GEspeak; then
    espeak -w ${SOUNDF} "$WORD"
    echo "Sound file generated."
else
    echo "Downloading the sound file..."
    # I used this script: https://gist.github.com/873364
    wget -q -U Mozilla -O ${SOUNDF} "${URL}${WORD}"
    echo "Sound file downloaded."
fi 

# Decode and move downloaded/generated sound file to media path
# with ogg format.
ffmpeg -loglevel panic -i ${SOUNDF} -acodec libvorbis $DECKMedia/${SOUNDF}.ogg \
    && rm -v ${SOUNDF} && echo "Generated/Downloaded sound file, is encoded!"

echo "${WORD}[sound:${SOUNDF}.ogg];${TRANSLATION}" >> $DECKNAME.txt \
    && echo "$WORD translated to $TRANSLATION and added to deck." | fribidi
