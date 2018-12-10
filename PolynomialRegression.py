# Function definitions of methods required
# for estimation using Polynomial Regression

################################################################################

import GaussJordan as gj

def createMatrix(x,y,n=1):
# creates an augmented coefficient matrix from
# x - list of values (independent variables)
# y - list of values (dependent variables)
# n - degree of polynomial to be used for estimation (default 1)

  matrix = []

  # populating lhs of coefficient matrix
  for i in range(n+1):
    row = []
    for j in range(n+1):
      row.append(0)
      for k in range(len(x)):
        row[j] += x[k]**(i+j)
      row[j] = round(row[j],4)
    matrix.append(row)

  # populating rhs of coefficient matrix
  for i in range(n+1):
    matrix[i].append(0)
    for k in range(len(x)):
      matrix[i][n+1] += x[k]**i*y[k]
    matrix[i][n+1] = round(matrix[i][n+1],4)

  return matrix

################################################################################

def regression(x,y,n=1):
# performs polynomial regression of degree n on x,y data points 
# returns a function which estimates the value yield by a given x

  if not len(x)==len(y):
    print('Error: X and Y are not of the same length')
    return

  if n < 1 or n >= len(x):
    print('degree of polynommial is not valid')
    return

  solution = gj.solve(createMatrix(x,y,n))

  fxn = ''
  for i in range(len(solution)):
    temp = str(solution[i])
    if i > 0:
      temp += 'x'
    if i > 1:
      temp += '^'+str(i)
    if i < len(solution)-1:
      temp = ' + '+temp
    fxn = temp + fxn
  fxn = 'f(x) = '+fxn

  def estimate(x):
    ans = 0
    for i in range(len(solution)):
      ans += solution[i]*x**i
    return round(ans,4)
  
  return fxn,estimate

################################################################################

if __name__ == '__main__':
  x = [50,50,50,70,70,70,80,80,80,90,90,90,100,100,100]
  y = [3.3,2.8,2.9,2.3,2.6,2.1,2.5,2.9,2.4,3.0,3.1,2.8,3.3,3.5,3.0]
  f_str,f = regression(x,y,2)
  print(f_str)
  print(f(60))
