import tkinter as tk


def main():
    window = tk.Tk()
    window.title("Text Editor")

    window_w = 900
    window_h = 600

    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    center_x = int(screen_w/2 - window_w/2)
    center_y = int(screen_h/2 - window_h/2)

    # centers the window
    window.geometry(f'{window_w}x{window_h}+{center_x}+{center_y}')

    window.rowconfigure(0,minsize=900,weight=1)
    window.columnconfigure(1, minsize=900, weight=1)

    txt_edit = tk.Text(window)
    fr_buttons = tk.Frame(window)
    #btn_open = tk.Button(fr_buttons, text="Open")
    btn_save = tk.Button(fr_buttons, text="Get Text", command= lambda: retrieve_input(txt_edit))

    #btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=10)
    fr_buttons.grid(row=0, column=0, sticky="ns")
    txt_edit.grid(row=0, column=1, sticky="nsew")

    window.mainloop()


"""This function grabs all text in editor upon clicking the get text button and outputs to command line"""
def retrieve_input(txt_edit):
    inputValue=txt_edit.get("1.0","end-1c")
    #Following replace lines remove punctuations from the words. Useful for when we do operations on words.
    inputValue = inputValue.replace("!","")
    inputValue = inputValue.replace("?","")
    inputValue = inputValue.replace(".","")
    inputValue = inputValue.replace(",","")
    my_split = inputValue.split()
    print(my_split)
    print(inputValue)


if __name__ == "__main__":
    main()