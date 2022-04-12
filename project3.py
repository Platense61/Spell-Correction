import tkinter as tk

"""This function grabs all text in editor upon clicking the get text button and outputs to command line"""
def retrieve_input():
    inputValue=txt_edit.get("1.0","end-1c")
    print(inputValue)


window = tk.Tk()
window.title("Text Editor")

window.rowconfigure(0,minsize=900,weight=1)
window.columnconfigure(1, minsize=900, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window)
#btn_open = tk.Button(fr_buttons, text="Open")
btn_save = tk.Button(fr_buttons, text="Get Text", command=retrieve_input)

#btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=10)
fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()