mkdir -p res

total=`cat test_data/newspaper.txt | sed 's/[^а-яӈһа̄э̄о̄ӣӯе̄ёА-ЯӇҺА̄Э̄О̄ӢӮЕ̄Ё]\+/ /g' | tr ' ' '\n'  | grep -v '^$' | wc -l`
echo $total
cat test_data/newspaper.txt | sed 's/[^а-яӈһа̄э̄о̄ӣӯе̄ёА-ЯӇҺА̄Э̄О̄ӢӮЕ̄Ё]\+/ /g' | tr ' ' '\n'  | grep -v '^$' | sed -e 's/\(.*\)/\L\1/' | hfst-proc evn.automorf.hfst > res/newspaper_res
unknown=`cat res/newspaper_res | grep '*' | wc -l`
echo $unknown
calc "(($total-$unknown)/$total)*100"

total=`cat test_data/siberian_lang.txt  | sed 's/[^а-яӈһа̄э̄о̄ӣӯе̄ёА-ЯӇҺА̄Э̄О̄ӢӮЕ̄Ё]\+/ /g' | tr ' ' '\n'  | grep -v '^$' | wc -l`
echo $total
cat test_data/siberian_lang.txt | sed 's/[^а-яӈһа̄э̄о̄ӣӯе̄ёА-ЯӇҺА̄Э̄О̄ӢӮЕ̄Ё]\+/ /g' | tr ' ' '\n'  | grep -v '^$' | sed -e 's/\(.*\)/\L\1/' | hfst-proc evn.automorf.hfst > res/siberian_res
unknown=`cat res/siberian_res  | grep '*' | wc -l`
echo $unknown
calc "(($total-$unknown)/$total)*100"

total=`cat test_data/iea_ras.txt | sed 's/[^а-яӈһа̄э̄о̄ӣӯе̄ёА-ЯӇҺА̄Э̄О̄ӢӮЕ̄Ё]\+/ /g' | tr ' ' '\n'  | grep -v '^$' | wc -l`
echo $total
cat test_data/iea_ras.txt | sed 's/[^а-яӈһа̄э̄о̄ӣӯе̄ёА-ЯӇҺА̄Э̄О̄ӢӮЕ̄Ё]\+/ /g' | tr ' ' '\n'  | grep -v '^$' | sed -e 's/\(.*\)/\L\1/' | hfst-proc evn.automorf.hfst > res/iea_res
unknown=`cat res/iea_res  | grep '*' | wc -l`
echo $unknown
calc "(($total-$unknown)/$total)*100"
