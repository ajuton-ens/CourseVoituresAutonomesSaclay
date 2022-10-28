import numpy as np
import matplotlib.pyplot as plt
def ransac_polyfit(x, y, order=3, n=20, k=100, t=0.1, d=100, f=0.8):
  # Thanks https://en.wikipedia.org/wiki/Random_sample_consensus
  
  # n – minimum number of data points required to fit the model
  # k – maximum number of iterations allowed in the algorithm
  # t – threshold value to determine when a data point fits a model
  # d – number of close data points required to assert that a model fits well to data
  # f – fraction of close data points required
  
  besterr = np.inf
  bestfit = None
  for _ in range(k):
    maybeinliers = np.random.randint(len(x), size=n)
    maybemodel = np.polyfit(x[maybeinliers], y[maybeinliers], order)
    alsoinliers = np.abs(np.polyval(maybemodel, x)-y) < t
    if sum(alsoinliers) > d and sum(alsoinliers) > len(x)*f:
      bettermodel = np.polyfit(x[alsoinliers], y[alsoinliers], order)
      thiserr = np.sum(np.abs(np.polyval(bettermodel, x[alsoinliers])-y[alsoinliers]))
      if thiserr < besterr:
        bestfit = bettermodel
        besterr = thiserr
  return bestfit,thiserr

