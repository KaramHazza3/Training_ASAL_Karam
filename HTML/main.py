from html_element import HTMLElement, DuplicateIDError, InvalidElementName

def main():
    try:
        div1 = HTMLElement("div", [ HTMLElement("p", "mhmmad",{"id": "unique_id5"}), HTMLElement("p", "mhmmad",{"id": "unique_id6"}) ], {"id": "unique_id1", "name":"karam"})
        div2 = HTMLElement("div", [ HTMLElement("p", "ahhh",{"id": "unique_id12"}), HTMLElement("p", "ahh",{"id": "unique_id13"}) ], {"id": "unique_id2"}) 
        div3 = HTMLElement("div", "Content33", {"id": "unique_id3"}) 
        p = HTMLElement("p", "Hello world!", {"id": "unique_id4", "name":"karam"}) 
        HTMLElement.append(div2, p)
        HTMLElement.append(div1, div2)
        print(HTMLElement.render(div1))
        print("calling find elements by tag name")
        elements = HTMLElement.find_elements_by_tag(div1, "div")
        for elem in elements:
            print(elem.name, elem.attributes)
        print("calling find elements by attr")
        elements = HTMLElement.find_elements_by_attr(div1, "name", "karam")
        for elem in elements:
            print(elem.name, elem.attributes)
        HTMLElement.render_to_html_file(div1)
    except InvalidElementName as e:
        print(f"InvalidElementName error: {e}")
    except DuplicateIDError as e:
        print(f"DuplicateIDError error: {e}")
    except TypeError as e:
        print(f"TypeError error: {e}")

if __name__ == "__main__":
    main()
