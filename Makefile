DEST=blogspam.net

output: clean
	templer

clean:
	@rm -rf output/ || true

upload: output
	rsync -e "ssh -p 2222" -vazr --delete ./output/ root@${DEST}:/srv/blogspam.net/htdocs/
	rsync -e "ssh -p 2222" -vazr --delete ./cgi-bin/ root@${DEST}:/srv/blogspam.net/cgi-bin/

serve: output
	templer --serve=4433
