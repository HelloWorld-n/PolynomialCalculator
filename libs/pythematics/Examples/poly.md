### Sections (Polynomials)
- [Getting to know the basics by solving 2 equations](#getting-down-to-the-interesting-stuff)
    - [Basic Linear Equation](#first-degree-linear-equation)
    - [More complex equations with fractions](#second-Example-with-polynomial-division)
- [Root finding methods (Generalised)](#root-finding-methods)
- [Delving deeper into Polynomials](#delving-deeper-into-polynomials)


You can easily work with Polynomials via the `polynomials.py` module

Here you use polynomials as per their default definition :
> In mathematics, a polynomial is an expression consisting of variables (also called indeterminates) and coefficients, that involves only the operations of addition, subtraction, multiplication, and non-negative integer exponentiation of variables (Wikipedia forgot division).

- Assuming that you do not re-define `x` you can simple use this all for you operations

```python

from libs import pythematics as pl

x = pl.x  # You define the 'x' variable
P = 3 * x + 1
```
This would give the following output aimed at visualiazation:

```
Polynomial of degree 1 : 3x + 1
```

### Getting down to the interesting stuff

In the following two examples we will bring these two Polynomials into a solvable form performing math operations such as bringing all variables to one side and performing various Polynomial Operations. After that we will see a very **POWERFUL** method that can sove any Polynomial equation once it is brought into form, and discuss about other non-Polynomial ways of solving any Equation you can think of.


Let's consider the Following 2 algebraic equations : 
- **First** Degree 

>![First equation](Latex/eq_1.png)

- **Uknown** as of now Degree (*Polynomial Division*)

>![Second Equation](Latex/eq_2.png)

### First Degree Linear Equation
We will begin by writting out the equation and for convenience we are going to split it into variables

```python

from libs import pythematics as pl

x = pl.x

term_0 = - (x / 2)
term_1 = (x + 3) / 3
side_0 = term_0 + term_1  # The first side of our equation
side_1 = x + 1  # The second one
final_polynomial = side_0 - side_1  # Bring everything to one side
```
Basically right now we've almost solved this equations by **JUST WRITTING IT**, in more Depth see what is going on at each variable declaration if we print everything


```
Polynomial of degree 1 : - 0.5x // term_0 (Divides x by 2 and taktes the negative of that)
Polynomial of degree 1 : 0.3333333333333333x + 1 //term_1 (Divide x and 3 by three)
Polynomial of degree 1 : - 0.16666666666666669x + 1 // side_0 (add term0 and term1)
```
And thus the result is the difference of the 2 sides `side_0 - side_1 = 0` :
```
Polynomial of degree 1 : - 1.1666666666666667x 
```
Of course the root here is easy to find and it's zero (Because the remainder difference of the two sides `side_0-side_1` is equal to one) and we did not have to use a root finding method or do anything complex other than just write the equation, but what if things are not so simple?

 ### Second Example with Polynomial Division


Here we can see 2 fractions that are both being divided by a Polynomial

- You could try doing Polynomial division in the first expression but you would end up doing nothing helpful
- In the second expression you can't do anything

Here is where `LCM` (Least common multiple) comes in handy (The equivalant of LCM in `num_theory.py`) . We are going to repeat what we did before but with a few adjustments
```python
#Find the LCM of x+1 and x (The terms that we are dividing with)
pol_lcm = LCM_POL(
    x+1,x
)

 # we multiply everything by pol_lcm (To get rid of the division)
term0 = (x * pol_lcm) / (x+1)
term1 = (8 * pol_lcm) / (x)
s0 = term0[0] - term1[0] #We are performing polynomial division which gives (Output,Remainder)
s1 = pol_lcm * 1 #Do not forget to multiple the next side as well with pol_lcm
final_polynomial = s0-s1 #Move everthing to one side
```
Now one way to get the root of this equation is by using  **Newton's method**

```python
from libs.pythematics.functions import NewtonMethod

f_p_function = final_polynomial.getFunction()  # Aquire the function of the pol (callabe)
root_0 = NewtonMethod(f_p_function, 2, iterations=50)  # Use 50 iterations to approximate and a start point
```
The output is `-0.888888888888889` which infact is the only root of this equation, still we haven't used are **best** tool for this because it would be overkill

Some things ought to be explained here in more depth:

#### What's going on during the division step?

> s0 = term0[0] - term1[0]

Here we are using indexes because the actual output is a list containing The result and remainder of the division 
```python
term0 = (x * pol_lcm) / (x+1) #Polynomial division works if the numerator is of higher degree than the denominator
print(term1)

>> [Polynomial of degree 1 : 8x + 8, 0] # Polynomial in 0 index and remainder in 1
```

The remainder can either be another Polynomial or a scalar value : `int`,`float` or even `complex`

In this case the `LCM_POL` which represents the LCM multiple of these polynomials:

> **Finds the smallest Polynomial that can equally be devided by all of these Polynomials**

In **every** case the division will have a remainder of 0 , so it is safe to always use the 0th term

#### Why use Newton's method? How does it even work? What else is there to use?

## Root finding methods

By definition **Newton's** method is described as : 

> In numerical analysis, Newton's method, also known as the Newton–Raphson method, named after Isaac Newton and Joseph Raphson, is a root-finding algorithm which produces successively better approximations to the roots (or zeroes) of a real-valued function (using fixed point iteration). - Wikipedia

You begin with a starting point `starting_point : Union[float,int]` and each time You solve the linear equation of the slope of function getting closer each time (finding the derivative of the function)

This technique and generally all techniques that include fixed point iteration are very powerfull and that's a reason why all the following functions that you will now see use it as well

Another alternative for real roots is the **Secant** Method which does the same but with 2 points

```python
final_polynomial = s0-s1
f_p_function = final_polynomial.getFunction()
root_0 = SecantMethod(f_p_function,1,2,2) #(input function,starting_point_1,point_2,iterations)
print(root_0)
```
This outputs `-0.8888888888888888` as well but with only 2 iterations and no derivative computation

The secant method needs just few iterations to find the result and because it converges very fast this often causes `ZeroDivisionError` errors at even a few iterations more than normal 

The number we chose was `2`, at the very next number `3` it causes an Error

```
ZeroDivisionError: float division by zero
```

Perhaps the most **powerful**  method is the **Durand–Kerner** method which gives all complex roots of Polynomial equations, the only downside being this is limited to Polynomials (On the other hand Newton and Secant work on non-polynomial equations)

Let's consider the following Polynomial

```python
P = x**2 - 8*x - 9 #You can generate this using s0-1 from the equation example
```
To get all of it's roots we can apply the above method as follows

```python
roots = P.roots(iterations=50)
print(roots)
#or if you wish by the functional method
adjusted_polynomial = reduceCoefficients(final_polynomial)
roots = applyKruger(adjusted_polynomial.getFunction(),adjusted_polynomial.degree,50)
print(roots)
```
The output in both cases is exatctly the same

```python
[(-1+0j), (9+0j)] # A list of complex numbers which are the roots (Generated in iteration 10)
[(-0.9999999869391464-4.333046649490722e-08j), (8.999999986939148+4.33304664947988e-08j)] #Iteration 9
```
This method also requires some starting points but because it doesn't really matter, they are automatically generated completely randomly using `pythematics.random`

Notice how in the functional method we used `reduceCoefficients(final_polynomial)`, what this does is, Makes sure that the leading coefficient of the Polynomial is 1 as is required per the **Durand-Kerner** method, so,ething you don't have to worry about if calling the method `instace_of_polynomial.roots()`

Also you are offered the ability to adjust iterations and benchmark yourself

Here is a more practical Example

> ![Third Equation](Latex/eq_3.png)

```python
P = 5*x**4 + 3*x**2 + 2*x**2 +1
roots = P.roots(iterations=50)
for root in roots:
    print(f'{root} : {P.getFunction()(root)}') #getFunction() returns a lamda Function of the Polynomial
```
- Output
```
-0.5257311121191336j : 0j
0.5257311121191337j : 0j
-0.8506508083520399j : 0j
0.8506508083520399j : 0j
```

Also something to note here is that the result will always be declared as a complex number even when the output is only real (No checking is done)

> REMINDER : **Durand-Kerner** is for polynomials only

## Delving deeper into Polynomials

As of now all Polynomial arithimtic was defined using `x = pl.x ` and normal operations giving it a nice Pythonic feeling, and clearly it is just a more natural way 

```python
P = x*(x+1) + x**2 + 3*x +1 #This feels way to Pythonic
```
But that is not how the system interprets it and there are some other methods to declare an instance of Polynomial

```python
P = Polynomial([3,4,1]) #The Class method of doing it which explains how everything works
G = PolString("x^2 + 4x + 3") #The string method of doing it
#In fact pl.x is just the following
x = PolString("x") #or
x = Polynomial([0,1])
```
This would output the following Polynomial
```
Polynomial of degree 2 : 1x^2 + 4x + 3 #P and G
Polynomial of degree 1 : + 1x #x
```

Despite the existance of the functions `derivative` (or `derivativeNth`) and `integral` in **functions.py** which work at all cases perfectly they do not actually provide an observable and visualizable formula and to achive this you can use the `.diffrentiate` and `.integrate` methods for Polynomials

```
P = Polynomial([3,4,1])
print(P.diffrentiate()) #Polynomial of degree 1 : 2x + 4 
print(P.integrate()) #Polynomial of degree 3 : + 0.333x^3 + 2x^2 + 3x
```

As a remainder you can use `polynomial.getFunction()` to get a callabe of the corresponding polynomial
