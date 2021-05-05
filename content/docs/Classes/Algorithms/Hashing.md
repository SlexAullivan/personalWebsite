# **Hashing**

Date: Mar 2, 2021
Module: four

## **Dictionary (ADT)**

- Maintain set of items ( key, Value)
- insert an item (key, value)
- delete items (key, value)
- search (key) to get specified value
- insert item ( do not allow duplicate keys to exist)
- {{<katex>}}O(1){{</katex>}} time, expected time not worst case time
- We are leaving the comparison model, since we proved the fastest search time is {{<katex>}}O(nlog(n)){{</katex>}}
- Can not find nearby values, or minimum/ maximum values as easily since we are not within the comparison model.

## **Python Dictionaries**

Create: `D = dict()`

Insert: `D[key] = value`

Search: `D[key]` → Gives a `value`

delete: `del D[key]`

`d.items` → `[ (k,v) , (k,v) ... ]`

## **Motivation:**

- Document Distance
- Databases, Most do but not all
- word → definition dictionary ( An actual dictionary )
    - words are keys, definitions are values
- Spell Checkers, nearby words
- Login credentials, key username, password is a hashed version of the password

## **Simple Approach**

Direct Access table or array

- items in array indexed by key

    ### **Bad**

    1. requires keys to be integer
    2. Memory hog

    Solution to problem 1: pre-hash ( maps keys to non-negative integers)

    Solution to problem 2: Hashing

    Origins of the word hash: to cut into pieces and mix around.

    - map the set of all possible keys ( after pre-hashing ) to a valid index in the array
    - Collision is when two keys map to the same index within the array

    ![Hashing%2092cc8c69f2bb441abedc01f6bc9f416c/Untitled.png](/images/hashing1.png)

    Chaining to Deal with collisions:

    ![Hashing%2092cc8c69f2bb441abedc01f6bc9f416c/Untitled%201.png](/images/hashing2.png)

## **Simple Uniform Hashing**

Uniformity:

any arbitrary key is equally likely to be mapped to any index in the table.

Independence:

independent of where the other keys are hashed.

### **Hashing with Chaining Analysis:**

n keys, m indexes

what is the expected length of a chain ?

{{<katex>}}\alpha = \frac{n}{m} = Load\ Factor{{</katex>}}

if  {{<katex>}}m = \theta (n){{</katex>}} then

then {{<katex>}}\alpha\ is \theta(1){{</katex>}}

if {{<katex>}}\alpha= \theta(1){{</katex>}}, then insert, delete, search take:

hash: {{<katex>}}\theta(1){{</katex>}}  This may not be true, for example with strings that may be very long, but the time is still bounded.

index array: {{<katex>}}\theta(1){{</katex>}} 

find element in chain: {{<katex>}}\theta (\alpha){{</katex>}} if {{<katex>}}\alpha = \theta(1){{</katex>}} then 

## **Example Hash Functions**

1. **Division method**

    {{<katex>}}h(k) = k\ mod\ m{{</katex>}} 

2. **The multiplication Method**

    assume {{<katex>}}m = 2^r{{</katex>}} 

    {{<katex>}}h(k) = [(a * k)\ mod\ 2^w]>>(w-r){{</katex>}} 

    a:  Random Constant 

    w:  Is the length of the word of the machine

    {{<katex>}}a * k{{</katex>}} = 2 words = 2w bits

    {{<katex>}}(a*k)\ mod\ 2^w{{</katex>}} rightmost w bits

    (          ) >> (w-r) → left most r  bits 

3. **Universal Hashing** 

![Hashing%2092cc8c69f2bb441abedc01f6bc9f416c/Untitled%202.png](/images/hashing3.png)