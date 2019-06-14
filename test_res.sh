#!/bin/bash

mkdir -p res

evaluate () {

    total=`cat test_data/$1.txt | sed 's/[^а-яӈһа̄э̄о̄ӣӯе̄ёА-ЯӇҺА̄Э̄О̄ӢӮЕ̄Ё]\+/ /g' | tr ' ' '\n'  | grep -v '^$' | wc -l`
    cat test_data/$1.txt | sed 's/[^а-яӈһа̄э̄о̄ӣӯе̄ёА-ЯӇҺА̄Э̄О̄ӢӮЕ̄Ё]\+/ /g' | tr ' ' '\n'  | grep -v '^$' | sed -e 's/\(.*\)/\L\1/' | hfst-proc evn.automorf.hfst > res/$1
    unknown=`cat res/$1 | grep '*' | wc -l`
    analyses=`cat res/$1 | grep -v '*' | cut -f2- -d'/' | sed 's/\//\n/g' | wc -l`

    coverage=`calc "(($total-$unknown)/$total)*100" | tr '\t' ' '`
    mean_ambig=`calc $analyses/$total | tr '\t' ' '`

    echo -e "$1:\n\tcoverage: $coverage, mean_ambiguity: $mean_ambig, unknown/total: $unknown/$total"

}

evaluate newspaper
evaluate siblang
evaluate iea_ras
