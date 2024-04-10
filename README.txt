File execution instructions for the Bayes classifier.

1.) First we need to build our vocabulary with the most common words. For this to happen we open the data.py file.
2.) You have to pass the inputs in the file because when we asked for them during the execution of the program, incomprehensible errors occurred.
    i) In the __init__ function give mostCommonWordsToKeep a number for the most common words we want to keep. (There is a relevant comment next to the command).
    ii) In the __init__ function give mostCommonWordsToDiscard a number that will indicate how many of the first most common words we have already selected in (i) we will discard according to the pronunciation (There is a relevant comment next to the command).
    Sub-queries (i) and (ii) have some default values which you can not change if you don't want to.
    iii) In the link function, give the url the path where the folder with the data from Imdb is located exactly as it is in the predefined value of the url. Pay attention that for it to work you must put a double slash (\\) after each folder. This step is mandatory to run the file on your computer.


Note1: Each py file takes 3-4 minutes to run.
Note2: If an error occurs when running Bayes.py from cmd, run it from idle.
