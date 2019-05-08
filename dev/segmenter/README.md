

# Example 

```echo "нуӈанӈин" | hfst-lookup evn.segmenter.hfst```

expected answer: нуӈан>ӈи>н

```echo "оронду" | hfst-lookup evn.segmenter.hfst```

expected answer: оро>н>ду (will be changed to орон>ду later in lexc)
