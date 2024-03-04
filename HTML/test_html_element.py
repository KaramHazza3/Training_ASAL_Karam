import pytest
import os
from html_element import HTMLElement, InvalidElementName, DuplicateIDError
from html_element_samples import div1,div2,div3,p

@pytest.fixture
def expected_output():
    return ("<div id=\"unique_id2\">\n"
        "\tContent22\n"
        "</div>\n")


def test_html_element_init():
    assert div1.name == "div"
    assert div1.value == "Content"
    assert div1.attributes == {"id": "unique_id1", "name":"karam"}
    assert div1.children == []

def test_html_element_init_with_invalid_name():
    with pytest.raises(InvalidElementName):
         HTMLElement("ahmad", "content", {"id": "my_div"})

def test_html_element_append():
    assert len(div1.children) == 0
    HTMLElement.append(div1,div2)
    assert len(div1.children) == 1

def test_html_element_append_same_ids():
    with pytest.raises(DuplicateIDError):
        HTMLElement.append(div2, HTMLElement("div", "content1", {"id": "unique_id2"}))

def test_html_element_render_success(expected_output):
    result = HTMLElement.render(div2)
    assert result.strip() == expected_output.strip()

def test_html_element_render_failure(expected_output):
    result = HTMLElement.render(div3)
    assert result.strip() != expected_output.strip()

def test_html_element_find_by_valid_attr():
    elements = HTMLElement.find_elements_by_attr(div1, "name", "karam")
    assert len(elements) == 1

def test_html_element_find_by_valid_attr_with_append():
    HTMLElement.append(div2,p)
    elements = HTMLElement.find_elements_by_attr(div1, "name", "karam")
    assert len(elements) == 2

def test_html_element_find_by_invalid_attr():
    elements = HTMLElement.find_elements_by_attr(div1, "color", "black")
    assert len(elements) == 0

def test_html_element_find_by_valid_tag():
    elements = HTMLElement.find_elements_by_tag(div1, "div")
    assert len(elements) == 2

def test_html_element_find_by_not_exist_tag():
    elements = HTMLElement.find_elements_by_tag(div1, "h1")
    assert len(elements) == 0

def test_html_element_render_invalid_element_to_html_file():
    with pytest.raises(DuplicateIDError):
        HTMLElement.append(div2, HTMLElement("div", "Content22", {"id": "unique_id2"}))
        HTMLElement.render_to_html_file(div2)
    output_file_path = os.path.join(os.getcwd(), 'output.html')
    assert not os.path.exists(output_file_path)

def test_html_element_render_to_html_file():
    HTMLElement.render_to_html_file(div1)
    output_file_path = os.path.join(os.getcwd(), 'output.html')
    assert os.path.exists(output_file_path), "output.html file does not exist"
    assert os.path.getsize(output_file_path) > 0, "output.html file is empty"
