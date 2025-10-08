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
    
    self.create_widgets()

def main() -> None:
  pass

if __name__ == "__main__":
  main()