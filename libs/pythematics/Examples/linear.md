# Linear Algebra

> There is hardly any theory which is more elementary (than linear algebra), in spite of the fact that generations of professors and textbook writers have obscured its simplicity by preposterous calculations with matrices. - Foundations of Modern Analysis, Vol. 1

That's **exactly** what this submodule aims to simplify and automate while giving a visual interpretation of what it is doing.


### Table of contents (Linear Algebra)

- [Some Very Basic Operations (**Adittion**, **Subraction**,**Multiplication** and Vector **Products**)](#basic-operations)
- [Learning The fundamental Operations while finding the Eigen-Vectors and Eigen-Values of a Matrix](#learning-the-operations-by-finding-the-eigen-vectors---values-of-a-matrix)
   - [Finding the determinant of a Square Matrix](#determinant-in-detail)
   - [Solving Linear Systems of Equations](#linear-systems-of-equations)
   - [Mapping Each Element of a Matrix](#TODO1)
- [List of extra **usefull** operations (**Inverse**,**Cofactors**,**Transpose** ...)](#TODO4)

## Basic Operations

The way to Declare a **Matrix** is by passing a **list of lists**, each representing the row of the collumn, while on the other hand you declare a **Vector** by passing in an array of arguments.

The **following** Matrix and Vector Instances:

- Matrix
> ![Matrix](Latex/linear/matrix.png) 
- Vector
> ![Vector](Latex/linear/vector.png)

would be translated into this:

```python
from libs.pythematics import *

# Create a Matrix passing rows
A = Matrix([
	[1, 2, 3],
	[4, 5, 6],
	[7, 8, 9]
])
# Or if you wanted to do the same with collumns
A_col = CreateMatrixPassingCollumns([
	[1, 4, 7], [2, 5, 8], [3, 6, 8]
])
# Declaring a Vector
B = Vector([
	1, 2, 3
])
```
And thus the Output would be a nice visual representation 

```cpp

 // Matrix A and A_col

 CI |   C1        C2         C3
 R1 |   1          2          3
 R2 |   4          5          6
 R3 |   7          8          8

3 x 3 Matrix

// The Vector

R1|   1
R2|   2
R3|   3

3 x 1 Vector array
```

Matrix-Vector Operations such as **Multiplication**, **Addition** and **Subtraction** are defined as they are used in Mathematics

- You can Only Multiply two **Matrices** **A** and B if the number rows of **A** is equal to the number of **collumns** of **B**.
- You can **Add** two **Matrices** **A** and **B** if they have the exact same dimensions (Rows,Collumns)
- The above also applies for Matrix **Subtraction**

- The only operation you can Perform with a **scalar** is multiplication (**Scaling** a Matrix)

The same **rules** apply to **Vectors** (Same dimensions for **Add (+)** AND **Sub (-)** and Only multiplication by a **scalar**) with The only Exception that there are 2 ways you can Multiply Vectors Togther:

- **Dot Product** outputs a Scalar

- **Cross Product** outputs another Vector

The **Dot** Product is well defined in any dimensions but the **Cross** Product if we stick to linear algebra is only defined on **3D** space (sometimes in **7D**) but can be generalised using complex math such as **Octanions** or **Quaternions**

To avoid **confusion** the cross Product of two Vectors remains in **3 Dimensions**

```python
A = Matrix([
	[1, 2],
	[3, 4]
])

B = Matrix([
	[1, 2, 3, 4],
	[5, 6, 7, 8]
])

w = Vector([
	1, 2, 3
])

v = Vector([
	4, 5, 6
])

angle = (w * v) / (magnitude(w) * magnitude(v))  # Or if you like
angle = w.dot(v) / (magnitude(w) * magnitude(v))

from libs.pythematics import arccos  # For Computing the angle

print(A * B)  # WARNING : B*A is not the same!
print(A + A)  # SAME DIMENSIONS 
print(w.cross(v))  # The Cross product of w and v
print(arccos(angle))  # The angle between Vector w and v in radians

```
- The **Output** (In order)

```c
// A*B

 CI |   C1        C2         C3         C4
 R1 |  11         14         17         20
 R2 |  23         30         37         44

2 x 4 Matrix

// A + A (same as 2*A)

 CI |   C1        C2
 R1 |   2          4
 R2 |   6          8

2 x 2 Matrix

//Cross Product

R1|  -3
R2|   6
R3|  -3

3 x 1 Vector array

0.22375608124549928 //The Angle in radians
```

Of course for finding the angle of two Vectors there already exists a function `AngleBetweenVectors` and for the magnitude `magnitude` but we just recreated it here for example purposes

## Learning the operations by finding the Eigen Vectors - Values of a Matrix

What [Eigen-Vectors](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) and [Eigen-Values](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) are does not really matter as we only need the Algorithm to compute them since many of the fundamental operations are Involved in this process. In addition, there already exists a callabe method `EigenVectors` or if you like `.EigenVectors()` but we're going to build it here from scratch for the sake of **Learning**

> Eigen-Vector of a square Matrix **A** is a Vector ![w](Latex/linear/w.png) that when multiplied by a scalar **λ** it produces the same result as multiplying that scalar **λ** with Matrix **A**. Mathematically :  ![eigen](Latex/linear/eigen.png), where both sides are Vectors

The Method for computing them for an **NxN** Matrix goes as follows

>Find The **Characteristic-Polynomial** of that Matrix by doing the following steps:
   - Multiply The n dimensional **Identity Matrix** with **λ** (**λ** here acts as a Polynomial) and subtract the result from **A**
   - Find the Determinant of the Matrix generated above

The determinant will return a **Polynomial** (as the name suggests) whose **roots** are the **eigen-values** of the Matrix **A**.

> Proceed with the following steps
* Compute the roots of the **Characteristic-Polynomial** and store them in memory in an array as **roots**
* Get the Matrix from the very first step **A**-(**λ** * **Identity Matrix**) store it in memory as **sub**
- Declare a Dictionary **dict** Where we're storing the **Eigenvalues** with their coressponding **Eigenvectors**

Now Perform the following steps (in pseudo-code)

- **for** each **root** in **roots** (roots of the **Characteristic-Polynomial**)
   - **Take** the Matrix **sub** (First Step) and wherever you see **lamda** substitute the **root**
   - **Take** the above **Matrix** and Solve the Corresponding System with target output the **0 Vector**
   - **Take** all the solutions from the above **result** put them in a Vector and insert that Vector into **dict** with a key of **root**  `{root:result}`


**That's it**, if you did not understand any steps, no worry, you can continue and see the real code

### Using The Real Code

First we need to make a function that finds the **Characteristic-Polynomial** but because we need to perform operations with **Polynomials** we need to import the coresponding module (if you want more info about Polynmials check [here](#TODO))

```python
import libs.pythematics.linear as lin  #For Matrix-Vector stuff
from libs import pythematics as pl

x = pl.x  #Instead of lamda we are going to use x
```

Now we need to find a Way to get the Identity matrix of **N** dimensions and also find a **determinant**, and luckily, there exists a function `IdenityMatrix` and a `determinant` one, and also all the Matrix operations are also defined so we are **OK**

```
def characteristic_polynomial(square_matrix : Matrix): 
    assert square_matrix.is_square() #DO NOT FORGET TO CHECK IF THE MATRIX IS SQUARE
    A = square_matrix 
    dimensions : int = A.__len__()[0] #Returns (Rows,Collumns) either will do, (square-matrix they're equal)
    identity_matrix : Matrix = IdenityMatrix(dimensions) #The Idenity Matrix
    polynomial_matrix : Matrix = A - (x * identity_matrix) #Subtract the scaled matrix from A
    det : pl.Polynomial = scaled_matrix.determinant() #Find the Determinant
    return det,polynomial_matrix 
```

Here I'm declaring the type of each variable so as for the code to make more sense

- `A.__len__()` returns the dimensions of the matrix but because it is square, they are exactly the same
- `A - (x * identity_matrix)` Operations with normal numbers as well as Polynomials are well defined
- `det` which is the determinant of `polynomial_matrix ` will produce a Polynomial in this case

- `return det,polynomial_matrix` We need both the **Polynomial** and the **Matrix** for further computations (see above)


> Do not forget that `.determinant()` (or `determinant(matrix)` if you wish) is only possible if the Matrix has the **same** number of **rows** and **collumns** - **Square** Matrix

**NOTE** : `polynomial_matrix` will produce a Polynomial in this case (Point **3**)

In this specific case we have a Matrix that consists of Polynomials and calculating the **Determinant** involves some Polynomial Operations since they are treated normally as Any Number, For **Example**:

### Determinant In Detail

A determinant is usefull for many things such as Matrix **inversion** and **Solving** linear systems and in fact many of the **built-in** functions (the module) are based on the determinant such as`.inverse()` - `inverse` and `.solve()` - `solveCramer`.

For computations the module uses **Cramer's** recursive rule for computing the determinant

```python
A = IdenityMatrix(dimensions=3) #The Identity Matrix
B = Matrix([
    [1,2,3],
    [4,5,6],
    [7,8,9]
])
x = pl.x #The polynomial 'x'
polynomial_matrix = A*(x+1)
print(B)
print(B.determinant())
print(polynomial_matrix)
print(polynomial_matrix.determinant()) 
```
- **Output** (In order)

```c

 CI |   C1        C2         C3
 R1 |   1          2          3
 R2 |   4          5          6
 R3 |   7          8          9

3 x 3 Matrix

0 // The determinant of the integer Matrix above

 CI |   C1        C2         C3
 R1 | (x+1)        0          0
 R2 |   0        (x+1)        0
 R3 |   0          0        (x+1)

3 x 3 Matrix

Polynomial of degree 3 : x^3 + 3x^2 + 3x + 1 //The determinant of the Above polynomial Matrix
```


Now we need to define our function that actually finds the Eigen-Values and for that we need
 1. Another function for  finding the **roots** of the Polynomial which are the **Eigenvalues**
 2. A Method to Solve a system of linear equations which will give us the **Eigenvectors** 

The corresponding methods are `.roots` for the **Polynomials** and `.solve` for the **Eigenvectors** and Specifically

> `matrix.solve(unknowns : Union[tuple,list],output : Vector)`, We need to provide a tuple or a list containing the names of the variables we need to solve for and the desired output we want to get

### Linear Systems of Equations

To better understand how the `.solve()` method works consider the following system of equations

> ![Example System](Latex/linear/system.png) 

If you were to solve this system using **Cramer's Method**  (`SolveCramer`) or by **Row-Reduction** (`solveREF`) You would Probably Write the system of equations in the following **Matrix** format in a similar or exactly this format

> ![System In Matrix](Latex/linear/matrix_system.png)

and here that's exactly what you need to pass but in a slightly different format

- The **Outputs** : **5** and **11** as a `Vector`
- the **Unknowns** : **x** and **y** as a **list** or a **tuple** `('x','y')`

```python
import libs.pythematics.linear as lin

A = lin.Matrix([  #The Coefficient Matrix
	[1, 2],
	[3, 4]
])

unknowns = ('x', 'y')  #The Unknowns
output = lin.Vector([5, 11])  #The output that will make the augemented Matrix
solution1 = A.solve(output, unknowns)
solution2 = A.solve(output, unknowns, useRef=True)
print(solution1)
print(solution2)
```
Here we in `solution2` we are setting `useRef=True` which means that we are solving the system by row reduction while on `solution1` we are using **Cramer's** method of the determinants, and in both cases the result is the same of-course

> `{'x': 1.0, 'y': 2.0}`

or if you for whatever reason do not like the class-method of doing it you can instead use

```
cramer = lin.SolveCramer(A,output,unknowns) 
reduction = lin.solveREF(A,output,unknowns)
```

In general `useRef=True` or if you like `solveREF` is more powerful that `solveCramer` in situations where there are infinitely many solutions, when **Cramer's Method** fail's if you specify the parameter `ContinueOnFail=True` it will solve the remaining equations picking the value "1" for the **free** variable (That's the default) (**AND THE METHOD IT WILL USE WILL BE ROW REDUCTION**) which you can of course change if you explicitely call `solveREF` and set the parameter `onFailSetConst`. if there are **NO** (Rank of **Coefficient** Matrix is less than rank of **Augemented** Matrix) solutions it will throw an `AssertionError`

Here in our example the Matrix that will be produced (by substitution) will always have infinite solutions so we are going to use **Row Reduction** to improve Performance

Continuing on where we left, we know we can Solve the Polynomial equation and the Linear system but how can we substitute the eigen Vectors wherever we see **lamda**?

### Mapping Items of a Matrix

The answer to this is the `.forEach()` method which for each element of the Matrix it Applies a certain function and returns a new **Matrix** with that function applied to every element - something like array **
map**

```python
from libs.pythematics.functions import exp


def sigmoid(x):
	return 1 / (1 + exp(-x))


print(A.forEach(sigmoid))

#  CI |   C1        C2
#  R1 |  0.98       0.73
#  R2 |  1.0        0.95

# 2 x 2 Matrix
```
The Polynomial Matrix we Generate will look some like this (the **sub** Matrix from the very first step)

```c
 CI |   C1        C2
 R1 | (-x+4)       1
 R2 |   6        (-x+3)

```

Then you can get the **Polynomial** as a function is by using the `.getFunction()` method, which will return a fully usable lamda function

So to substitute for each element we are goind to use the `.forEach()` method and define a new function `substitute` which given a number it will substitute it into any Polynomial it finds

```python
import pythematics.polynomials as pl

x = pl.x

def substitute(expression ,number):
    if not type(expression) == type(x):
        return expression #if not a Polynomial simply return the expression
    return expression.getFunction()(term)
```
And now since we know everything, we can complete our function

```
def eigenvectors(matrix):
    char_pol = CharacteristicPolynomial(matrix) #Find the Characteristic Polynomials and the sub Matrix
    char_pol_roots = char_pol[0].roots(iterations=50) #Find the roots of the 1st element (Polynomial)
    sub_matrix = char_pol[1] #The 0th element is the sub matrix
    output = Vector0(dimensions=matrix.__len__()[0]) #Our Target is the 0 Vector of N dimensions 
    unknowns = [i for i in range(matrix.__len__()[0]) #The names of our 'unknowns'
    eigen_dict = {} #The Dictionary in which we will store the Values with their Vectors
    for root in char_pol_roots:
          m_0 = sub.forEach(lambda num : substitute(num,root)) #Substitute the Eigen Values in the Lamda scaled Identity Matrix
        eigen_vector = m_0.solve(output,unknowns,useRef=True) #Solve the linear system
        eigen_vector = Vector([eigen_vector.get(sol) for sol in eigen_vector])
        eigen_dict[root] = eigen_vector #Eigen value has a coressponding Vector
        #Insert into the dictionary the root with it's eigen Vector
```
Each **eigenvalue** has **infinite** coressponding **eigenvectors** but we are only goind to return one for the sake of simplicity (You can find them by instead of substituting the number **1** to use another Polynomial to get a formula, while Solving the **Linear Equations**)


To test our function we're going to use The following simple **2x2** Matrix

> ![Eigen Example Matrix](http://www.sciweavers.org/upload/Tex2Img_1599685273/render.png)

```python
from libs.pythematics.linear import *

A = Matrix([
	[4, 1],
	[6, 3]
])

vs = EigenVectors(A)
for item in vs:
	print(A * vs[item])
	print(item * vs[item])
```

- **Output**

```cs
 CI |   C1
 R1 | -0.33
 R2 |   1

2 x 1 Matrix


R1| (-0.3333333333333333+0j)
R2| (1+0j)

2 x 1 Vector array


 CI |   C1
 R1 |   3
 R2 |   6

2 x 1 Matrix


R1| (3+0j)
R2| (6+0j)

2 x 1 Vector array
```

And in fact it is correct (**despite** a small floating point Error in the first **Vector**)

### Aditional Methods

**Methods** and their corresponding **functions** for Matrix Manipulation

|Method|Functional |Description|
|-------------------|---|---|
|`.inverse()`     | `inverse`   |Finds the Inverse of a square Matrix   |
|`.ref()`| `ref`  | Returns the REF of a Matrix   |
|`.determinant()`         |`determinant`   | Finds the Determinant of a square Matrix  |
|`.transpose()` |`adjugate`   |Returns the passed Matrix Transposed   |
|`cofactors()`    | `MatrixOfCofactors`  |Returns the Matrix of cofactors of a Matrix   |
|`.minors()`    |`MatrixOfMinors`   |Returns the Matrix of Minors of a Matrix   |
|`.trace()`      |`Trace`   |Returns the sum of the diagnals   |
|  None         |`IdenityMatrix`   |Returns the Identity Matrix of N dimensions   |
| `.swap`          |    `SwapNoCopy`              | Swaps 2 rows of a given Matrix                    |

**Methods** for Solving systems of Equations

|Name|function |Description|
|-------------------|---|---|
|Row Reduction     | `.solve(useRef=True)` and `solveREF`   |Solves using row Reduction   |
|Cramer's rule| `.solve` and `solveCramer`  | Finds determinants recursively|

**Vector** Operations - Methods for manipulation

|Method|Functional |Description|
|-------------------|---|---|
|`.dot()` or by * operator     | `dot`   |Dot Product of 2 Vectors|
|`.cross()`| `cross`  | Cross Product of 2 3D Vectors|
|`.magnitude()`         |`magnitude`   | Magnitude of a Vector |
|`.AngleVector()`         |`AngleBetweenVectors`   | Returns the angle between 2 Vectors |

