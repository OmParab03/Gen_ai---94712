import math
def cal_area_of_circle(radius):
    area=math.pi*(radius**2 )
    print(f"Area of circle with radius = {radius} is:{area}" )
    
def cal_area_of_square(side):
    area=side**2
    print(f"Area of square with side = {side} is:{area}" )
    
def cal_area_of_rectangle(l, b):
    area=l*b
    print(f"Area of rectangle with length = {l} and breadth = {b} is:{area}" )

def cal_area_of_triangle(base, height):
    area=0.5*base*height
    print(f"Area of triangle with base = {base} and height = {height} is:{area}" )    

cal_area_of_circle(5)
cal_area_of_square(4)   
cal_area_of_rectangle(4, 6)
cal_area_of_triangle(4, 7)    