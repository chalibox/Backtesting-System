import numpy
import pandas
import random
import csv
import datetime
import matplotlib.pyplot as plt

# Defines the strategy
class RandomStrategy:
	def __init__(self, num_random, historical_start, historical_end, recent_end, threshold_pct, path):

		# parameters needed for this strategy
		self.num_random = num_random
		self.historical_start = historical_start
		self.historical_end = historical_end
		self.recent_end = recent_end
		self.historical_price_raw = read_data(path)
		self.threshold_pct = threshold_pct

	
	def read_historical_price(self):

		'''
		Read part of the data in order to leave the rest for testing. 
		This is to make sure that the strategy doesn't 'cheat'.
		'''

		# Use historical_start and historical_end to identify the part needed
		start_index = self.historical_price_raw.loc[self.historical_price_raw['Date'] == self.historical_start].index.tolist()[0]
		end_index = self.historical_price_raw.loc[self.historical_price_raw['Date'] == self.historical_end].index.tolist()[0]
		historical_price = self.historical_price_raw.iloc[start_index:end_index+1,:]
		historical_price = historical_price.reset_index(drop = True)
		return historical_price

	
	def read_recent_price(self):

		'''
		This part of the data is for testing
		'''

		# Read the data just like read_historical_price
		recent_start_index = self.historical_price_raw.loc[self.historical_price_raw['Date'] == self.historical_end].index.tolist()[0] + 1
		recent_end_index = self.historical_price_raw.loc[self.historical_price_raw['Date'] == self.recent_end].index.tolist()[0]
		recent_price = self.historical_price_raw.iloc[recent_start_index:recent_end_index+1,:]
		recent_price = recent_price.reset_index(drop = True)
		return recent_price

	
	def make_random_price(self):

		'''
		This function runs the strategy
		'''

		# call the above functions
		price_history = self.read_historical_price()
		price_recent = self.read_recent_price()

		# Find out how much the ticker moves for one timeframe in average (both up and down)
		positive = price_history['p_change'][price_history['p_change'] > 0].mean()
		negative = price_history['p_change'][price_history['p_change'] < 0].mean()
		
		# Create an empty list to store all the possibilities.
		compare_random = []

		# loop through random lines created
		for x in range(self.num_random):

			# Create an empty list to store generated trend line
			random_price = []
			random_price.append(price_recent['Close'][0])
			for i in range(len(price_recent['Close'])):

				# calculate new price every timeframe and append it to the list
				new_price = random_price[i] * (100 + random.choice([positive,negative])) / 100
				random_price.append(new_price)

			# Each column represents one generated trend line, num random is the total number of trend lines
			price_recent['random_{}'.format(x)] = random_price[:len(price_recent['Close'])]

			# Use compare_random to find the trend line with the lowest value
			compare_random.append(price_recent['random_{}'.format(x)].mean())
		
		# Use the last price of the lowest trend line, compare it with the real price, if the distance between them is smaller than threshold percentage, return true, else, return false
		if price_recent['random_{}'.format(compare_random.index(min(compare_random)))].iloc[-1] > price_recent['Close'].iloc[-1] * (1-(self.threshold_pct * 0.01)) and price_recent['random_{}'.format(compare_random.index(min(compare_random)))].iloc[-1] < price_recent['Close'].iloc[-1] * (1+(self.threshold_pct * 0.01)):
			return price_recent, True
		else:
			return price_recent, False



def read_data(file_path):

	'''
	This function handles data reading part
	'''

	try:
		rawData = pandas.read_csv(file_path)

		# This is to make sure that the data is in correct order
		d0 = datetime.datetime.fromisoformat(rawData['Date'].iloc[0]).timestamp()
		d1 = datetime.datetime.fromisoformat(rawData['Date'].iloc[-1]).timestamp()
		if d0 > d1:

			# Reverse order
			rawData = rawData.iloc[::-1].reset_index(drop = True)

			# Calculate change in percentage
			rawData['p_change'] = rawData['Close'].pct_change() * 100
			rawData = rawData.dropna().reset_index(drop = True)
			return rawData
		else:
			rawData['p_change'] = rawData['Close'].pct_change() * 100
			rawData = rawData.dropna().reset_index(drop = True)
			return rawData
	except:

		# Handles the situation where the headline is lower cased
		rawData = pandas.read_csv(file_path)
		d0 = datetime.datetime.fromisoformat(rawData['date'][0]).timestamp()
		d1 = datetime.datetime.fromisoformat(rawData['date'][-1]).timestamp()
		if d0 > d1:
			rawData = rawData.iloc[::-1].reset_index(drop = True)
			rawData['p_change'] = rawData['close'].pct_change() * 100
			rawData = rawData.dropna().reset_index(drop = True)
			return rawData
		else:
			rawData['p_change'] = rawData['close'].pct_change() * 100
			rawData = rawData.dropna().reset_index(drop = True)
			return rawData



def run_test(data, parameters, path):

	'''
	Loop through all the data and perform backtest
	'''

	# Read inputs from user
	num_random = parameters[0]
	threshold_pct = parameters[1]
	history_interval = parameters[2]
	test_interval = parameters[3]
	prediction = parameters[4]
	money = parameters[5]
	
	# Create x and y lists for plotting
	x = []
	y = []
	y.append(money)
	x.append(data['Date'][0])
	
	# Loop through all the data with a jump of the length of prediction so that the system doesn't buy extra stock when there is no money left.
	for i in range(0, len(data['Date']), prediction):
		try:

			# Identifying values needed for RandomStrategy's parameters
			his_start = data['Date'][i]
			his_end = data['Date'][i + history_interval]
			test_end = data['Date'][i + history_interval + test_interval]
			predict_end = data['Date'][i+ history_interval + test_interval + prediction]
			
			# Runs the strategy
			run = RandomStrategy(num_random,his_start, his_end, test_end,threshold_pct, path)
			result = run.make_random_price()
			if result[1] == False:

				# Log
				print('it is not valid with {} - {}'.format(his_end, test_end))
				pass
			if result[1] == True:

				# Get the price when buying the ticker
				first_day = data['Close'].loc[data['Date'] == test_end].to_list()[0]

				# Get the price when selling the ticker
				predicted_day = data['Close'].loc[data['Date'] == predict_end].to_list()[0]

				# Calculate profit and append it to y list
				predicted_value = ((predicted_day - first_day) / first_day) * 100
				y.append(y[-1] * (predicted_value/100 + 1))

				# Append date to x list
				x.append(test_end)

				# Log
				print('use {} - {} data, test to {}, give prediction of {} percent in {} timeframes'.format(his_start,his_end,test_end,predicted_value,prediction))
		except:
			pass

	# Plot total earning
	plot_result(x,y)	


def plot_result(x, y):

	'''
	Handles matplotlib plotting
	'''

	plt.plot(x,y)
	plt.title(label='Total Earning')
	plt.show()



def check_input(num_random, threshold_pct, history_interval, test_interval, prediction, initial_money):

	'''
	This is to make sure that all user inputs are positive 
	'''

	# Not stacking them all together because this is easier to change the boundary for one parameter
	
	if threshold_pct <= 0 or threshold_pct > 100:
		return False
	if num_random <= 0 or num_random > 1000:
		return False
	if history_interval <= 0:
		return False
	if test_interval <= 0:
		return False
	if prediction <= 0:
		return False
	if initial_money <= 0:
		return False
	return True
