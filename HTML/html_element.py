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
    valid_tags: List[str] = ["div", "p", "span", "h1", "h2", "h3", "h4", "h5"]

    def __init__(self, name: str, value: Union['HTMLElement', Iterable], attributes: Dict[str, str]):

        self.unique_ids: set[str] = set()
        self.name = self.validate_name(name)
        self.value = list(self.validate_value(value))
        self.attributes = self.validate_attributes(attributes)
        self.parent: Union[HTMLElement, None] = None

        if "id" in self.attributes:
            self.unique_ids.add(self.attributes["id"])

        self.append_to_value(value)

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
        if name.lower() not in HTMLElement.valid_tags:
            raise InvalidElementName(f"Invalid HTML element name: {name}")
        return name.lower()

    @staticmethod
    def validate_value(value: Union['HTMLElement', Iterable]) -> []:
        """
    Validates the given HTML element value.

    Args:
        value (Union['HTMLElement'Iterable]): The value to validate.

    Returns:
        An empty array to append there [].

    Raises:
        TypeError: If the value is not of the correct type.
    """
        if not isinstance(value, (HTMLElement, Iterable)):
            raise TypeError("Invalid value type")
        if isinstance(value, Iterable) and not isinstance(value, str):
            for item in value:
                if not isinstance(item, HTMLElement):
                    raise TypeError("Invalid value type in the list. Must be HTML element.")
        return []

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
        return attributes

    def append_to_value(self, value: Union['HTMLElement', Iterable]):
        if isinstance(value, str):
            self.value.append(value)
        if isinstance(value, HTMLElement):
            self.add_child(child=value)
        if isinstance(value, Iterable):
            for val in value:
                if isinstance(val, HTMLElement):
                    self.add_child(child=val)

    def add_child(self, child: 'HTMLElement') -> None:
        """
                Add the provided HTML element to the current HTML element.

                Args:
                    child ('HTMLElement'): The HTML element to be added.
                """
        if not self.is_id_duplication(elem=child):

            child.parent = self
            self.value.append(child)
            self.unique_ids.update(child.unique_ids)

            ancestor = self.parent

            while ancestor:
                result = ancestor.unique_ids.intersection(child.unique_ids)
                if len(result) > 0:
                    raise DuplicateIDError(f"ID '{result.pop()}' is already exists")
                ancestor.unique_ids.update(child.unique_ids)
                ancestor = ancestor.parent

    def is_id_duplication(self, elem: 'HTMLElement') -> bool:
        """
        Checks for duplication of the 'id' attribute among HTML element instances.

        Args:
            elem (HTMLElement): The HTML element to check against.

        Returns:
            bool: True if the 'id' attribute is duplicated, False otherwise.

        Raises:
            DuplicateIDError: If the 'id' attribute is found to be duplicated.
        """
        if len(elem.unique_ids) > 1:
            result = self.unique_ids.intersection(elem.unique_ids)
            if len(result) > 0:
                raise DuplicateIDError(f"ID '{result.pop()}' is already exists")

        else:
            existing_id: str = elem.attributes.get("id")
            if existing_id and existing_id in self.unique_ids:
                raise DuplicateIDError(f"ID '{existing_id}' is already exists")

        return False

    @classmethod
    def append(cls, parent_element: 'HTMLElement',
               child_element: Union['HTMLElement', List['HTMLElement']]) -> None:
        """
        Appends HTML element/elements as a child to another HTML element.

        Args:
            cls: The class itself (HTMLElement).
            parent_element ('HTMLElement'): The parent HTML element to which
                the child element will be appended.
            child_element ('HTMLElement'): The child HTML element/elements to append.

        Returns:
           None.
        """
        parent_element.append_to_value(child_element)

    @classmethod
    def render(cls, element: 'HTMLElement', indent_level: int = 0, space_level: int = 1) -> str:
        """
        Renders the HTML representation of the given HTML element and its children.

       Args:
        cls: The class itself (HTMLElement).
        element ('HTMLElement'): The HTML element to render.
        indent_level (int, optional): The indentation level for formatting the output.
        space_level (int, optional): The level of indentation for spacing between tags.

        Returns:
            str: The HTML representation of the element and its children.
        """
        result: str = ""
        indent = '\t' * indent_level
        space = '\t' * space_level
        opening_tag = f'<{element.name}'

        for key, value in element.attributes.items():
            opening_tag += f' {key}="{value}"'
        opening_tag += '>\n'

        element_value = ''.join(item for item in element.value if isinstance(item, str))

        result += f'{indent}{opening_tag}{space}{element_value}\n'

        for child in element.value:
            if isinstance(child, HTMLElement):
                result += cls.render(child, indent_level + 1, space_level + 1)

        closing_tag = f'{indent}</{element.name}>'
        result += closing_tag + '\n'
        return result

    @classmethod
    def find_elements(cls, element: 'HTMLElement', **kwargs) -> List['HTMLElement']:
        """
        Finds HTML elements based on the specified criteria.

        Args:
            element ('HTMLElement'): The HTML element to start the search from.
            **kwargs: Keyword arguments representing the search criteria. Supported criteria:
                    - attr (str): The attribute to search for.
                    - attr_value (str): The value of the attribute to search for.
                    - tag_name (str): The tag name to search for.

        Returns:
            List['HTMLElement']: A list of HTML elements that match the search criteria.
        """
        elements: List['HTMLElement'] = []

        attr = kwargs.get('attr')
        attr_value = kwargs.get('attr_value')
        tag_name = kwargs.get('tag_name')

        if attr and attr_value:
            for key, value in element.attributes.items():
                if key == attr and attr_value == value:
                    elements.append(element)

        elif tag_name and HTMLElement.validate_name(tag_name) and element.name == tag_name:
            elements.append(element)

            for child in element.value:
                if isinstance(child, HTMLElement):
                    elements.extend(child.find_elements(child, **kwargs))
        return elements

    @classmethod
    def find_elements_by_attr(cls, element: 'HTMLElement',
                              attr: str, attr_value: str
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
        return cls.find_elements(element, attr=attr, attr_value=attr_value)

    @classmethod
    def find_elements_by_tag(cls, element: 'HTMLElement', tag_name: str) -> List['HTMLElement']:
        """
    Finds HTML elements with the specified tag name starting from the given element.

    Args:
        element ('HTMLElement'): The HTML element to start the search from.
        tag_name (str): The tag name to search for.

    Returns:
        List['HTMLElement']: A list of HTML elements with the specified tag name.
    """
        return cls.find_elements(element, tag_name=tag_name)

    @classmethod
    def render_to_html_file(cls, element: 'HTMLElement') -> None:
        """
    Renders the given HTML element and its children to an HTML file.

    Args:
        element ('HTMLElement'): The root HTML element to render.

    Returns:
        None
    """
        with open("output.html", 'w', encoding='utf-8') as html_file:
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
