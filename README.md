# Data-Structures-Project-Youtube-Insights-
A youtube insights engine that provides fast analytics on a user's behaviour. 

Project Title: YouTube Search Data Insights
Group Members: David Deng, Josh Zhou, John Long
GitHub Repo Link: https://github.com/ddeng26-spec/Data-Structures-Project-Youtube-Insights-

Abstract
Problem Statement: Users on YoutTube have limited access to the insights and data from their search and watch history. Users often accumulate large, unorganized YouTube search histories that reveal patterns in their interests over time. They can access what videos they’ve watched by going through their history, but have no information regarding the topical frequency of their content, key search words, or what their YouTube behavior looks like in practice. Given that the average person from Generation Z spends between 1 hour and 1 hour 30 minutes on YouTube per day, they are unable to access information for a large part of their life. 

Solution: We propose building a YouTube Search History Insight Engine that ingests a user’s exported search-history.json from Google Takeout and provides fast analytics such as:
frequency of search terms,
most active search days/times
burst detection (topics searched repeatedly in short windows)
autocomplete suggestions
topic-based trend exploration over time

Application to Data Structures: We will utilize both hash tables and binary search trees for our final project. The goal of the project is to gain insights from users’ YouTube searches. The hash tables will be used to track the frequency of words searched by the user. Each word will be a key in a key-value pair where the value is the frequency of search. Each search will update the existing values or add new key-value pairs if certain words were not previously present. The Binary Search Trees will be used to order the search word frequency data in order according to individual frequency. This will give us a sorted data set that we can easily analyze for patterns or tendencies. These two data structures will allow us to store and organize our data easily, so we can gain insights from it.
