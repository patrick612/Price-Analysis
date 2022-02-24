# Point Grouping
Point Grouping

In order to group consecutive points that exhibit group behavior, we use neighborhood to describe consecutively occurring points and select statistically significant neighborhoods. Specifically, the method goes as follows:
1. Divide up the time series into neighborhoods of same size. 
2. Count the length of all consecutively occurring neighborhoods
3. Do the same for the same neighborhood size with different offsets; translate the starting point of the first neighborhood.
4. Collect all the samples of lengths occurring from different offsets for a neighborhood size
5. Pick out longest occurring neighborhood and calculate its number of standard deviation from the mean of the sample
6. Repeat above steps for different neighborhood sizes and select the one which gives the one with largest number of standard deviation from the mean
7. Remove the consecutive points when described by certain neighborhood size and offset gives the largest number of standard deviation from the mean, then redo the above steps. This will pick out the next most significant consecutive points. We repeat this process for points that have number of standard deviation from the mean above a certain threshold value we set. 
![Figure_1](https://user-images.githubusercontent.com/77427280/155604591-6994f730-d9f3-448f-b8a9-2cb927ace4db.png)
