def char():
    count=len(sen)
    print("Number of characters in the sentence:",count)

def word():
    count=1
    for i in sen:
        if i==' ':
            count+=1
    print("Number of words in the sentence:",count)

def vowel():
    count=0
    for i in sen:
        if i.lower()in 'aeiou':
            count+=1
    print("Number of vowels in the sentence:",count)
    
    
sen=str(input("Enter a sentence: "))
char()
word()
vowel()