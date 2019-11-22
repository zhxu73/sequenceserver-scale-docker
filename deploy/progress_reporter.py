#!/usr/bin/env python

import os
import sys
import uuid

html_path = "/var/www/html/index.html"

html_header = (
    "<!doctype html>"
    "<html lang=\"en\">"
    "<head>"
    "<meta charset=\"utf-8\">"
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">"
    "<link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css\" integrity=\"sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T\" crossorigin=\"anonymous\">"

    "<title>config progress</title>"
    "</head>\n"
    "<body>\n"
    "<div class=\"container\">"
    "<h1>Instance Initializing...</h1>\n"
    "<div class=\"row\">"
    "<div class=\"col-sm\">"
    "<ul class=\"list-group\">\n"
    )
html_placeholder_1="<!-- PLACEHOLDER 1 -->\n"
html_placeholder_2="<!-- PLACEHOLDER 2 -->\n"
html_placeholder_3="<!-- PLACEHOLDER 3 -->\n"
html_footer = (
    "</ul></div>\n<div class=\"col-sm\"><!-- PLACEHOLDER 2 -->\n</div>\n</div></div>"
    "<script src=\"https://code.jquery.com/jquery-3.3.1.slim.min.js\" integrity=\"sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo\" crossorigin=\"anonymous\"></script>\n"
    "<script src=\"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js\" integrity=\"sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1\" crossorigin=\"anonymous\"></script>\n"
    "<script src=\"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js\" integrity=\"sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM\" crossorigin=\"anonymous\"></script>\n"
    "</body></html>"
    )
collapse_header = ("<div class=\"collapse multi-collapse\" id=\"collapse_id\">"
                "<div class=\"card card-body\">")
collapse_footer = ("</div></div>")

def main():
    html = ""
    try:
        with open(html_path, "r") as f:
            html = f.read()
    except FileNotFoundError:
        create_index_page()
        with open(html_path, "r") as f:
            html = f.read()

    detail = ""
    if len(sys.argv) == 1:
        return
    elif len(sys.argv) == 2:
        tag = "p"
        text = sys.argv[1]
    elif len(sys.argv) == 3:
        tag = sys.argv[1]
        text = sys.argv[2]
    elif len(sys.argv) >= 4:
        tag = sys.argv[1]
        text = sys.argv[2]
        detail = sys.argv[3]

    text = replace_newline_with_br(text)
    detail = replace_newline_with_br(detail)
    insert_paragraph(html, tag, text, detail)

def read_index_page():
    html = ""
    try:
        with open(html_path, "r") as f:
            html = f.read()
    except FileNotFoundError:
        create_index_page()
        with open(html_path, "r") as f:
            html = f.read()
    return html

def create_index_page():
    with open(html_path, "w+") as f :
        f.write(html_header)
        f.write(html_placeholder_1)
        f.write(html_footer)

def insert_paragraph(html, tag, text, detail):
    if html.find(html_placeholder_1) == -1:
        create_index_page()
        print("Cannot find place holder, recreate the page")
        html = read_index_page()
    collapse_id = ""
    collapse_button_html = ""
    if len(detail) > 0:
        collapse_id = "coll" + str(uuid.uuid1())
        collapse_button_html = "<a class=\"btn btn-light border text-right\" type=\"button\" data-toggle=\"collapse\" data-target=\"#" + collapse_id + "\" aria-expanded=\"false\" aria-controls=\"" + collapse_id + "\">Detail</a>"
    tag_header = '<' + tag + '>'
    tag_footer = "</" + tag + '>'
    inner_text = "<li class=\"list-group-item\">" + "<div class=\"row\"><div class=\"col-9\">" + tag_header + text + tag_footer + "</div><div class=\"col\">" + collapse_button_html + "</div></div>" + "</li>"
    html = html.replace(html_placeholder_1, inner_text + "\n" + html_placeholder_1)
    print(inner_text)
    # if detail is provided, add a card to PLACEHOLDER 2
    if len(detail) > 0:
        detail = "<p>" + detail + "</p>"
        inner_text = collapse_header.replace("collapse_id", collapse_id) + detail + html_placeholder_3 + collapse_footer
        html = html.replace(html_placeholder_2, inner_text + "\n" + html_placeholder_2)
    with open(html_path, "w+") as f :
        f.write(html)

def replace_newline_with_br(content):
    return content.replace("\\n", "<br>")

def append_detail(html, detail):
    if html.rfind(html_placeholder_3) == -1:
        return
    detail = replace_newline_with_br(detail)
    detail = "<p>" + detail + "</p>"
    r_html_placeholder_3 = ''.join(reversed(html_placeholder_3))
    r_detail = ''.join(reversed(detail))
    r_html = ''.join(reversed(html))
    r_html = r_html.replace(r_html_placeholder_3, r_html_placeholder_3 + r_detail)
    html = ''.join(reversed(r_html))
    with open(html_path, "w+") as f :
        f.write(html)

if __name__== "__main__":
    main()

