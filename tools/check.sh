while true
do
	sleep 1
	date
	len=`ls Working/Downloads | wc -l`
	echo "$len / 36876 : "
	echo "$len / 36876 * 100" | bc -l
	echo "----------------------------"
done
