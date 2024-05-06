from html_element import HTMLElement, DuplicateIDError, InvalidElementName


def main():
    try:
        # Sample HTML elements
        div1 = HTMLElement("div", [
            HTMLElement("p", "mhmmad", {"id": "unique_id5"}),
            HTMLElement("p", "mhmmad", {"id": "unique_id6"})
        ], {"id": "unique_id1", "name": "karam"})

        div2 = HTMLElement("div", [
            HTMLElement("p", "ahhh", {"id": "unique_id12"}),
            HTMLElement("p", "ahh", {"id": "unique_id13"})
        ], {"id": "unique_id2"})

        div3 = HTMLElement("div", "Content33", {"id": "unique_id3"})

        p = HTMLElement("p", "Hello world!", {"id": "unique_id4", "name": "karam"})

        h1 = HTMLElement("h1", "Hello", {"id": "unique_id3", "name": "karam"})

        # Append div3 to div2
        HTMLElement.append(div2, div3)

        # Append p to div3
        HTMLElement.append(div3, p)

        # Append div2 to div1
        HTMLElement.append(div1, div2)

        # Append h1 to div1
        # HTMLElement.append(div1, h1)

        # Render the HTML structure of div1
        print(HTMLElement.render(div1))

        # Calling find_elements_by_tag_name
        print("Calling find_elements_by_tag_name:")
        elements = HTMLElement.find_elements_by_tag(div1, "div")
        for elem in elements:
            print(elem.name, elem.attributes)

        # Calling find_elements_by_attr
        print("Calling find_elements_by_attr:")
        elements = HTMLElement.find_elements_by_attr(div1, "name", "karam")
        for elem in elements:
            print(elem.name, elem.attributes)

        # Render the HTML structure to an HTML file
        HTMLElement.render_to_html_file(div1)

    except InvalidElementName as e:
        print(f"InvalidElementName error: {e}")
    except DuplicateIDError as e:
        print(f"DuplicateIDError error: {e}")
    except TypeError as e:
        print(f"TypeError error: {e}")


if __name__ == "__main__":
    main()

