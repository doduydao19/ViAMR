echo 'Converting DP to AMR'
python convertDP2AMR.py
echo 'Converting, done!'

echo 'Generate rule '
python gen_rule.py
echo 'Generate, done!'

echo 'Make AMR PENMAN format:'
python make_penman.py
echo 'Make, done!'

echo 'Make data for evaluate:'
python pre_evaluate.py
echo 'Make, done!'


echo 'Evaluate'
output_file='result_eval.txt'
smatch.py --ms --pr -f test_500.amr gold_500.amr > $output_file
echo 'Evaluate, done! The output is written to the file:' $output_file
