echo "Running tests..."
echo

output0=$(python3 ./processtown.py)
expected_output0="\"Mini Town\"
3,\"1 First Street\",\"2 First Street\"
2,\"1 Second Street\",\"1 First Street\"
3,\"2 First Street\",\"1 Second Street\""

if [ $? -eq 0 ] ; then
  echo "Pass: Program exited zero"
else
  echo "Fail: Program did not exit zero"
  exit 1
fi

echo
echo "Should print town in standard format without any flags"
if [ "$output0" == "$expected_output0" ] ; then
  echo "Pass: Test 0 output is correct"
else
  echo "Fail: Test 0"
  echo "Expected '$expected_output0'"
  echo "but got: '$output0'"
  exit 1
fi

output1=$(python3 ./processtown.py -s)
expected_output1="\"Mini Town\"
3,\"1 First Street\",\"2 First Street\"
2,\"1 Second Street\",\"1 First Street\"
3,\"2 First Street\",\"1 Second Street\""

echo
echo "Should print town in standard format with -s flag"
if [ "$output1" == "$expected_output1" ] ; then
  echo "Pass: Test 1 output is correct"
else
  echo "Fail: Test 1"
  echo "Expected '$expected_output1'"
  echo "but got: '$output1'"
  exit 1
fi

output2=$(python3 ./processtown.py -a)
expected_output2="\"Mini Town\"
\"1 First Street\"
\"2 First Street\"
\"1 Second Street\"
\"1 First Street\",\"2 First Street\",3
\"1 Second Street\",\"1 First Street\",2
\"2 First Street\",\"1 Second Street\",3"

echo
echo "Should print town in alternate format with -a flag"
if [ "$output2" == "$expected_output2" ] ; then
  echo "Pass: Test 2 output is correct"
else
  echo "Fail: Test 2"
  echo "Expected '$expected_output2'"
  echo "but got: '$output2'"
  exit 1
fi

output3=$(python3 ./processtown.py -r static/MiniTown.dat -s)
expected_output3="\"Mini Town\"
3,\"1 First Street\",\"2 First Street\"
2,\"1 Second Street\",\"1 First Street\"
3,\"2 First Street\",\"1 Second Street\""

echo
echo "Should read town from file and then print in standard format when combining -r + -s flags"
if [ "$output3" == "$expected_output3" ] ; then
  echo "Pass: Test 3 output is correct"
else
  echo "Fail: Test 3"
  echo "Expected '$expected_output3'"
  echo "but got: '$output3'"
  exit 1
fi


expected_output4="\"MT Plan A\"
Connected: True
Total Cost: 6
Optimal: 5"

output4=$(python3 ./processtown.py -e static/MiniTownPavingPlan.dat)

echo
echo "Should evaluate paving plan"
count=$(echo $output4 | wc -l)
if [ "$output4" == "$expected_output4" ] ; then
  echo "Pass: Test 4 output is correct"
else
  echo "Fail: Test 4"
  echo
  echo "Expected '$expected_output4'"
  echo
  echo "but got: '$output4'"
  exit 1
fi


output5=$(python3 ./processtown.py -c 5 6 -s)

echo
echo "Should create connected town with correct number of streets"
count=$(echo "$output5" | wc -l)
if [ $count == 11 ] ; then
  echo "Pass: Test 5 output is correct"
else
  echo "Fail: Test 5 - number of streets wrong"
  exit 1
fi



output6=$(python3 ./processtown.py -p static/test_file.txt)
expected_file_content="\"Mini Town Paving Plan\"
\"1 Second Street\",\"1 First Street\"
\"1 First Street\",\"2 First Street\""
file_content=$(cat static/test_file.txt)

echo
echo "Should pave a new town and write to file"
if [ -f static/test_file.txt ] ; then
  # file exists, check contents
  if [ "$file_content" == "$expected_file_content" ] ; then
    echo "Pass: Test 6 output is correct"
  else
    echo "Fail: Test 6"
    echo "Expected '$expected_file_content'"
    echo "but got: '$file_content'"
    exit 1
  fi
  rm static/test_file.txt
else
  echo "Fail: Test 6"
  echo "No file found"
  exit 1
fi



echo
echo "All tests passed."
exit 0