def double_ransac_polyfit(x, y, order=1, n1=2, n2=2, k1=100, k2=10, t=0.1, d1=100, d2=100 ):
  # Thanks https://en.wikipedia.org/wiki/Random_sample_consensus
  
  # n – minimum number of data points required to fit the model
  # k – maximum number of iterations allowed in the algorithm
  # t – threshold value to determine when a data point fits a model
  # d – number of close data points required to assert that a model fits well to data
  # f – fraction of close data points required
  
  besterr = np.inf
  bestfit1 = np.array([None])
  bestfit2 = np.array([None])
  bestfit3 = np.array([None])

  bestinliners1 = np.array([None])
  bestinliners2 = np.array([None])
  bestinliners3 = np.array([None])

  for _ in range(k1):
    maybeinliers = np.random.randint(len(x), size=n1)
    maybemodel1 = np.polyfit(x[maybeinliers], y[maybeinliers], order)
    m1=maybemodel1[0]
    b1=maybemodel1[1]
    alsoinliers1 = np.abs(m1*x-y+b1)/np.sqrt(m1**2+1) < t
    if sum(alsoinliers1) > d1:
      bettermodel1 = np.polyfit(x[alsoinliers1], y[alsoinliers1], order)
      m1=bettermodel1[0]
      b1=bettermodel1[1]
      outliner1 = np.abs(m1*x-y+b1)/((m1**2+1)**(1/2)) >= t
      vec_err1 = np.abs(m1*x-y+b1)/((m1**2+1)**(1/2))/len(x)
      err1 = np.sum(vec_err1)
      if sum(outliner1)>n2:
        maybeinliers2 = np.random.randint(len(x[outliner1]), size=n2)
        maybemodel2 = np.polyfit(x[outliner1][maybeinliers2], y[outliner1][maybeinliers2], order)
        m2=maybemodel2[0]
        b2=maybemodel2[1]
        alsoinliers2 = np.abs(m2*x[outliner1]-y[outliner1]+b2)/np.sqrt(m2**2+1) < t
        if sum(alsoinliers2)>d2:
          bettermodel2 = np.polyfit(x[outliner1][alsoinliers2], y[outliner1][alsoinliers2], order)
          m2=bettermodel2[0]
          b2=bettermodel2[1]
          vec_err2 = np.abs(m2*x-y+b2)/np.sqrt(m2**2+1)/len(x)
          vec_err12 = np.minimum(vec_err1,vec_err2)
          err12=np.sum(vec_err12)
          outliner2= np.abs(m2*x[outliner1]-y[outliner1]+b2)/np.sqrt(m2**2+1) > t
          if sum(outliner2)>n2:
            maybeinliers3 = np.random.randint(len(x[outliner1][outliner2]), size=n2)
            maybemodel3 = np.polyfit(x[outliner1][outliner2][maybeinliers3], y[outliner1][outliner2][maybeinliers3], order)
            m3=maybemodel3[0]
            b3=maybemodel3[1]
            alsoinliers3 = np.abs(m3*x[outliner1][outliner2]-y[outliner1][outliner2]+b3)/np.sqrt(m3**2+1) < t
            if sum(alsoinliers3)>d2:
              bettermodel3 = np.polyfit(x[outliner1][outliner2][alsoinliers3], y[outliner1][outliner2][alsoinliers3], order)
              m3=bettermodel3[0]
              b3=bettermodel3[1]
              vec_err3 = np.abs(m3*x-y+b3)/np.sqrt(m3**2+1)/len(x)
              vec_err123 = np.minimum(vec_err12,vec_err3)
              err123=np.sum(vec_err123)
              if 1.25*err123 < besterr:
                bestfit1=bettermodel1
                bestfit2=bettermodel2
                bestfit3=bettermodel3
                bestinliners1 = alsoinliers1
                bestinliners2 = alsoinliers2
                bestinliners3 = alsoinliers3
                besterr=1.5*err123
            elif 1.25*err12<besterr:
              bestfit1=bettermodel1
              bestfit2=bettermodel2
              bestfit3=np.array([None])
              bestinliners1 = alsoinliers1
              bestinliners2 = alsoinliers2
              bestinliners3 = np.array([None])
              besterr=1.25*err12
          elif 1.25*err12<besterr:
              bestfit1=bettermodel1
              bestfit2=bettermodel2
              bestfit3=np.array([None])
              bestinliners1 = alsoinliers1
              bestinliners2 = alsoinliers2
              bestinliners3 = np.array([None])
              besterr=1.25*err12
        elif err1<besterr:
          bestfit1=bettermodel1
          bestfit2=np.array([None])
          bestfit3=np.array([None])
          bestinliners1 = alsoinliers1
          bestinliners2 = np.array([None])
          bestinliners3 = np.array([None])
          besterr=err1
      elif err1<besterr:
          bestfit1=bettermodel1
          bestfit2=np.array([None])
          bestfit3=np.array([None])
          bestinliners1 = alsoinliers1
          bestinliners2 = np.array([None])
          bestinliners3 = np.array([None])
          besterr=err1
  """print("bestfit 1 : " , bestfit1, type(bestfit1))
  print("bestfit 2 : " , bestfit2, type(bestfit2))
  print("bestfit 3 : " , bestfit3, type(bestfit3))"""
  if (bestfit1.all()!=None and bestfit2.all()!=None and bestfit3.all()!=None):
    bestfit=np.array([bestfit1,bestfit2,bestfit3])
    bestinliners=np.array([bestinliners1,bestinliners2,bestinliners3])
  elif (bestfit1.all()!=None and bestfit2.all()!=None):
    bestfit=np.array([bestfit1,bestfit2])
    bestinliners=np.array([bestinliners1,bestinliners2])
  else:
    bestfit=np.array([bestfit1])
    bestinliners=np.array([bestinliners1])
  return bestfit,bestinliners,besterr

