import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from lxml import etree

BG_COLOR = "#f4f6f8"
PRIMARY = "#2c7be5"
SUCCESS = "#28a745"
ERROR = "#dc3545"
TEXT_COLOR = "#333"

def browse_xml():
    path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
    xml_entry.delete(0, tk.END)
    xml_entry.insert(0, path)


def browse_xsd():
    path = filedialog.askopenfilename(filetypes=[("XSD Files", "*.xsd")])
    xsd_entry.delete(0, tk.END)
    xsd_entry.insert(0, path)


def validate_xml():
    xml_path = xml_entry.get().strip()
    xsd_path = xsd_entry.get().strip()

    result_text.delete(1.0, tk.END)
    status_label.config(text="", fg=TEXT_COLOR)

    if not xml_path or not xsd_path:
        messagebox.showerror("Error", "Please select both XML and XSD files.")
        return

    try:
        with open(xsd_path, "rb") as xsd_file:
            xsd_doc = etree.parse(xsd_file)
            xmlschema = etree.XMLSchema(xsd_doc)

        parser = etree.XMLParser(schema=xmlschema)

        for event, element in etree.iterparse(
            xml_path,
            events=("end",),
        ):
            element.clear()  # free memory

        status_label.config(text="✔ Валидацията мина успешно", fg=SUCCESS)

    except etree.XMLSyntaxError as e:
        status_label.config(text="✖ Валидацията се провали", fg=ERROR)
        result_text.insert(tk.END, str(e))

    except Exception as e:
        messagebox.showerror("Exception", str(e))
    xml_path = xml_entry.get().strip()
    xsd_path = xsd_entry.get().strip()

    result_text.delete(1.0, tk.END)
    status_label.config(text="", fg=TEXT_COLOR)

    if not xml_path or not xsd_path:
        messagebox.showerror("Error", "Please select both XML and XSD files.")
        return

    try:
        with open(xml_path, "rb") as xml_file, open(xsd_path, "rb") as xsd_file:
            xml_doc = etree.parse(xml_file)
            xsd_doc = etree.parse(xsd_file)

        xmlschema = etree.XMLSchema(xsd_doc)

        if xmlschema.validate(xml_doc):
            status_label.config(text="✔Валидацията мина успешно", fg=SUCCESS)
        else:
            status_label.config(text="✖ Валидацията се провали", fg=ERROR)
            for error in xmlschema.error_log:
                result_text.insert(
                    tk.END,
                    f"Line {error.line}, Column {error.column}: {error.message}\n"
                )

    except Exception as e:
        messagebox.showerror("Exception", str(e))


root = tk.Tk()
root.title("Smart XML Validator")
root.geometry("600x400")
root.configure(bg=BG_COLOR)

default_font = ("Segoe UI", 10)
title_font = ("Segoe UI", 16, "bold")

title_label = tk.Label(
    root,
    text="Smart XML Validator",
    font=title_font,
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
title_label.pack(pady=15)

container = tk.Frame(root, bg=BG_COLOR)
container.pack(fill="x", padx=30)

tk.Label(container, text="XML File", bg=BG_COLOR, font=default_font).grid(row=0, column=0, sticky="w")

xml_entry = tk.Entry(container, font=default_font)
xml_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 15))

xml_button = tk.Button(
    container,
    text="Browse",
    command=browse_xml,
    bg=PRIMARY,
    fg="white",
    relief="flat",
    padx=15
)
xml_button.grid(row=1, column=1, pady=(0, 15))

tk.Label(container, text="XSD Schema", bg=BG_COLOR, font=default_font).grid(row=2, column=0, sticky="w")

xsd_entry = tk.Entry(container, font=default_font)
xsd_entry.grid(row=3, column=0, sticky="ew", padx=(0, 10), pady=(0, 20))

xsd_button = tk.Button(
    container,
    text="Browse",
    command=browse_xsd,
    bg=PRIMARY,
    fg="white",
    relief="flat",
    padx=15
)
xsd_button.grid(row=3, column=1, pady=(0, 20))

container.columnconfigure(0, weight=1)

validate_button = tk.Button(
    root,
    text="Validate",
    command=validate_xml,
    bg=PRIMARY,
    fg="white",
    font=("Segoe UI", 11, "bold"),
    relief="flat",
    padx=20,
    pady=8
)
validate_button.pack(pady=5)

status_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 12, "bold"),
    bg=BG_COLOR
)
status_label.pack(pady=5)

result_text = scrolledtext.ScrolledText(
    root,
    font=("Consolas", 9),
    height=10
)
result_text.pack(fill="both", expand=True, padx=30, pady=15)
root.mainloop()


def __init__():
    print()