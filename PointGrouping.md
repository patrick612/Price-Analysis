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

Test Result of the Algorithm
We have used 600 minute points of BTC price data for the test. 
Step 1 of the process looks like the following. The time series data is segmented into price neighborhoods. The neighborhood size of 20% of price range was used. 5 different offsets were used. We see that Tthe largest consecutive points that occur is approximately 90 consecutive points which starts around 140th point. 

![Figure_1](https://user-images.githubusercontent.com/77427280/155604591-6994f730-d9f3-448f-b8a9-2cb927ace4db.png)

After running the algorithm up to step 4, we obtain a data set containing number of consecutive points that have occured for all iterations with different offsets. The distribution of length of consecutive data is given below. The y axis is the count of number of consecutive points and the x axis is the length of consecutive points. 

![Figure_2](https://user-images.githubusercontent.com/77427280/155614108-b8963e32-8e21-41d3-8dcc-d42f3655f4a9.png)
We see that 90 consecutive points is quite statistically significant. In fact, for 600 points of minute data, we have found the following results:<img width="571" alt="Screen Shot 2022-02-24 at 4 56 41 PM" src="https://user-images.githubusercontent.com/77427280/155614425-c65a2438-eef8-4ae5-bb52-738d52dad7ea.png">

Where Nb size is given as percent of max – min values of the time series. 
The method described above picks out the most statistically significant way to capturing the neighborhood of a group behavior. One thing to note however is that the average deviation from the mean of the standard deviation is very high. That is the longest occurring time series is at least 6 standard deviations away from the mean for the above cases. This is because we have used a minute data for 600 points. The minute data captures small oscillations and variance in time series and therefore when divided into neighborhoods, the short continuous time series are more likely to be captured. If we had used 120 points of 5 minute data, the standard deviations would be less. Regardless, the longest occurring segment would still have the highest relative standard deviation. Furthermore, as the size of the neighborhood grows, its statistical significance should decrease since although longer time series are captured, more statistically insignificant time series will be included in the data set. Also, as neighborhood gets smaller, we will capture more and more of small variance of the time series leading to statistically insignificant points. As we see from the following graph, we see that when we set the neighborhood size to around 20% we capture the boxed area:

<img width="846" alt="Screen Shot 2022-02-24 at 5 04 05 PM" src="https://user-images.githubusercontent.com/77427280/155615343-40333ba0-cb94-473f-af16-a5e170b35787.png">

