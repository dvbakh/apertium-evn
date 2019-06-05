#!/bin/bash

total=`cat test_data/*.txt  | sed 's/[^а-яӈһа̄э̄о̄ӣӯе̄ёА-ЯӇҺА̄Э̄О̄ӢӮЕ̄Ё]\+/ /g' | tr ' ' '\n'  | grep -v '^$' | wc -l`
echo $total
unknown=`cat test_data/*.txt  | sed 's/[^а-яӈһа̄э̄о̄ӣӯе̄ёА-ЯӇҺА̄Э̄О̄ӢӮЕ̄Ё]\+/ /g' | tr ' ' '\n'  | grep -v '^$' | hfst-proc -qp evn.automorf.hfst  | grep '*' | wc -l`
echo $unknown
calc "(($total-$unknown)/$total)*100"
