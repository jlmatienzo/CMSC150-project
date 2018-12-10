import GaussJordan as gj

################################################################################

def createMatrix(x,y):
  # creates an augmented coefficient matrix from the generated eqns from
  #   given independent variables X and dependent variables Y
  matrix = []
  colNames = []
  n = len(x)-1
  for i in range(1,n+1):
    if i > 1:
      colNames.append('a'+str(i))
    colNames.append('b'+str(i))
    colNames.append('c'+str(i))
  colNames.append('ANS')

  # ai-1 (x_i-1)^2 + bi-1 xi-1 + ci-1 = f(xi-1)
  # ai (xi)^2 + bi xi + ci = f(xi)
  for i in range(1,n):
    eqn = []
    for j in range(3*n):
      eqn.append(0)
    if i > 1:
      eqn[(i-1)*3-1] = x[i]**2
    eqn[(i-1)*3]  = x[i]
    eqn[(i-1)*3+1]= 1
    eqn[-1] = y[i]
    matrix.append(eqn)

    eqn = []
    for j in range(3*n):
      eqn.append(0)
    eqn[(i)*3-1] = x[i]**2
    eqn[(i)*3]  = x[i]
    eqn[(i)*3+1]= 1
    eqn[-1] = y[i]
    matrix.append(eqn)

  # a1(x0)^2 + b1x0 + c1 = f(x0)
  eqn = []
  for j in range(3*n):
    eqn.append(0)
  eqn[0] = x[0]
  eqn[1] = 1
  eqn[-1]= y[0]
  matrix.append(eqn)

  # an(xn)^2 + bn xn + cn = f(xn)
  eqn = []
  for j in range(3*n):
    eqn.append(0)
  eqn[(n-1)*3-1] = x[n]**2
  eqn[(n-1)*3  ] = x[n]
  eqn[(n-1)*3+1] = 1
  eqn[-1]= y[n]
  matrix.append(eqn)

  # 2*ai-1(xi-1) + bi-1 = 2*ai(xi-1) + bi
  for i in range(1,n):
    eqn = []
    for j in range(3*n):
      eqn.append(0)
    if i > 1:
      eqn[(i-1)*3-1] = 2*x[i]
    eqn[(i-1)*3] = 1
    eqn[i*3-1] = -2*x[i]
    eqn[i*3] = -1
    eqn[-1] = 0
    matrix.append(eqn)

  return colNames,matrix

################################################################################

def createFunctions(solution,x):
  # creates a list of functions in string form
  fxns = []

  for i in range(len(x)-1):
    fxn = 'f(x) = '
    fxn += str(solution[i*3])+'x^2 + '
    fxn += str(solution[i*3+1])+'x + '
    fxn += str(solution[i*3+2])

    fxns.append((fxn,str(x[i])+' <= x <= '+str(x[i+1])))

  # returns a list of tuples of function and cond of x
  return fxns

################################################################################

def interpolation(x,y):
  if not len(x) == len(y):
    print('Error: X and Y are not of the same length')
    return
  
  colNames,matrix = createMatrix(x,y)

  solution = gj.solve(matrix)
  solution.insert(0,0)  # a1 = 0

  fxns = createFunctions(solution,x)
  for i in fxns:
    print(i[0].ljust(50),i[1].rjust(20))

  def estimate(num):
    if num in x:
      return y[x.index(num)]
    
    for i in range(len(x)-1):
      if x[i] < num and num < x[i+1]:
        print('f(',num,') = ',end='',sep='')
        print(solution[i*3],'*',num**2,end=' + ')
        ans = solution[i*3]*num**2

        print(solution[i*3+1],'*',num,end=' + ')
        ans+= solution[i*3+1]*num

        print(solution[i*3+2])
        ans+= solution[i*3+2]
        return ans
  
  # returns a list of function that estimates the value of x
  # returns a function definition that evaluates(estimates) the value of a x
  return fxns,estimate

################################################################################

if __name__=='__main__':
  x = [3.0,4.5,7.0,9.0]
  y = [2.5,1.0,2.5,0.5]
  fxns,f = interpolation(x,y)
  for i in fxns:
    print(i[0].ljust(40),i[1].rjust(20))
  print(f(5))
