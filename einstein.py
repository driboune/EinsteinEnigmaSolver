import pandas as pd


house_features = {
	"house_numbers": [0,1,2,3,4],
	"animals": ['dog', 'cat', 'bird', 'horse', 'fish'],
	"drinks": ['tea', 'coffee', 'milk', 'beer', 'water'],
	"nationalities": ['English', 'Swedish', 'Danish', 'Norwegian', 'German'],
	"cig_brands": ['Marlboro', 'Rothman', 'Winfield', 'Dunhill', 'Pall Mall'],
	"colors": ['red', 'white', 'yellow', 'green', 'blue'],
}
#feature_list = []
init_list = []
feature_family_dict = {}
for house_feature_key, house_feature_value in house_features.items():
	for element in house_feature_value:
		init_list.append(element)
		feature_family_dict[element] = house_feature_key
		#feature_list.append(house_feature_key)

df = pd.DataFrame(columns=init_list, index=init_list)


def set_house_features_neighbours(neighbour_left, neighbour_right, feature1, feature2, value):
	if feature1 == neighbour_left and feature_family_dict[feature2]=="house_numbers":
		if feature2 < 4:
			set_house_feature(neighbour_right, feature2+1, value)
	elif feature1 == neighbour_right and feature_family_dict[feature2]=="house_numbers":
		if feature2 > 0:
			set_house_feature(neighbour_left, feature2-1, value)
	elif feature2 == neighbour_left and feature_family_dict[feature1]=="house_numbers":
		if feature1 < 4:
			set_house_feature(neighbour_right, feature1+1, value)	
	elif feature2 == neighbour_right and feature_family_dict[feature1]=="house_numbers":
		if feature1 > 0:
			set_house_feature(neighbour_left, feature1-1, value)

def find_feature_by_feature_family(feature, feature_family):
	for feature_family_feature in house_features[feature_family]:
		if df[feature][feature_family_feature] == True:
			return feature_family_feature
	return None


def set_house_feature(feature1, feature2, value):
	#if the value is already set, the job is already done
	if(df[feature1][feature2]!=value):
		df[feature1][feature2]=value
		#for every element linked to featire1. For example if we KNOW water (element_linked) and dog(element1) are in the same house, then water inherits of the new link with (German)element2
		for element_linked in [key for (key,value) in df[feature1].items() if value==True ]:
			if(df[element_linked][feature2]!=value):
				set_house_feature(element_linked, feature2, value)
		if(value == True):
			#when we know german and green are in the same house, we know german is not in the same house with any other color and every other nationality is with green
			for element_same_family in [x for x in house_features[feature_family_dict[feature1]] if x !=feature1]:
				if(df[element_same_family][feature2]!=value):
					set_house_feature(element_same_family, feature2, False)
			for element_same_family in [x for x in house_features[feature_family_dict[feature1]] if x !=feature2]:
				if(df[feature1][element_same_family]!=value):
					set_house_feature(feature1, element_same_family, False)
		set_house_features_neighbours('green', 'white', feature1, feature2, value)

	#applying symetric connections
	if(df[feature2][feature1]!=value):
		set_house_feature(feature2, feature1, value)

def check_house_features_unknown_neighbours_one_order(neighbour_1, neighbour_2):
	neighbour_1_house_number = find_feature_by_feature_family(neighbour_1, "house_numbers")
	neighbour_2_house_number = find_feature_by_feature_family(neighbour_2, "house_numbers")
	if neighbour_1_house_number != None and neighbour_2_house_number == None:
		neighbour_2_family = feature_family_dict[neighbour_2]
		##check if left is taken
		if neighbour_1_house_number >= 1:
			neighbour_1_left_neighbour_of_neighbour_2_family = find_feature_by_feature_family(neighbour_1_house_number-1, neighbour_2_family)
			if neighbour_1_left_neighbour_of_neighbour_2_family and neighbour_1_left_neighbour_of_neighbour_2_family != neighbour_2:
				if neighbour_1_house_number <= 3:
					set_house_feature(neighbour_2, neighbour_1_house_number+1, True)
		else:
			set_house_feature(neighbour_2, neighbour_1_house_number+1, True)
		##check if left is taken
		if neighbour_1_house_number <= 3:
			neighbour_1_right_neighbour_of_neighbour_2_family = find_feature_by_feature_family(neighbour_1_house_number+1, neighbour_2_family)
			if neighbour_1_right_neighbour_of_neighbour_2_family and neighbour_1_right_neighbour_of_neighbour_2_family != neighbour_2:
				if neighbour_1_house_number >= 1:
					set_house_feature(neighbour_2, neighbour_1_house_number-1, True)
		else: 
			set_house_feature(neighbour_2, neighbour_1_house_number-1, True)

def check_house_features_unknown_neighbours(neighbour_1, neighbour_2):
	check_house_features_unknown_neighbours_one_order(neighbour_1, neighbour_2)
	check_house_features_unknown_neighbours_one_order(neighbour_2, neighbour_1)



def set_last_remaining():
	for element_col in init_list:
		for house_family_key, house_family_elements in house_features.items():
			false_count = 0
			not_false_feature = None
			not_false_feature_state = None
			feature_state = None
			for element_row in house_family_elements:
				feature_state = df[element_col][element_row]
				if feature_state == False:
					false_count +=1
				else:
					not_false_feature = element_row
					not_false_feature_state = feature_state
			if false_count == 4 and pd.isna(not_false_feature_state):
				set_house_feature(element_col, not_false_feature, True)



for element in init_list:
	set_house_feature(element, element, True)

set_house_feature('English', 'red', True)
set_house_feature('Swedish', 'dog', True)
set_house_feature('Danish', 'tea', True)
#green on the left of white
set_house_feature(4, 'green', False)
set_house_feature(0, 'white', False)
set_house_feature('green', 'coffee', True)
set_house_feature('Pall Mall', 'bird', True)
set_house_feature(2, 'milk', True)
set_house_feature('yellow', 'Dunhill', True)
set_house_feature('Norwegian', 0, True)
##Marlboro and cat neighbours
set_house_feature('Marlboro', 'cat', False)
##Dunhill and horse neighbours
set_house_feature('Dunhill', 'horse', False)
set_house_feature('Winfield', 'beer', True)
##Norwegian and blue neighbours
set_house_feature('Norwegian', 'blue', False)
set_house_feature('German', 'Rothman', True)
#Marlboro and water neighbours
set_house_feature('Marlboro', 'water', False)

fish_owner = None
def find_fish_owenr():
	for owner in house_features['nationalities']:
		if df['fish'][owner] == True:
			print('The ', owner, ' has the fish')
			return owner
	return None
while not fish_owner:
	check_house_features_unknown_neighbours_one_order('Marlboro', 'cat')
	check_house_features_unknown_neighbours_one_order('Dunhill', 'horse')
	check_house_features_unknown_neighbours_one_order('Norwegian', 'blue')
	check_house_features_unknown_neighbours_one_order('Marlboro', 'water')
	set_last_remaining()
	fish_owner = find_fish_owenr()



df.to_excel('dataframe.xlsx', index = True, header=True)
