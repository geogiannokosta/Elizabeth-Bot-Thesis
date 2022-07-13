import json
import numpy as np

def sentiment_avg(filename):
	"""Basic average sentiment"""

	count = 0
	result = 0

	with open(filename) as json_file:
	    for line in json_file:
	    	# print(line.strip())
	    	data = json.loads(line.strip())

	    	result+=data['compound']
	    	count+=1

	return result/count

def sentiment_weight_avg(filename):
	"""Weighted average sentiment using y=|x|"""

	num = 0 #numerator
	den = 0 #denominator

	with open(filename) as json_file:
		for line in json_file:
			
			data = json.loads(line.strip())

			num+=data['compound']*abs(data['compound'])
			den+=abs(data['compound'])

	return num/den

def sentiment_weight2_avg(filename):
	"""Weighted average sentiment using y=x^2"""

	num = 0 #numerator
	den = 0 #denominator

	with open(filename) as json_file:
		for line in json_file:
			
			data = json.loads(line.strip())

			num+=data['compound']*(data['compound'])**2
			den+=(data['compound'])**2

	return num/den

def sentiment_threshold_avg(filename):
	"""Average sentiment, cutting out sentiment values between [-.2,.2]"""

	count = 0
	result = 0

	with open(filename) as json_file:
		for line in json_file:			
			data = json.loads(line.strip())

			if data['compound'] > 0.2 or data['compound'] < -0.2:
				result+=data['compound']
				count+=1

	return result/count

def sentiment_confidence_avg(filename):
	"""Average sentiment, multiplying confidence of the result with the compound result."""

	num = 0 #numerator
	den = 0 #denominator

	with open(filename) as json_file:
		for line in json_file:			
			data = json.loads(line.strip())
			
			num+=data['compound']*data['confidence']
			den+=data['confidence']

	return num/den

# Try sentiment average weighted by percentiles

# def sentiment_avg_perc(filename):
# 	"""Weighted average sentiment using data percentiles"""

# 	count = 0 
# 	result = 0 
# 	compounds = []
# 	compounds_real =[]

# 	with open(filename) as json_file:
# 		for line in json_file:
			
# 			data = json.loads(line.strip())
# 			compounds.append(abs(data['compound']))

# 	# 		compounds_real.append(data['compound'])
# 	# seires 36,39 tis exw gia na ektipwsw ta compounds 
# 	# kai na dw pou kimanthike h syzhthsh
# 	# print(compounds_real)

# 	sent_percentile = np.percentile(compounds, 75)

# 	# isws na xrisimopoiithei san threshold
# 	# oti dld h timh pou tha bgei (edw px 0.296) tha einai to threshold gia
# 	# to poies times the ypologistoun ston MO

# 	with open(filename) as json_file:
# 		for line in json_file:
# 			data = json.loads(line.strip())

# 			if data['compound'] > sent_percentile or data['compound'] < -sent_percentile:
# 						result+=data['compound']
# 						count+=1

# 	return result/count

if __name__ == '__main__':
	# negative
	print("negative")
	print(sentiment_avg("logs/log-2022-05-09-22-20-58.json"))
	print(sentiment_weight_avg("logs/log-2022-05-09-22-20-58.json"))
	print(sentiment_weight2_avg("logs/log-2022-05-09-22-20-58.json"))
	print(sentiment_threshold_avg("logs/log-2022-05-09-22-20-58.json"))
	print(sentiment_confidence_avg("logs/log-2022-05-09-22-20-58.json"))

	# positive
	print("positive")
	print(sentiment_avg("logs/log-2022-05-09-22-09-16.json"))
	print(sentiment_weight_avg("logs/log-2022-05-09-22-09-16.json"))
	print(sentiment_weight2_avg("logs/log-2022-05-09-22-09-16.json"))
	print(sentiment_threshold_avg("logs/log-2022-05-09-22-09-16.json"))
	print(sentiment_confidence_avg("logs/log-2022-05-09-22-09-16.json"))

	# # whole conv from that day - neutral (?)
	print("whole")
	print(sentiment_avg("logs/log-2022-05-09.json"))
	print(sentiment_weight_avg("logs/log-2022-05-09.json"))
	print(sentiment_weight2_avg("logs/log-2022-05-09.json"))
	print(sentiment_threshold_avg("logs/log-2022-05-09.json"))
	print(sentiment_confidence_avg("logs/log-2022-05-09.json"))