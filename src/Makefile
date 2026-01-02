-include ../Makefile

egXomoG: ## big file
	./binr.lua -l 5 -e 5 -r 20 -f ~/gits/moot/optimize/process/xomo_ground.csv --score

egs: ## run all tests
	./binr.lua --all

~/tmp/xai4.log:  ## run on many files
	$(MAKE) todo=xai files="$(HOME)/gits/moot/optimize/*/*.csv" run16 | tee $@ 

~/tmp/lurch.log:  ## run on many files
	$(MAKE) todo=lurch files="$(HOME)/gits/moot/optimize/*/*.csv" run16| tee $@ 

run16:
	@mkdir -p ~/tmp
	time ls -r $(files) | xargs -P 16 -n 1 -I{} sh -c 'python3 -B xai4.py --$(todo)  "{}"'


