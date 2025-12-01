SHELL=/bin/bash
export PATH := $(CURDIR):$(PATH)
.SILENT:

help: ## show this help
	@gawk 'BEGIN { FS=":.*?## ";c="\033[1;3"; r="\033[0m";            \
		             printf "\n%s6mcd src; make%s [%s3moptions%s]:\n\n",c,r,c,r} \
         NF==2 && $$1~/^[a-z0-9A-Z_-]+/{                              \
				         printf "  %s2m%-15s%s %s\n",c,$$1,r,$$2}' $(MAKEFILE_LIST)

docs  : htmls mds pdfs ## make all docs
htmls : ../docs/act.html ../docs/binr.html  
mds   : ../docs/act.1.md ../docs/act_data.5.md ../docs/binr.md ../docs/act.md   
pdfs  : ../docs/binr.pdf ../docs/act.pdf ../docs/compart.pdf 

../docs/%.md : ../src/%.lua ## lua ==> markdown
	../sh/lua2md $^ > $@

locs: ## print LOCS
	gawk '/^(local)? ?function/ { fun=NR } \
	        fun && /^[ \t]*$$/ { print NR-fun; fun=0 }'  ../src/*.lua \
					| sort -n | fmt -20

../docs/%.html : %.lua ../etc/brain.png ../etc/header.md ## lua to html
	mkdir -p ~/tmp
	cat $<  | gawk 'BEGIN { FS=";;"} \
	                NR==1 { system("cat ../etc/header.md") ; next }  \
	                NF==2 && sub(/^-- /,"",$$1) {$$0= "-- <b>"$$1"</b><br>"$$2} \
	                1 ' > ~/tmp/$< 
	pycco -d  ../docs ~/tmp/$<
	echo "p {text-align:right;}" >> ../docs/pycco.css
	echo "h2 {padding-top: 3px; border-top: 1px solid #000;}" >> ../docs/pycco.css

sh: ## run a customized shell
	../sh/ell

pull: ## update from main
	git pull

push: ## commit to main
	git commit -am saving;  git push; git status

../docs/act.1.md      :; pandoc -s -f man -t markdown ../src/act.1 -o $@
../docs/act_data.5.md :; pandoc -s -f man -t markdown ../src/act_data.5 -o $@

../docs/%.pdf: %.lua ## lua ==> pdf
	echo "pdf-ing $@ ... "
	a2ps                        \
		--file-align=virtual       \
		--line-numbers=1            \
		--pro=color                  \
		--lines-per-page=120          \
		--pretty=../etc/lua.ssh         \
		--left-title=""                 \
		--borders=no                     \
	  --right-footer="page %s. of %s#"  \
		--landscape                        \
		--columns 3                         \
		-M letter                            \
		-o - $^ | ps2pdf - $@
	open $@
