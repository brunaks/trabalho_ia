cat Output.txt | grep _spok_ | echo "spok: $(wc -l)"
cat Output.txt | grep _news_ | echo "news: $(wc -l)"
cat Output.txt | grep _mag_ | echo "mag: $(wc -l)"
cat Output.txt | grep _fic_ | echo "fic: $(wc -l)"
cat Output.txt | grep _acad_ | echo "acad: $(wc -l)"
