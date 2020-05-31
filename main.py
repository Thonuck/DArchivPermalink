import tkinter as tk
import requests
import re

class PermalinkExtractor():
    def __init__(self, master):
        self.master = master
        self.clipboard_content = tk.StringVar(value="empty_clipboard")
        self.perma_link = tk.StringVar(value="")
        tk.Label(self.master, text="Detected Clipboard:").grid(row=0, column=0, sticky="w")
        tk.Label(self.master, textvariable=self.clipboard_content, width=100, anchor="w", relief="sunken").grid(row=0, column=1, sticky="w")
        tk.Label(self.master, text="Permalink:").grid(row=1, column=0, sticky="w")
        tk.Label(self.master, textvariable=self.perma_link, width=100, anchor="w", relief="sunken").grid(row=1, column=1, sticky="w")
        self.check_clipboard()

    def check_clipboard(self):
        try:
            current_clipboard = self.master.clipboard_get()
            self.clipboard_content.set(current_clipboard)
            if not current_clipboard == self.perma_link.get():
                if current_clipboard.startswith("http"):
                    self.check_link(current_clipboard)
        except tk.TclError:
            pass

        self.master.after(1000, self.check_clipboard)

    def check_link(self, cb_link):

        self.perma_link.set("processing...")

        response = requests.get(cb_link)
        data = response.text
        print(data)

        mm = re.search("include/permalink.php\?f=([0-9-]+)", data)
        print(mm)
        if mm:
            print(mm.groups())
            if mm.groups():
                new_link = "http://www.landesarchiv-bw.de/plink/?f={}".format(mm.groups()[0])
                self.master.clipboard_clear()
                self.master.clipboard_append(new_link)
                self.master.update()
                self.perma_link.set(new_link)



def main():
    root = tk.Tk()
    root.title("D-Archiv Permalink Translator")
    PermalinkExtractor(root)
    root.mainloop()

if __name__ == "__main__":
    main()