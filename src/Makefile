-include ../Makefile

egXomoG: ## big file
	./binr.lua -l 5 -e 5 -r 20 -f ~/gits/moot/optimize/process/xomo_ground.csv --score

egs: ## run all tests
	./binr.lua --all

TASKS := $(wildcard ~/gits/moot/optimize/[bhmp]*/*.csv)
JOBS := $(addprefix run-, $(TASKS))

egxai: $(JOBS)

.PHONY: egxai $(JOBS)

$(JOBS): run-%: %
	@mkdir -p ~/tmp/xai
	@echo "--- [STARTED] Processing $<"
	@# use $(notdir $<) to get just 'data.csv' without the folder path
	@./xai4 -xai $< > ~/tmp/xai/$(notdir $<).log 2>&1
	@echo "--- [DONE]    Finished   $<"

#magxaie -j16 --output-sync=target:
#gmake  -j16 --output-sync=target   egxai

TASKS := $(wildcard ~/gits/moot/optimize/[bhmp]*/*.csv)
JOBS := $(addprefix run1-, $(TASKS))

egxai: setup-dir $(JOBS)

setup-dir:
	@mkdir -p ~/tmp/xai

.PHONY: egxai $(JOBS)

run1-%: %
	@echo "--- [STARTED] Processing $<"
	@./xai4 -xai $< > ~/tmp/xai/$(notdir $<).log 2>&1
	@echo "--- [DONE]    Finished   $<"

