class univariate():
    
    def QuanQual(dataset):
        quan=[]
        qual=[]
        for columnName in dataset.columns:
           #print(columnName)
            if(dataset[columnName].dtype=='O'):
               # print("qual")
               qual.append(columnName) 
            else:
               # print("quan")
               quan.append(columnName)
        return quan,qual
    
   

    def freqTable(columnName,dataset):
        freqTable=pd.DataFrame(columns=["unique_values","frequency","relative_frequency","cumsum"])
        freqTable["unique_values"]=dataset[columnName].value_counts().index
        freqTable["frequency"]=dataset[columnName].value_counts().values
        freqTable["relative_frequency"]=(freqTable["frequency"]/103)
        freqTable["cumsum"]=freqTable["relative_frequency"].cumsum()
    return freqTable 

   def Univariate_concepts(quan,dataset):
    descriptive=pd.DataFrame(index=["mean","median","mode","q1:25%","q2:50%","q3:75%","99%","q4:100%","IQR","1.5rule","Lesser",
                                "Greater","min","max"],columns=quan)
        for columnName in quan:
            descriptive[columnName]["mean"]=dataset[columnName].mean()
            descriptive[columnName]["median"]=dataset[columnName].median()
            descriptive[columnName]["mode"]=dataset[columnName].mode()[0]
            descriptive[columnName]["q1:25%"]=dataset.describe()[columnName]["25%"]
            descriptive[columnName]["q2:50%"]=dataset.describe()[columnName]["50%"]
            descriptive[columnName]["q3:75%"]=dataset.describe()[columnName]["75%"]
            descriptive[columnName]["99%"]=np.percentile(dataset[columnName],99)
            descriptive[columnName]["q4:100%"]=dataset.describe()[columnName]["max"]
            descriptive[columnName]["IQR"]=descriptive[columnName]["q3:75%"]-descriptive[columnName]["q1:25%"]
            descriptive[columnName]["1.5rule"]=1.5*descriptive[columnName]["IQR"] 
            descriptive[columnName]["Lesser"]=descriptive[columnName]["q1:25%"]- descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Greater"]=descriptive[columnName]["q3:75%"]+ descriptive[columnName]["1.5rule"]
            descriptive[columnName]["min"]=dataset[columnName].min()
            descriptive[columnName]["max"]=dataset[columnName].max()
        return descriptive
   
   def FindOutlier(dataset):
        Lesser=[]
        Greater=[]

        for columnName in quan:
             if(descriptive[columnName]["min"]<descriptive[columnName]["Lesser"]):
            Lesser.append(columnName)
       
            if(descriptive[columnName]["max"]>descriptive[columnName]["Greater"]):
            Greater.append(columnName)
        return Lesser,Greater
    
    def ReplaceOutlier():
        for columnName in Lesser:
            dataset[columnName][dataset[columnName]<descriptive[columnName]["Lesser"]]=descriptive[columnName]["Lesser"]
        for columnName in Greater:
            dataset[columnName][dataset[columnName]>descriptive[columnName]["Greater"]]=descriptive[columnName]["Greater"]
        return Lesser,Greater
    def PDF(dataset,startrange,endrange):
        from matplotlib import pyplot # library import
        from scipy.stats import norm# library import
        import seaborn as sns# library import
        ax= sns.distplot(dataset,kde=True,kde_kws={'color':'blue'},color='green')#ploting the data and giving colour for identifying
        pyplot.axvline(startrange,color='red') #axv-vertical line
        pyplot.axvline(endrange,color='red')
        #sample
        sample= dataset
        #calculate mean and standard deviation
        sample_mean=sample.mean()
        sample_std=sample.std()
        print('mean=%.3f,std= %.3f' % (sample_mean,sample_std))
        dist=norm(sample_mean,sample_std)
    
        #sample probabilities for range
        values=[value for value in range(startrange,endrange)]#assigning in oneliner forloop
        probabilities=[dist.pdf(value)for value in values]
        prob=sum(probabilities)
        print("range({},{}):{}".format(startrange,endrange,sum(probabilities)))
    return PDF

    def STDN(dataset):
        import seaborn as sns#import library
        mean=dataset.mean()#calculating mean and std
        std=dataset.std()
        values = [i for i in dataset]#giving in list
        z_score=[((j-mean)/std) for j in values] #formula Z-score
        sns.distplot(z_score,kde=True)#plotting the STDN
        #sum(z_score)/len(z_score)
    return STDN