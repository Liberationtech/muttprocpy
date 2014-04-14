cd /home/oivvio/coderepositories/muttprocpy
python 2013mailinglists.py
python 2013mailinglists_oivvio_gmail.py

mv ~/mail/unsorted /tmp

mkdir ~/mail/unsorted
mkdir ~/mail/unsorted/tmp
mkdir ~/mail/unsorted/cur
mkdir ~/mail/unsorted/new


for f in $(find /tmp/unsorted -type f)
do 
    cat $f|procmail -m /home/oivvio/.procmailrc
    echo -n "."
done

rm -fr /tmp/unsorted
