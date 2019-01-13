while True
do
	sleep 1
	date
	len=`ls Working/Downloads | wc -l`
	echo "$len / 36834 : "
	echo "$len / 36834 * 100" | bc -l
	echo "----------------------------"
done
