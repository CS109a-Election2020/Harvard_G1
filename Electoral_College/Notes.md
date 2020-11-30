Notes on states: 
For the following states, we have absolutely no data from 5.38 and I could not find them elsewhere: 
Alaska 2012 
Delaware 2012 
Idaho 1988  
Mississippi 2012 
Wyoming 2004 
Wyoming 2012 
How to handle such situation ? Train with less data? We could try out.
To fix: 3 NaN in the House of Representative votes
Question: Do we want to perform a classification task ? Ie vote = Rep or Dem, or do we want to perform 
a Regression task when obtaining the repartition of votes for every state ? 
Left to check: the House of Reps vote, renew the construction of the frames + how we computed the scores.
We changed the House of Reps vote, everything is okay except for the 2018 election, which is going to be manually fixed.
Fix the polls for Alabama, to be pulled from github
We checked the lengths of the dfs, being coherent with the polls
Now, going to manually fix the results from the 2018 election: done