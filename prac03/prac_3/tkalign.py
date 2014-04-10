
import Tkinter as tk


class AlignmentFrame(tk.Frame):
  
    def __init__(self, parent, alignment, description = "alignment"):
        tk.Frame.__init__(self, parent)   
         
        self.parent = parent
        self.alignment = alignment
        self.description = description        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Alignment")

        self.pack(fill=tk.BOTH, expand=1)
        self.var = tk.IntVar()

        seqFrame = tk.Frame(self)
        seqFrame.pack()
        row = 0
        gap_count = 0
        for sequence in self.alignment.seqs:
            nameLabel = tk.Label(seqFrame, text=sequence.name)
            nameLabel.place(x=50, y=50)
            nameLabel.grid(row=row, column=0)
            symbolCol = 0
            for symbol in sequence:
                if symbol == '-':
                    bgColour = "red"
                    gap_count += 1
                elif symbol == 'M':
                    bgColour = "green"
                else:
                    bgColour = "white"
                symbolCol += 1
                symbolLabel = tk.Label(seqFrame, text=symbol, bg=bgColour)
                symbolLabel.grid(row=row, column=symbolCol)
            row += 1
        summary = self.description + "; penalty=" + str(self.alignment.gap_penalty) + ". " + str(gap_count) + " gaps."
        summaryLabel = tk.Label(seqFrame, text=summary, fg="blue")
        summaryLabel.grid(row=row, column=0, columnspan=40, sticky=tk.W)

    def onClick(self):
       
        if self.var.get() == 1:
            self.master.title("Checkbutton")
        else:
            self.master.title("")


def main():
  
    root = tk.Tk()
    root.geometry("250x150+300+300")
    app = AlignmentFrame(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  