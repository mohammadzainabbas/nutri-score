#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import numpy as np

import math

from sklearn.metrics import accuracy_score

class MRsort():
    def __init__(self, lmda):
        self.lmda = lmda
        self.profiles = {
            'A': [[-1000, -2.5, -0.6, -0.35, 10, 3.5, 20], [0, 0, 0, 0, 21, 9, 60]],
            'B': [[-1860, -4, -1, -0.7, 6, 1.8, 8], [-1000, -2.5, -0.6, -0.35, 10, 3.5, 20]],
            'C': [[-2000, -6, -1.35, -0.9, 3, 0.6, 5], [-1860, -4, -1, -0.7, 6, 1.8, 8]],
            'D': [[-2400, -15, -1.82, -1.3, 1, 0.4, 1], [-2000, -6, -1.35, -0.9, 3, 0.6, 5]],
            'E': [[-3000, -100, -5, -2, 0, 0, 0], [-2400, -15, -1.82, -1.3, 1, 0.4, 1]]
        }            
        
        self.weights = np.array((2,2,2,2,1,1,1))
        self.criterias_num = 7
        
    def setProfile(self, profiles_arg):
        self.profiles = profiles_arg
    
    def setWeights(self, weights_arg):
        self.weights = weights_arg
        
    def compareCriterias(self, item_arg, key_arg):                
        return np.array(item_arg)>=np.array(self.profiles[key_arg][0])
    
    def compareCriteriasOpp(self, item_arg, key_arg):                
        return np.array(item_arg)<=np.array(self.profiles[key_arg][0])
    
    def getScore(self, mask_arg):
        sum_arg = 0
        for i in range(len(self.weights)):
            sum_arg += mask_arg[i] * self.weights[i]
        return sum_arg
    
    def getNScore(self, score_arg):
        return score_arg >= sum(self.weights)*self.lmda
        
    def pessimisticSort(self, item_criterias):
        scores_arg = []
        
        for i in item_criterias.index:
            for key in self.profiles.keys():
                mask = self.compareCriterias(item_criterias.loc[i, 'en':'fr'], key)
                if(self.getNScore(self.getScore(mask))):
                    scores_arg.append([item_criterias.loc[i, 'id'], key])
                    break
        
        return scores_arg
    
    def optm_end_scoring(self, scoring_arg):
        
        for i in range(len(scoring_arg)-1):
            if(scoring_arg[i][1] == 2):
                return scoring_arg[i+1][0]
            if(scoring_arg[i][1] == 3):
                return scoring_arg[i][0]
                              
    
    def optimisticSort(self, item_criterias):
        scores_arg = []
        scores_ret = []
        for i in item_criterias.index:
            for key in self.profiles.keys():
                m = 0x00
                mask_1_item = self.compareCriterias(item_criterias.loc[i, 'en':'fr'], key)
                mask_2_profile = self.compareCriteriasOpp(item_criterias.loc[i, 'en':'fr'], key)
                score_1_item = self.getNScore(self.getScore(mask_1_item))
                score_2_profile = self.getNScore(self.getScore(mask_2_profile))
                m = m | (score_2_profile << 1)
                m = m | score_1_item
                scores_arg.append([key, m])
            scores_ret.append([item_criterias.loc[i, 'id'], self.optm_end_scoring(scores_arg)])
                
        return scores_ret 
    
class Read_Data():
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.cols = ['id', 'name', 'category', 'en', 'su', 'fa', 'sa', 'pr', 'fi', 'fr', 'grade']
        self.init_cols = ['id', 'name', 'categories', 'energy', 'sugars' ,'saturated-fat','salt', 'proteins',
        'fiber','fruits-vegetables-nuts-estimate-from-ingredients_100g','grade']
    
    def getCols(self):
        self.data = self.data.loc[:, self.init_cols].copy()
        self.data.columns = self.cols
    
    def setNans(self):
        self.data.dropna(inplace=True)
    
    def setNegValues(self):
        self.data.en = self.data.en * -1
        self.data.su = self.data.su * -1
        self.data.fa = self.data.fa * -1
        self.data.sa = self.data.sa * -1
    
    def getData(self):
        self.getCols()
        self.setNans()
        self.setNegValues()
        
        return self.data

    
# pass the data directory to Read_Data class
rd = Read_Data("products_1000.csv")

# call the getData() to return dataframe
df = rd.getData()

# call the MRsort class with lambda 0.5
class_sort = MRsort(0.5)

# get a new scores for data using pessimistic sort
y_pess_sort = pd.DataFrame(class_sort.pessimisticSort(df), columns=['id', 'y_pred_ps'])


# get a new scores for data using optimistic sort
y_opt_sort = pd.DataFrame(class_sort.optimisticSort(df), columns=['id', 'y_opt_ps'])

# get original scores from data
y_true = df.grade.apply(lambda x: x.upper())

y_pess_sort.to_csv('scores_PS.csv', index=False)
y_opt_sort.to_csv('scores_OP.csv', index = False)

print("Accuracy of Pessimistic Sort:", np.round(accuracy_score(y_true, y_pess_sort.y_pred_ps), 3))
print("Accuracy of Optimistic Sort:", np.round(accuracy_score(y_true, y_opt_sort.y_opt_ps), 3))
        


# In[ ]:




