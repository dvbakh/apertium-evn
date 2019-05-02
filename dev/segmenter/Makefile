LANG1=evn


all: $(LANG1).segmenter.hfst


$(LANG1)-seg.twol.hfst: apertium-$(LANG1).$(LANG1)-seg.twol
	hfst-twolc $< -o $@

$(LANG1)-seg.hfst: ../../.deps/$(LANG1).LR.lexc.hfst $(LANG1)-seg.twol.hfst
	hfst-compose-intersect -1 ../../.deps/$(LANG1).LR.lexc.hfst -2 $(LANG1)-seg.twol.hfst | hfst-minimise -o $@

$(LANG1).segmenter.hfst: ../../$(LANG1).automorf.hfst $(LANG1)-seg.hfst
	hfst-compose-intersect -1 ../../.deps/$(LANG1).LR.hfst -2 $(LANG1)-seg.hfst | hfst-minimise | hfst-fst2fst -w -o $@

clean:
	rm *.hfst
