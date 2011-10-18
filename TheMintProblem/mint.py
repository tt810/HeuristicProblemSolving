import sys
import json

def arrayAdd(array1, array2):
  return [el+array2[i] for i, el in enumerate(array1)]
  
def exactChange(denomination):
  """
  exact change numbers for 1 to 99 are stored in array best
  best[i] = 1 + min{best[i-deno1], best[i-deno2], best[i-deno3], best[i-deno4], best[i-deno5]}
  """
  best = [[0,0,0,0,0] for i in range(100)]

  for i in range (1, 100):
    mini = [100,100,100,100,100]
    col = 0
    for j in range(0, 5):
      if denomination[j] > i:
        break
      if denomination[j] <= i and sum(mini) >= sum(best[i-denomination[j]]):
        mini = best[i-denomination[j]]
        col = j
    best[i][col] += 1
    best[i] = arrayAdd(best[i], mini)
  return best

def exchangeNumber(denomination, N):
  """
  exchange numbers for 1 to 99 are stored in array best, which is the min of following three:
  best[i] = min{exact[i], best[100-i], exact[j-i]+exact[j]},
  for
    exact[i] is the exact number of i,
    best[100-i] is the exchange number of 100-i,
    exact[j] is the exact number of j, for i < j <= 100.
  """
  exact = exactChange(denomination) + [[0, 0, 0, 0, 0]]    
  best = [[0,0,0,0,0] for i in range(100)]
  score = 0
  
  def absSum(array):
    return sum(abs(el) for el in array)
  
  for i in range(1, 100):
    mini = [100, 100, 100, 100, 100]
    for j in range(i+1, 101):
      if sum(exact[i]) == 1:
        mini = exact[i]
        break
      exchange = sum(exact[j]) + sum(exact[j-i])
      if exchange < absSum(mini) and exchange < sum(exact[i]):
        mini = arrayAdd(exact[j], [-1* el for el in exact[j-i]]) 
    opposite = absSum(best[100-i])
    abssummini = absSum(mini)
    if opposite != 0 and opposite < sum(exact[i]) and opposite < abssummini:
      best[i] = [-1*el for el in best[100-i]]
    elif sum(exact[i]) > abssummini:
      best[i] = mini
    else:
      best[i] = exact[i]
    abssum = absSum(best[i])
    if i % 5 == 0:
      score = score +  abssum* N
    else:
      score = score + abssum
  #score = score + absSum(best[50]) * N
  averScore = score / (N*19 + (99-19))
  return (score, averScore, best)

def mint(N):
  bound = sys.maxint
  best = [0, 0, 0, 0, 0]
  if N <= 20.0:
    for x2 in range(2, 7):
      for x3 in range(x2+1, 2*x2):
      #for x3 in range(2*x2, 13):    
        #for x4 in range(x3+1, 2*x3):
        for x4 in range(2*x3, 26):
          for x5 in range(x4+1, 2*x4):
          #for x5 in range(2*x4, 51):
            (score, averScore, exchange) = exchangeNumber([1, x2, x3, x4, x5], N)
            if score < bound:
              best = [1, x2, x3, x4, x5]
              bound = score
              #print best, " score: ", score
  else:
    for x2 in range(2, 7):
      #for x3 in range(x2+1, 2*x2):
      for x3 in range(2*x2, 13):    
        #for x4 in range(x3+1, 2*x3):
        for x4 in range(2*x3, 26):
          for x5 in range(x4+1, 2*x4):
          #for x5 in range(2*x4, 51):
            (score, averScore, exchange) = exchangeNumber([1, x2, x3, x4, x5], N)
            if score < bound:
              best = [1, x2, x3, x4, x5]
              bound = score
              #print best, " score: ", score
  return (best, score)
   
def jsonOutput(best, N):
  """exchange = exchangeNumber(best, N)
  print "Best denomination:", best, "with N=", N
  print "score: ", exchange[0], " average score: ", exchange[1]
  for i in range(1,100):
    print exchange[2][i]"""
  output = {}
  output['denomination'] = best
  exchange = exchangeNumber(best, N)
  output['exchanges'] = exchange[2][1:]
  output['score'] = exchange[0]
  output['average score'] = exchange[1]
  
  #with open('SToutput.json', 'wb') as f:
    #json.dump(output, f, indent = 2)
  print output 
       
if __name__ == "__main__":
  N = float(sys.argv[1])
  (best, score) = mint(N)
  jsonOutput(best, N)
  """
  (score, averScore, exchange) = exchangeNumber([1, 3, 8, 18, 40], 1.0)
  for i in range(1, 100):
    print i, exchange[i]
  print score
  """
  
