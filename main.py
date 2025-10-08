import customtkinter as CT
import os

class KalkulatorGUI(CT.CTk):
  # class kalkulator
  
  def __init__(self):
    # fungsi inisialisasi class kalkulator
    # untuk persiapan data awal 
    super().__init__()
    
    # set geometri, judul, icon
    self.geometry("400x600")
    self.title("Kalkulator GUI")
    self.resizable(False, False)
    if os.path.exists("kalkulatorGUI.ico"):
      self.iconbitmap("kalkulatorGUI.ico")
    
    # set warna
    CT.set_appearance_mode("dark")
    self.bg_color = "#121212"
    self.button_color = "#1e1e1e"
    self.accent_color = "#4fd1c5"
    self.configure(fg_color=self.bg_color)
    
    # ekspresi matematika awal dan font awal
    self.ekspresi_matematika = "0"
    self.ukuran_font = 64
  
  def buat_tombol(self):
    
    # frame tampilan utama -> (bagian atas kalkulator)
    frame_tampilan = CT.CTkFrame(self, fg_color=self.bg_color)
    frame_tampilan.pack(fill="x", padx=20, pady=(40, 10))
    
    # tanda [ = ] -> (di bagian tampilan)
    tanda_samaDengan = CT.CTkLabel(frame_tampilan, text="=",
                       font=("Arial", 45), text_color=self.accent_color)
    tanda_samaDengan.pack(side="left", padx=(0, 10))
    
    # tampilan hasil
    self.hasil = CT.CTkEntry(frame_tampilan, font=("Arial", 64),
                             fg_color=self.bg_color, text_color="white",
                             border_width=0, justify="right")
    # jadiin read-only -> (cuma buat nampilin)
    self.hasil.pack(fill="x", expand=True)
    self.hasil.insert(0, "0")
    self.hasil.configure(state="readonly")

def main() -> None:
  app = KalkulatorGUI()
  app.mainloop()

if __name__ == "__main__":
  main()