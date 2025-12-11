def odd(list1):
    count_odd=0
    for i in list1:
        if int(i)%2!=0:
            count_odd+=1
    print("Number of odd numbers in the list:",count_odd)

def even(list1):
    count_even=0
    for i in list1:
        if int(i)%2==0:
            count_even+=1
    print("Number of even numbers in the list:",count_even)
    
list1=[]
user_input = input("Enter numbers separated by commas ")
list1 = user_input.split(',')
for x in list1:
 list1 = [x.strip()] 
    
odd(list1)
even(list1)
print("The list is:",list1)