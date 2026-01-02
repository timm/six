-include ../Makefile

egXomoG: ## big file
	./binr.lua -l 5 -e 5 -r 20 -f ~/gits/moot/optimize/process/xomo_ground.csv --score

egs: ## run all tests
	./binr.lua --all

TASKS := $(wildcard ~/gits/moot/optimize/[bhmp]*/*.csv)

egxai: $(TASKS)

$(TASKS):
	mkdir -p ~/tmp/xai
	@echo "--- [STARTED] Processing $@"
	@./xai4 -xai $@ > ~/tmp/xai/$@.log 2>&1
	@echo "--- [DONE]    Finished   $@"

#magxaie -j16 --output-sync=target:
#make  -j16 --output-sync=target   egxai
