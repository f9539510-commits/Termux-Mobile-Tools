#!/data/data/com.termux/files/usr/bin/bash
read -p "اكتب الرقم: " num
if [ "$num" = "13" ]; then
termux-open-url "http://websdr.ewi.utwente.nl:8901"
else
echo الرقم غلط لازم 13
fi
