# Evenki morphological analyser, generator and segmenter

The repository contains files for analysing, generating and segmenting wordforms in Evenki.

Full version and more description can be found in previous [README](..blob/master/README).

### Light version (only HFST is required)

#### Requirements
* HFST: see [installation](https://github.com/hfst/hfst/wiki/Download-And-Install), e.g.```sudo apt-get install hfst```

#### Usage

1. clone the repo
  
2. run:  
    * ```make``` for the **bare analyser**  
    * ```make -f Makefile_deriv``` for the analyser with **extended derivation**  
    * ```make -f Makefile_relax``` for the analyser that supports **dialectal features**  
    * ```make -f Makefile_relax_deriv``` for the analyser with **extended derivation** that supports **dialectal features**  
    
    as a result, the following transducers are created:  
    
    ```evn.automorf.hfst```: a transducer for morphological **analysis** (surface form : analysis)  
    ```evn.autogen.hfst```: a transducer for morphological **generation** (analysis : surface form)  
    ```evn.segmenter.hfst```: a transducer for morphological **segmentation** (surface form : segmented form)  
      
3.  run:   
     * ```cat path/to/file | hfst-proc evn.automorf.hfst``` for **analysing a file**  
     * ```echo "a word in Evenki" | hfst-lookup evn.automorf.hfst``` for **analysing a wordform**  
     * ```echo "lemma<with><tags>" | hfst-lookup evn.autogen.hfst``` for **generating** a wordform  
     * ```python3 segment.py "wordform" [path to segmenter]``` for **segmenting** a wordform and  
                                                                              getting the segmented form in the **original spelling**
    
3.  use in python:  
        
     install: ```pip install hfst```  
    
    *  analysis, generation, segmentation:
   
       ```python
       import hfst
       
       # load a transducer from the ones listed above
       transducer = hfst.HfstInputStream('path/to/transducer').read()
       
       # get the result for a wordform:
       result = transducer.lookup("wordform")
       ```
   
    *  segmentation:
   
       ```python
       # load a function for getting segmentation in original spelling 
       from segment import segment
       
       # segment the word 
       # (loaded transducer for segmentation can be passed instead of the path/to/transducer) 
       segmented_word  = segment('wordform', 'path/to/transducer')
       ```


