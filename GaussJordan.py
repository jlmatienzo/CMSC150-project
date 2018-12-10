# Gauss-Jordan Method of solving systems of equations

################################################################################

def pivotMatrix(matrix,i):
# partial pivoting function
# Swaps the ith row with the row with largest value at ith column

  maxx = matrix[i][i]
  pivot = i

  for j in range(i+1,len(matrix)):
    if maxx < matrix[j][i]:
      maxx = matrix[j][i]
      pivot = j
  
  if not pivot == i:
    matrix[i],matrix[pivot] = matrix[pivot],matrix[i]

################################################################################

def solve(matrix):
# GAUSS-JORDAN with partial pivoting

  for i in range(len(matrix)):
    # pivot matrix
    pivotMatrix(matrix,i)

    # normalize
    divisor = matrix[i][i]
    for j in range(i,len(matrix[0])):
      matrix[i][j] = round(matrix[i][j]/divisor,4)

    for j in range(len(matrix)):
      if j==i : continue
      multiplier = matrix[j][i]
      for k in range(i,len(matrix[0])):
        matrix[j][k] -= matrix[i][k] * multiplier
        matrix[j][k] = round(matrix[j][k],4)

  # solution
  return list(map(lambda x: x[-1],matrix))
  # solution = []
  # for i in range(len(matrix)):
  #   solution.append(matrix[i][-1])

  # return solution

################################################################################