def quicksort(array):
	if len(array)<=1:
		return array
	pivot = array.pop(0)
	less = filter (lambda x:x<=pivot,array)
	greater = filter(lambda x:x>pivot,array)
	return quicksort(less)+[pivot]+quicksort(greater)


#main function
if __name__=='__main__':
	print quicksort([4,7,5,1,3,2])