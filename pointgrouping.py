
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# sectionalize into neighbourhoods for opening values
#nb_perc is neighborhood range in percentile
# for empty placeholders occuring due to offsets or the highest sections, -1 is assigned
#0.01 is added to maximum value of the price list to include the last point
def sectionalize(df, nb_perc, offset = False):
    col_open = df["open"]
    max_val = col_open.max()
    min_val = col_open.min()
    increment = nb_perc / 100 * (max_val - min_val)
    offset = offset / 100 * (max_val - min_val)
    cat_list = []
    dividing_points = []
    if offset is False:
        for sections in np.arange(min_val, max_val + 0.1, increment):
            dividing_points.append(sections)
    else:
        for sections in np.arange(min_val + offset, max_val + 0.1, increment):
            dividing_points.append(sections)

    for price in np.arange(0, len(col_open), 1):
        i = 0
        while True:
            if dividing_points[i] <= col_open[price] < dividing_points[i + 1]:
                cat_list.append(i)
                break
            if i == len(dividing_points) -2:
                cat_list.append(-1)
                break
            else:  i = i + 1
    df['sections'] = cat_list

#now we count number of consecutive points occuring
#we don't count consecutively occuring -1
# if longestpoint_index is True, function returns [length of longest point, [start index, end index]]
def count_consecutive(df, longestpoint_index = False):
    count_list = []
    holder = 0
    if longestpoint_index is False:
        for i in np.arange(1, len(df['sections']), 1):
            if df['sections'][holder] == df['sections'][i]:
                pass
            elif df['sections'][holder] == -1:
                holder = i
            else:
                consecutive_length = i - holder
                count_list.append((consecutive_length))
                holder = i
        return count_list
    else:
        lp_index = [0, [0, 0]]
        for i in np.arange(1, len(df['sections']), 1):
            if df['sections'][holder] == df['sections'][i]:
                pass
            elif df['sections'][holder] == -1:
                holder = i
            else:
                consecutive_length = i - holder
                count_list.append((consecutive_length))
                if consecutive_length > lp_index[0]:
                    lp_index[0] = consecutive_length
                    lp_index[1][0] = holder
                    lp_index[1][1] = i -1
                holder = i
        return count_list, lp_index

#collect samples of consecutive points from different sectionalizations by giving offset
#insert df and list of offset values
#is longestpoint_index is True, it returns lp_index = [length of longest point, [start index, end index], nb size in percent, offest]
def sample_consecutive(df, nb_perc, offset_list, longestpoint_index = False):
    if longestpoint_index is False:
        sectionalize(df, nb_perc)
        sample_list = count_consecutive(df)
        for i in np.arange(0, len(offset_list), 1):
            sectionalize(df, nb_perc, offset = offset_list[i])
            offset_sample_list = count_consecutive(df)
            sample_list = sample_list + offset_sample_list
        return sample_list
    else:
        sectionalize(df, nb_perc)
        sample_list, lp_index = count_consecutive(df, longestpoint_index = True)
        lp_index.append(nb_perc)
        lp_index.append(0)
        for i in np.arange(0, len(offset_list), 1):
            sectionalize(df, nb_perc, offset=offset_list[i])
            offset_sample_list, lp_index_i = count_consecutive(df, longestpoint_index = True)
            sample_list = sample_list + offset_sample_list
            if lp_index_i[0] > lp_index[0]:
                lp_index_i.append(nb_perc)
                lp_index_i.append(offset_list[i])
                lp_index = lp_index_i
            else:
                pass
        return sample_list, lp_index

def barchart(sample_list, width):
    x_list = []
    y_list = []
    for i in np.arange(width, np.ceil((max(sample_list)-min(sample_list)) / width) * width, width):
        x_list.append(i)
    x_list.pop(0)
    for i in np.arange(0, len(x_list), 1):
        count = np.count_nonzero(np.array(sample_list) < x_list[i]) and np.count_nonzero(np.array(sample_list) >= x_list[i] - width)
        y_list.append(count)
    plt.bar(x_list, y_list)
    plt.show()

# insert [neighborhood range, offset] for horizontal_line
def scatter_plot1(df, nb_perc, offset):
    col_open = df["open"]
    max_val = col_open.max()
    min_val = col_open.min()
    increment = nb_perc / 100 * (max_val - min_val)
    offset = offset / 100 * (max_val - min_val)
    dividing_points = []
    for sections in np.arange(min_val + offset, max_val + 0.1, increment):
        dividing_points.append(sections)
    x = np.arange(0, len(df_1m['open']), 1)
    y = np.array(df_1m['open'])
    plt.scatter(x, y, vmin=min(col_open))
    for i in np.arange(0, len(dividing_points), ):
        plt.axhline(y = dividing_points[i], color = 'r', linestyle = 'dashed')
    plt.show

#This scatter plot takes in df and lp_index and returns a plot with longest consecutive part highlighted
def scatter_plot(df, lp_index):
    nb_perc = lp_index[2]
    offset = lp_index[3]
    longestpoint_index = lp_index[1]
    col_open = df["open"]
    max_val = col_open.max()
    min_val = col_open.min()
    increment = nb_perc / 100 * (max_val - min_val)
    offset = offset / 100 * (max_val - min_val)
    dividing_points = []
    for sections in np.arange(min_val + offset, max_val + 0.1, increment):
        dividing_points.append(sections)
    x = np.arange(0, len(df_1m['open']), 1)
    y = np.array(df_1m['open'])
    plt.scatter(x[:longestpoint_index[0]], y[:longestpoint_index[0]], vmin=min(col_open), color = 'b')
    plt.scatter(x[longestpoint_index[0]: longestpoint_index[1]], y[longestpoint_index[0]: longestpoint_index[1]], vmin=min(col_open), color='hotpink')
    plt.scatter(x[longestpoint_index[1]:], y[longestpoint_index[1]:], vmin=min(col_open), color='b')
    for i in np.arange(0, len(dividing_points), ):
        plt.axhline(y = dividing_points[i], color = 'r', linestyle = 'dashed')
    plt.show
    
def find_stat(sample_list):
    print("mean is " + str(np.mean(sample_list)))
    print("STD is " + str(np.std(sample_list)))
    print("max is " + str(max(sample_list)))
    print("# of STD from mean is " + str((max(sample_list) -  np.mean(sample_list))/np.std(sample_list)))

