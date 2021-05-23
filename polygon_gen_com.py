'''
currently this program works well while generating around 50-70 polygons and each polygon can have vertices from 10-500.
But as the number of vertices in polygons increase it becomes more star like.

The final wkt file generated can be plotted with the help of qgis software (open-source)
'''
from random import sample,choice
from numpy import arctan2,random,sin,cos,degrees
import math
import os
import matplotlib.pyplot as plt
grid = {"x":[],"y":[]}
f = open("demo.csv","w")
f.write("\"POLYGON SHAPES\"\n")


'''
The number of polygons can be more than 20 also , but for testing purpose I have set it as 4 - 20
'''

n = int(input("Enter the number of polygons to generate: "))
def generate_random_polygons(n):
    for i in range(n):
        '''
        The number of vertices can be from 10 - 500 but for testing purpose , It has been set from 10 - 50
        '''
        number_of_vertices = random.randint(10,50)        #number of vertices in each polygon can be from 10-500
        if(i == 0):
            x_boundary,y_boundary = 1,500
        else:
            x_boundary = x_boundary+200                   #shifting the x and y axis so that they do not plot over each other.
            y_boundary = y_boundary + 210                 
        get_polygons(number_of_vertices,x_boundary,y_boundary,i)


#function to get center of mass
def get_com(grid):
    center = [sum(grid["x"])/len(grid["x"]) , sum(grid["y"])/len(grid["y"])]
    return center

#funtion to get distance and polar angle
def get_sqr_polar(point,com):
    return [math.atan2(point[1] - com[1] , point[0]-com[0]) , (point[0]-com[0])**2 + (point[1] - com[1])**2]


def get_polygons(n,x_boundary,y_boundary,i):
    x = []
    y = []
    x_hieght = 1
    y_height = 600
    if(i%2 == 0):
       x_hieght = x_hieght+100      #Just trying to shift the coordinates up and down , so that it can spread more evenly and not clutter at one place.
       y_height = y_height+140
    if(i%3 == 0):
        x_hieght = x_hieght-140
        y_height = y_height-210
    x,y = sample(range(x_boundary,y_boundary),n),sample(range(x_hieght,y_height),n)
    grid["x"] = x
    grid["y"] = y
    # print(grid)
    com = get_com(grid)

    final_l = []
    for i in range(len(grid["x"])):
        point = [grid["x"][i],grid["y"][i]]
        pd = get_sqr_polar(point,com)
        final_l.append(pd)
    '''
    The zipping and the sorting below is just used to sort the final_l (list) in decreasing order of the squared polar distance.
    '''
    zipped_x = zip(final_l,x)
    sorted_x =  sorted(zipped_x)
    sorted_list1 = [element for _, element in sorted_x]
    sorted_list1 = sorted_list1[::-1]
    zipped_y = zip(final_l,y)
    sorted_y =  sorted(zipped_y)
    sorted_list2 = [element for _, element in sorted_y]
    sorted_list2 = sorted_list2[::-1]

    #function to write the generated points in the wkt file
    write_to_file(sorted_list1,sorted_list2)
  

print("generating...")
#function to store the points in wkt file format (later to change it as .csv file)
def write_to_file(sorted_list1,sorted_list2):
    f.write("\"POLYGON ((")
    for i in range(len(sorted_list1)):
        f.write(str(sorted_list1[i])+" "+str(sorted_list2[i])+",")
    f.write(str(sorted_list1[0])+" "+str(sorted_list2[0])+"))\"\n")
generate_random_polygons(n)
f.close()

from shapely.ops import unary_union
import shapely.wkt
import pandas as pd
df = pd.read_csv("demo.csv")
df['POLYGON SHAPES'] = df['POLYGON SHAPES'].apply(lambda x: shapely.wkt.loads(x))
union_poly = unary_union(df.loc[:,'POLYGON SHAPES'])

file = open("de.csv", "w")
poly_df = pd.DataFrame(data = {'com_poly': union_poly}, index=[0])
poly_df.to_csv(file, index=False, header=["MERGED POLYGON"])
file.close()
