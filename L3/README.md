# Tasks
- Implement “trivial” dead code elimination, in which you delete instructions that are never used before they are reassigned. Remember to iterate to convergence. (This should not take you long.)
- Implement local value numbering. Make sure it eliminates some common subexpressions. Try pairing it with trivial dead code elimination as a post-processing step. (This might take you quite a while.)
- In your summary on the GitHub Discussions thread, briefly write up the evidence you have that your LVN implementation is correct and actually optimizes programs. (Hint: To be convincing, do not just use a few handcrafted test cases. One good way to do this is to run it on all the benchmarks in the Bril repository, perhaps using Brench. But this is truly open ended; you do you!)
- For bonus “points,” extend your LVN implementation to optimize the trickier examples given in class.
