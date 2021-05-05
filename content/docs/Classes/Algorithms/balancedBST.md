
---

title: Balanced Trees and AVL Trees

---

## Balanced BST's

- Importance of balancing
- AVL trees

Remember binary search trees where all items in  nodes subtree are less than the root and all of the items in the right subtree are greater than the root.

## Balancing Trees

### What is a balanced tree?

Ideally we want our tree to have a height of {{<katex>}}\theta(log(n)){{</katex>}}

Thus a BST is balanced if and only if:

1. The hieghts of left/ right subtrees differ by no more than 1
2. The left and right sub trees are balanced

{{<columns>}}

### Find and label the heights of the tree

![](/images/bst0.png)

<--->

### How can we recursively find node heights?

Recurse on both children, then when you return add one to the larger of the subtrees maximum height.

{{</columns>}}

## AVL Trees

AVL trees are a binary search tree that follows the AVL Constraint

### AVL Constraint

Heights of the left and right children differ by at most one for all nodes

We want to prove that the height of an AVL tree are {{<katex>}}\theta(log(n)){{</katex>}}. Lets take a look at the worst case scenario for an AVL tree, where every right subtree is one taller than the corresponding left sub tree.

![](/images/bst1.png)

{{<katex>}}N_h =\ minimum\ number\ of\ nodes\ possible\ in\ AVL\ tree\ with\ height\ h{{</katex>}}

{{<katex>}}N_h = N_{h-1}+N_{h-2}+1{{</katex>}}  

Clearly this sequence is increasing and  {{<katex>}}N_h > 2N_{h-2}{{</katex>}}, meaning that our sequence or number of nodes within the tree at least doubles, thus

{{<katex>}}N_h > 2^{\frac{h}{2}}{{</katex>}} and {{<katex>}}h < 2log(n){{</katex>}}

### Maintaining the AVL Constraint

### AVL Insert:

1. BST Insert
2. Fix AVL Constraint

The Real question here is how do we maintain the AVL constraint, so that by fixing the AVL tree so we don't spend more than the desired {{<katex>}}\theta(log(N)){{</katex>}} time.

### Rotation

![](/images/bst2.png)

Look at the following BST, when we insert 23, we get a doubly left heavy subtree and need to do a right rotate in order to fix our tree to follow the AVL constraint.

![](/images/bst3.png)

Sometimes just doing one single rotation is not enough, for example look wha theppens when we try to insert 55 and right rotate below.

![](/images/bst4.png)

Because 50's left subtree was empty, when we did the right rotate we created a doubly right heavy sub tree, to fix this we should have actually done a double rotation. Shown below.

 

![](/images/bst5.png)

Above we fixed the empty left sub tree, by doing a left rotate on 55. Then fixed the doubly left heavy sub tree of 65 by right rotating.

### Questions

1. A single insertion of deletion creates a violation of the AVL constraint. What is the difference between the offending sub trees? Why?

    2, because the elements are at most already one away from each other so when we insert a new node we are at most adding one to that

2. By Fixing this, we make another violation. What is the difference between the offending sub trees height? why?

    2, the rotated sub trees height either remains the same or decreases by one so the same reasoning from above applies.

### Fixing the AVL Property

```
Suppose x is the lowest node violating the AVL property. 
(Start at inserted node, go up until you find x, fix x as below then 
keep goin up from x)

if x is right heavy
	if right(x) if right heavy or balanced
		then left rotate(x)
	else
		right rotate(right(x))
		left rotate(x)
else
	if left(x) is left heavy or balanced
		the right rotate(x)
	else 
		left rotate(left(x))
		right rotate(x)

```

### Time Complexity of AVL

Time to insert: {{<katex>}}\theta(log(n)){{</katex>}}

number of corrections: {{<katex>}}\theta(h) = \theta(log(n)){{</katex>}}

corrections: {{<katex>}}\theta(1){{</katex>}} time each