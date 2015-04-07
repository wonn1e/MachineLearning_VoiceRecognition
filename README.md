# MachineLearning_VoiceRecognition
Implemented voice recognizer with Forward Algorithm using python

.:: Introduction ::.
This is a word recognizer, specifically numbers. People have recorded their voice saying numbers from 0-9.
Those records have been transformed into MFCC file and this recognizer is implemented using forward algorithm.

.:: Specification of the files included ::.
The information needed to implement forward algorithm such as language model probability, in this project, unigram.txt;
how numbers are pronounciated in dictionary.txt; and the specification of each sound in hmm.txt.

There are two ways to say 0, which are 'oh' and 'zero'.
I have considered those two differently when finding the most probable word for each MFCC file.

tst directory is also included and whithin its lower level there are around 8000 MFCC files in txt format.
The name of each txt file indicates (id of the person recording)_(the number that person is reading).
For instance, 44z5938_029_063_4 shows that person is reading number 4.

.:: How to run the program ::.
You should be able to run the program with 'Forward1.py' and since it's implemented in Python and the data
in txt directory is enormous, it might take some time to finish running the whole program.
If you wish to see the result more quickly, you should remove some files from txt directory.

.:: Results of the program ::.
As you finish running the program, you should be able to see the result in confusion matrix in 'result.txt'.
The rows indicate original numbers and the columns indicate the prediction.
The index of the numbers are in the following order
  0(oh), 1, 2, 3, 4, 5, 6, 7, 8, 9, 0(zero)
  
To give you deeper understading of the result; let's say that you were testing only 44z5938_029_063_4.txt file and the prediction
has given you the right answer, which is 4. Then every cell in the confusion matrix is set in 0 except for the cell in column 5, row 5.

After testing all the files, the result has shown 84% of correct prediction rate.
