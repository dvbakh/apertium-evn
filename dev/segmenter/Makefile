LANG1=evn


all: $(LANG1).segmenter.hfst

#$(LANG1).automorf.hfst: .deps/$(LANG1).LR.hfst .deps/spellrelax.hfst                        
#	hfst-compose-intersect -1 $< -2 .deps/spellrelax.hfst | hfst-invert | hfst-fst2fst -O -o $@

# Special twol file with space for morpheme boundary
$(LANG1)-seg.twol.hfst: apertium-$(LANG1).$(LANG1)-seg.twol
	hfst-twolc $< -o $@

# OUT: Analysis:Segmented surface form
# вульгарнай<adj><sg><ins><px1pi>:вульгарна ид ит
$(LANG1)-seg.hfst: ../../.deps/$(LANG1).LR.lexc.hfst $(LANG1)-seg.twol.hfst
	hfst-compose-intersect -1 ../../.deps/$(LANG1).LR.lexc.hfst -2 $(LANG1)-seg.twol.hfst | hfst-minimise -o $@

# OUT: Surface form:Segmented surface form
# бурьямӣрка̄м:бурья мӣ р ко̄ м
$(LANG1).seg.hfst: $(LANG1).inv_seg.hfst $(LANG1)-seg.hfst
$(LANG1).seg.hfst: ../../.deps/$(LANG1).LR.hfst $(LANG1)-seg.hfst
	#hfst-compose-intersect -1 $(LANG1).inv_seg.hfst -2 $(LANG1)-seg.hfst -o $@
	hfst-compose -1 $(LANG1).inv_seg.hfst -2 $(LANG1)-seg.hfst -o $@

# OUT: Surface form:analysis
# йэгиндяррпчукакӯндук:йэгиндяр<adv><attr5><pchu><ints1><sg><abl>
$(LANG1).inv_seg.hfst: ../../.deps/$(LANG1).LR.hfst 
	hfst-compose-intersect -1 ../../.deps/$(LANG1).LR.hfst -2 ../../.deps/spellrelax.hfst | hfst-invert -o $@ 
#	hfst-invert ../../.deps/$(LANG1).LR.hfst -o $@ 

# Optimised lookup version
$(LANG1).segmenter.hfst: $(LANG1).seg.hfst
	hfst-minimise $(LANG1).seg.hfst | hfst-fst2fst -O -o $@

clean:
	rm *.hfst
