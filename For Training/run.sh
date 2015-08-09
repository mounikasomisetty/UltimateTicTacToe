COUNTER=0
while [  $COUNTER -lt 100 ]; do
	echo The counter is $COUNTER
	python New.py 1
	wc -l ProbDis1 ProbDis21 ProbDis22 ProbDis3 ProbDis
	python New.py 2
	wc -l ProbDis1 ProbDis21 ProbDis22 ProbDis3 ProbDis
	python New.py 3
	wc -l ProbDis1 ProbDis21 ProbDis22 ProbDis3 ProbDis

	let COUNTER=COUNTER+1 
done

