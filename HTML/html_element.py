"""
This module contains the definition of the HTMLElement class
 and related functionality for handling HTML elements.
"""
from typing import Union, List, Dict, Iterable

class HTMLElement:
    """
    Represents an HTML element with a name, value, and attributes.
    This class provides functionality for creating and manipulating HTML elements.
    """
    unique_ids: set[int] = set()

    def __init__(self, name: str, value: Union['HTMLElement', str,
                                                List['HTMLElement']], attributes: Dict[str, str]):
        self.name: str = self.validate_name(name)
        self.value: Union['HTMLElement', str, List['HTMLElement']] = self.validate_value(value)
        self.attributes: Dict[str, str] = self.validate_attributes(attributes)
        self.children: List['HTMLElement'] = []

        if "id" in self.attributes:
            HTMLElement.unique_ids.add(self.attributes["id"])

    @staticmethod
    def validate_name(name: str) -> str:
        """
    Validates the given HTML element name.

    Args:
        name (str): The name of the HTML element to validate.

    Returns:
        str: The validated HTML element name.

    Raises:
        InvalidElementName: If the name is not a valid HTML element name.
    """
        valid_tags: List[str] = ["div", "p", "span", "h1", "h2", "h3", "h4", "h5"]
        if name.lower() not in valid_tags:
            raise InvalidElementName(f"Invalid HTML element name: {name}")
        return name.lower()
    @staticmethod
    def validate_value(value: Union['HTMLElement',
                                     Iterable]
                                     ) -> Union['HTMLElement', Iterable]:
        """
    Validates the given HTML element value.

    Args:
        value (Union['HTMLElement'Iterable]): The value to validate.

    Returns:
        Union['HTMLElement'Iterable]: The validated value.

    Raises:
        TypeError: If the value is not of the correct type.
    """
        if not isinstance(value, (HTMLElement,Iterable)):
            raise TypeError("Invalid value type")
        if isinstance(value,str):
            return value
        if isinstance(value,Iterable):
            for item in value:
                if not isinstance(item, HTMLElement):
                    raise TypeError("Invalid value type in the list. Must be HTML element.")
        return value
    @staticmethod
    def validate_attributes(attributes: Dict[str, str]) -> Dict[str, str]:
        """
    Validates the given HTML element attributes.

    Args:
        attributes (Dict[str, str]): The attributes to validate.

    Returns:
        Dict[str, str]: The validated attributes.

    Raises:
        TypeError: If the attributes are not of the correct type.
    """
        if not isinstance(attributes, dict):
            raise TypeError("attributes must be a dictionary")
        if not HTMLElement.is_id_duplication(attributes):
            return attributes
        return attributes
    @staticmethod
    def is_id_duplication(attributes: Dict[str,str], children: List['HTMLElement']=None) -> bool:
        """
    Checks for duplication of the 'id' attribute among HTML element instances and children.

    Args:
        attributes (Dict[str, str]): The attributes of the HTML element to check.
        children (List['HTMLElement'], optional): The list of children HTML
        elements to check. Default is None.

    Returns:
        bool: True if the 'id' attribute is duplicated, False otherwise.

    Raises:
        DuplicateIDError: If the 'id' attribute is found to be duplicated.
    """
        existing_id = attributes["id"]
        if existing_id in HTMLElement.unique_ids:
            raise DuplicateIDError(f"ID '{existing_id}' is already exists")
        if children:
            for child in children:
                if child.attributes.get("id") in HTMLElement.unique_ids:
                    raise DuplicateIDError(f"ID '{existing_id}' is already exists")
        return False
    @classmethod
    def append(cls, element: 'HTMLElement', element2: 'HTMLElement')->None:
        """
    Appends an HTML element as a child to another HTML element.

    Args:
        cls: The class itself (HTMLElement).
        element ('HTMLElement'): The parent HTML element to which
        the child element will be appended.
        element2 ('HTMLElement'): The child HTML element to append.

    Returns:
        bool: True if the child element was successfully appended, False otherwise.
    """
        if not element.children:
            element.children.append(element2)
            return
        if not HTMLElement.is_id_duplication(element.attributes, element.children):
            element.children.append(element2)
    @classmethod
    def render(cls, element: 'HTMLElement', indent_level: int=0) -> str:
        """
    Renders the HTML representation of the given HTML element and its children.

    Args:
        cls: The class itself (HTMLElement).
        element ('HTMLElement'): The HTML element to render.
        indent_level (int): The indentation level for formatting the output.

    Returns:
        None
    """
        result: str = ""
        indent = '\t' * indent_level
        opening_tag = f'<{element.name}'
        for key, value in element.attributes.items():
            opening_tag += f' {key}="{value}"'
        opening_tag += '>\n'
        result+=f'{indent}{opening_tag}\t\t{element.value}\n'
        if element.children:
            for child in element.children:
                result+=cls.render(child, indent_level + 1)
        closing_tag = f'{indent}</{element.name}>'
        result+=closing_tag + '\n'
        return result
    @classmethod
    def find_elements_by_attr(cls,element: 'HTMLElement',
                               attr: str,attr_value: str
                               ) -> List['HTMLElement']:
        """
    Finds HTML elements with the specified attribute and value.

    Args:
        element ('HTMLElement'): The HTML element to start the search from.
        attr (str): The attribute to search for.
        attr_value (str): The value of the attribute to search for.

    Returns:
        List['HTMLElement']: A list of HTML elements with the specified attribute and value.
    """
        elements: List['HTMLElement'] = []
        for key, value in element.attributes.items():
            if key == attr and attr_value == value:
                elements.append(element)
        if element.children:
            for child in element.children:
                elements.extend(child.find_elements_by_attr(child, attr, attr_value))
        return elements
    @classmethod
    def find_elements_by_tag(cls,element: 'HTMLElement', tag_name: str) -> List['HTMLElement']:
        """
    Finds HTML elements with the specified tag name starting from the given element.

    Args:
        element ('HTMLElement'): The HTML element to start the search from.
        tag_name (str): The tag name to search for.

    Returns:
        List['HTMLElement']: A list of HTML elements with the specified tag name.
    """
        elements: List['HTMLElement'] = []
        if HTMLElement.validate_name(tag_name) and element.name == tag_name:
            elements.append(element)
        if element.children:
            for child in element.children:
                elements.extend(child.find_elements_by_tag(child, tag_name))
        return elements
    @classmethod
    def render_to_html_file(cls, element: 'HTMLElement') -> None:
        """
    Renders the given HTML element and its children to an HTML file.

    Args:
        element ('HTMLElement'): The root HTML element to render.

    Returns:
        None
    """
        with open("output.html", 'w',encoding='utf-8') as html_file:
            html_file.write("<!DOCTYPE html>\n")
            html_file.write(cls.render(element))
class InvalidElementName(Exception):
    """
    Exception raised when an invalid HTML element name is encountered.
    """

class DuplicateIDError(Exception):
    """
    Exception raised when a duplicate ID attribute is encountered among HTML elements.
    """