"""
def triple_ransac_polyfit(x, y, order=1, n1=2, n2=2, k1=100, k2=10, t=0.1, d1=100, d2=100 ):
  # Thanks https://en.wikipedia.org/wiki/Random_sample_consensus
  
  # n – minimum number of data points required to fit the model
  # k – maximum number of iterations allowed in the algorithm
  # t – threshold value to determine when a data point fits a model
  # d – number of close data points required to assert that a model fits well to data
  # f – fraction of close data points required
  
  besterr1 = np.inf
  besterr2 = np.inf
  besterr3 = np.inf
  bestfit1 = np.array([None])
  bestfit2 = np.array([None])
  bestfit3 = np.array([None])
  for _ in range(k1):
    maybeinliers = np.random.randint(len(x), size=n1)
    maybemodel1 = np.polyfit(x[maybeinliers], y[maybeinliers], order)
    m1=maybemodel1[0]
    b1=maybemodel1[1]
    alsoinliers1 = np.abs(m1*x-y+b1)/np.sqrt(m1**2+1) < t
    if sum(alsoinliers1) > d1:
      bettermodel1 = np.polyfit(x[alsoinliers1], y[alsoinliers1], order)
      m1=bettermodel1[0]
      b1=bettermodel1[1]
      outliner1 = np.abs(m1*x-y+b1)/np.sqrt(m1**2+1) >= t
      vec_err1 = outliner
      err1 = np.sum(vec_err1)
      if err1 < besterr1:
                bestfit1=bettermodel1
                besterr1=err1
  m1=bestfit1[0]
  b1=bestfit1[1]
  outliner1 = np.abs(m1*x-y+b1)/np.sqrt(m1**2+1) >= t
  for _ in range(k1):
    if sum(outliner1)>n2:
      maybeinliers2 = np.random.randint(len(x[outliner1]), size=n2)
      maybemodel2 = np.polyfit(x[outliner1][maybeinliers2], y[outliner1][maybeinliers2], order)
      m2=maybemodel2[0]
      b2=maybemodel2[1]
      alsoinliers2 = np.abs(m2*x[outliner1]-y[outliner1]+b2)/np.sqrt(m2**2+1) < t
      if sum(alsoinliers2)>d2:
        bettermodel2 = np.polyfit(x[outliner1][alsoinliers2], y[outliner1][alsoinliers2], order)
        m2=bettermodel2[0]
        b2=bettermodel2[1]
        outliner2= np.abs(m2*x[outliner1]-y[outliner1]+b2)/np.sqrt(m2**2+1) > t
        vec_err2 = np.abs(m2*x-y+b2)/np.sqrt(m2**2+1)/len(x)
        vec_err12 = np.minimum(vec_err1,vec_err2)
        err12=np.sum(vec_err12)
        if err1 < besterr1:
          bestfit1=bettermodel1
          besterr1=err1
  m2=bestfit2[0]
  b2=bestfit2[1]
  outliner2= np.abs(m2*x[outliner1]-y[outliner1]+b2)/np.sqrt(m2**2+1) > t
  for _ in range(k1)
    if sum(outliner2)>n2:
      maybeinliers3 = np.random.randint(len(x[outliner1][outliner2]), size=n2)
      maybemodel3 = np.polyfit(x[outliner1][outliner2][maybeinliers3], y[outliner1][outliner2][maybeinliers3], order)
      m3=maybemodel3[0]
      b3=maybemodel3[1]
      alsoinliers3 = np.abs(m3*x[outliner1][outliner2]-y[outliner1][outliner2]+b3)/np.sqrt(m3**2+1) < t
      if sum(alsoinliers3)>d2:
        bettermodel3 = np.polyfit(x[outliner1][outliner2][alsoinliers3], y[outliner1][outliner2][alsoinliers3], order)
        m3=bettermodel3[0]
        b3=bettermodel3[1]
        vec_err3 = np.abs(m3*x-y+b3)/np.sqrt(m3**2+1)/len(x)
        vec_err123 = np.minimum(vec_err12,vec_err3)
        err123=np.sum(vec_err123)
              if err123 < besterr:
                bestfit1=bettermodel1
                bestfit2=bettermodel2
                bestfit3=bettermodel3
                besterr=err123
            elif err12<besterr:
              bestfit1=bettermodel1
              bestfit2=bettermodel2
              bestfit3=np.array([None])
              besterr=err12
          elif err12<besterr:
              bestfit1=bettermodel1
              bestfit2=bettermodel2
              bestfit3=np.array([None])
              besterr=err12
        elif err1<besterr:
          bestfit1=bettermodel1
          bestfit2=np.array([None])
          bestfit3=np.array([None])
          besterr=err1
      elif err1<besterr:
          bestfit1=bettermodel1
          bestfit2=np.array([None])
          bestfit3=np.array([None])
          besterr=err1
  print("bestfit 1 : " , bestfit1, type(bestfit1))
  print("bestfit 2 : ",bestfit2, type(bestfit2))
  print("bestfit 3 : ",bestfit3, type(bestfit3))
  if (bestfit1.all()!=None and bestfit1.all()!=None and bestfit3.all()!=None):
    bestfit=np.array([bestfit1,bestfit2,bestfit3])
  elif (bestfit1.all()!=None and bestfit2.all()!=None):
    bestfit=np.array([bestfit1,bestfit2])
  else:
    bestfit=np.array([bestfit1])
  return bestfit,besterr
"""