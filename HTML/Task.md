HTML Nanoframework.
--

Write a class that can create HTML elements/render/find.

Phase 0: Warm-Up
--

* Install The latest Python Version 3.12.
* Recap Python & Git
* Read about Venv and how to use them.
* Use Venv or Pipenv.
* Use OOP.
* use Python type annotation (Must).

Phase 1: HTML Nanoframework
--
* Write A class that can create an html element.

- this class will take 3 parameters.
  - name ( HTML element name)
  - value ( html element value)
    - can be:
      - Html element.
      - string
      - list of ( Html elements ).
  - attrs ( html element attributes).
    - must be a dict.
  - any invalid name shall case a custom exception.

- upon the creation be careful about the unique html attrs like :id. if there is two or more with the same id must raise an exception.

- this class will have 5 class-level methods.
  - [ ] append
    - this will append children to the current HTML element.
    - if one of the elements has the same id as another element this will fire a custom exception.  
  - [ ] render
    - will render the html element and its own sub-elements like this: ``` <name attr1="attr1_value" ... > value </name> ``` and print it to the stdout.
    - render will respect level indentation, see the use case below to understand.
    - if one of the elements has the same id as another element this will fire a custom exception.  
  - [ ] find elements by attrs
    - will take the element and find an attr value by the attr passed to it in the element itself or in the sub-elements.
    - example `find_elements_by_attr(elem, 'id', 'first')`. this will find the element with id first.
    - if the attr is `id` then it should be special for each element, there is no element that can have the same id.
    - in the render call if there are two elements that have the same id you need to raise a custom exception. 
  - [ ] find element by tag name
    - will take the element and find all tags that match the tag passed to it in itself or in the sub-elements.
  - [ ] render an HTML file.
    - will render the element and the sub-element into an HTML file.
    - the file shall have the doc type in the beginning.
  
 > Find a good mechanism to track all Html element ID(s).
 
 - write a small design spec.
 - write testcases using pytest.
 - use pylint.
 - venv 
 - create a subset of the html element in another module and reuse it in the testcases.
 - achievement file.
 - requirement file.
 - use Pdoc3 to generate an html documentation for the code.
 
 - use case:
   - we have element called div that have two sub-element h1 and p should be rendered like this.
    ```
    <div>
      <h1></h1>
      <p></p>
    </div>
    ```
   - we need to render it with indentations, each level with adjusted indentation.



Side Task:
--

Level: Easy.

* Find the equation of encrypted/decrypted data.
* write a class that does the encryption/decryption ( optional )
```
  key = "yahyaAbbadi"

  real_data = hi, it is me, how are you? are you ok? can you speak?

  encrypted_data = ŚīüĒīöäĭĵèĿŗîðŚıùäĥĴĭòūıŅıâãĶĩâŁŁŧâĿŝā¢ħĥİèŋšķðťĲçĥįā

```


Required Files.
-- 
These files are required for all Future tasks as well.

* Unit-Testing ( pytest ).
* Achievement file.
* PyDoc3
* Pylint
* venv
* requirements.txt or Pipfile.lock
* __init__.py files
