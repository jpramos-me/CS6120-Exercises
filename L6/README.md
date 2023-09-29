# Tasks

- Implement the ''into SSA'' and ''out of SSA'' transformations on Bril functions.
        
  - One thing to watch out for: a tricky part of the translation from the pseudocode to the real world is dealing with variables that are undefined along some paths.

  - Previous 6120 adventurers have found that it can be surprisingly difficult to get this right. Leave yourself plenty of time, and test thoroughly.
    
- As usual, convince yourself that your implementation actually works!
  
  - You will want to make sure the output of your “to SSA” pass is actually in SSA form. There’s a really simple is_ssa.py script that can check that for you.
  
  - You’ll also want to make sure that programs do the same thing when converted to SSA form and back again. Fortunately, brili supports the phi instruction, so you can interpret your SSA-form programs if you want to check the midpoint of that round trip.
    
- Measure the overhead. If you take a program on a round trip through SSA form and back, how many more instructions (static or dynamic) does the final program have than the original? Report this overhead so you can compare your implementation against the rest of the class.
