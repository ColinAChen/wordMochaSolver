# wordMochaSolver

Colin Chen
colin.a.chen@gmail.com  

2018




Finds words given six letters from a screenshot of the game. Made to beat the game WordMocha
Uses opencv for image processing and os to acceessing other directories
I used snipping tool to extract the individual letters for template matching. I couldn't find J, Q,  and X.
Game Screenshots were all found online.
Template matching help from https://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
Uses spellchecker to find English words

Spellchecker returns some weird results for "English words" but it is much easier to pick out english words from a small list of results
than it is to determine them from the thousands of possible combinations of letters

Currently only works from three to seven letter combinations. Also doesn't properly add duplicate letters if they appear more than once. 
I'm working on removing these restriction.








