# Simplex implementation

################################################################################

def selectPivotColumn(botRow):
  # finds the column with largest(magnitude) negative number
  pivot_e = 0
  for i in range(len(botRow)-2): # exclude Z and solution column
    if botRow[i] < pivot_e:
      pivot_e = botRow[i]
      pivot_i = i

  if pivot_e < 0: return pivot_i
  else: return

################################################################################

def selectPivotRow(pivotColumn,solnColumn):
  # finds the row in pivot column that has a positive value and the 
  #   smallest positive test ratio
  for i in range(len(pivotColumn)-1): # exclude Z row
    if(pivotColumn[i] <= 0): continue
    tr = int(solnColumn[i]//pivotColumn[i])
    if tr >= 0:
      try:
        if tr < pivot_e:
          pivot_e = tr
          pivot_i = i
      except Exception:
        pivot_e = tr
        pivot_i = i
  
  try:
    return pivot_i
  except Exception:
    return

################################################################################

def normalize(tableu,pRow,pCol):
# @args tableu  => tableu to be normalized
# @args pRow    => index of pivot element at pivot column
# @args pCol    => index of pivot column

  for i in range(len(tableu[pRow])):
    if i == pCol: continue
    if tableu[pRow][i] == 0: continue

    # Divide pivot row with pivot element
    tableu[pRow][i] /= tableu[pRow][pCol]
    tableu[pRow][i]  = round(tableu[pRow][i],4)

    # Transform each column
    for j in range(len(tableu)):
      if j == pRow: continue
      tableu[j][i] -= tableu[j][pCol]*tableu[pRow][i]
      tableu[j][i]  = round(tableu[j][i],4)

  # Turn pivot element to 1 and pivot column to zeroes
  tableu[pRow][pCol] = 1
  for j in range(len(tableu)):
    if j == pRow: continue
    tableu[j][pCol]  = 0

################################################################################

def addTableu(tableuHistory, tableu):
  tableuHistory.insert(0,[])
  for i in tableu:
    tableuHistory[0].append(i[:])

def addSolution(basicSolHist,tableu,var_names):
  basicSolHist.insert(0,{})
  for i in range(len(tableu[0])-2):
    col = list(map(lambda x: x[i],tableu))

    # check if column is normalized
    if col.count(0) == len(col)-1:
      try:
        basicSolHist[0][var_names[i]] = tableu[col.index(1)][-1]
      except Exception:
        basicSolHist[0][var_names[i]] = 0
    else:
      basicSolHist[0][var_names[i]] = 0
  if tableu[-1][-2] == -1:
    basicSolHist[0]['Z'] = -tableu[-1][-1]
  else:
    basicSolHist[0]['Z'] = tableu[-1][-1]

################################################################################

def simplex(tableu,var_names,tableu_hist_n=10):
# @args tableu   => (2D list) initial tableu created from obj fxn and constraints
# @args tableu_history_n => (int) max number of tableu states to save, default 5

  tableuHistory = []
  basicSolHist = []

  while True:
    addTableu(tableuHistory,tableu)
    addSolution(basicSolHist,tableu,var_names)
    if len(tableuHistory) > tableu_hist_n:
      tableuHistory.pop()
      basicSolHist.pop()

    pivotColumn = selectPivotColumn(tableu[-1])
    if not type(pivotColumn) == int: break

    pivotRow = selectPivotRow(\
      list(map(lambda x: x[pivotColumn],tableu)),\
      list(map(lambda x: x[-1],tableu)))
    if not type(pivotRow) == int: break

    normalize(tableu,pivotRow,pivotColumn)

  # tableuHistory[0] is the latest(final) tableu that contains solution
  # basicSolHist[0] is the latest(final) optimized solution to the tableu
  return tableuHistory,basicSolHist

################################################################################

if __name__ == '__main__':

  var_names = ['x1','x2','s1','s2','s3','s4','Z','ANS']
  tableu = [
    [   7,  11, 1, 0, 0, 0, 0, 77],
    [  10,   8, 0, 1, 0, 0, 0, 80],
    [   1,   0, 0, 0, 1, 0, 0,  9],
    [   0,   1, 0, 0, 0, 1, 0,  6],
    [-150,-175, 0, 0, 0, 0, 1,  0]
  ]

  # var_names = ['x1','x2','s1','s2','s3','s4','Z','ANS']
  # tableu = [
  #   [1,1,1, 0,0,0,0,400],
  #   [1,1,0,-1,0,0,0,200],
  #   [1,0,0, 0,1,0,0,200],
  #   [0,1,0, 0,0,1,0,300],
  #   [-6,-5,0,0,0,0,-1,-16200]
  # ]

  # var_names=['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10','x11','x12','x13','x14','x15',
  # 's1','s2','s3','s4','s5','s6','s7','s8','Z','ANS']
  # tableu = [
  #   [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0, 1,0,0,0,0,0,0,0,0,310],
  #   [0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0, 1,0,0,0,0,0,0,0,260],
  #   [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0, 1,0,0,0,0,0,0,280],
  #   [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,-1,0,0,0,0,0,180],
  #   [0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,-1,0,0,0,0, 80],
  #   [0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,-1,0,0,0,200],
  #   [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,-1,0,0,160],
  #   [0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,-1,0,220],
  #   [10,8,6,5,4,6,5,4,3,6,3,4,5,5,9,0,0,0,0,0,0,0,0,-1,0]
  # ]

  tableuHistory,solHistory = simplex(tableu,var_names)

  for i in range(len(tableuHistory)):
    print('tableu: ',i)
    for j in var_names:
      print(j.center(8),end=' ')
    print()
    for j in tableuHistory[i]:
      for k in j:
        print(str(k).rjust(8), end=' ')
      print()
    print()

    print('Basic Solution:')
    for j in var_names:
      try:
        print(j.ljust(3),' = ',solHistory[i][j])
      except Exception as e:
        pass
    print()
