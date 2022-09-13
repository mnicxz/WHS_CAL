import tkinter as tk
import logging,datetime

class TextboxHander(logging.Handler):
    def __init__(self, textbox):
        logging.Handler.__init__(self)
        self.textbox = textbox
        print(type(self.textbox))

    def emit(self, record):
        msg = self.format(record)
        self.textbox.insert('end',msg + '\n')

class App:
    def btn_command():
        now=datetime.datetime.now()
        log.info('*{}*'.format(now))
        pass

if __name__ =='__main__':
    root=tk.Tk()
    tk.Button(root,text="aaa",command=App.btn_command).pack()

    normalTextBox=tk.Text(root,width=50,height=5).pack()
    normalTextBox.pack()
    log=logging.getLogger('log')
    log.setLevel(logging.INFO)
    handler=TextboxHander(normalTextBox)
    log.addHandler(handler)
    root.mainloop()