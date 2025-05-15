from googletrans import Translator
from gtts import gTTS
from tkinter import *
from PIL import Image, ImageTk
import os
import uuid

# Create main window
root = Tk()
root.title('Translator')
root.geometry('600x280')
root.config(bg='black')

# ========== Background Image Setup ==========
try:
    bg_image = Image.open("bg.jpg")  # Ensure bg.jpg is in the same folder
    bg_image = bg_image.resize((600, 280), Image.Resampling.LANCZOS)  # Resize to fit window
    my_bg = ImageTk.PhotoImage(bg_image)
    label_1 = Label(root, image=my_bg)
    label_1.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print("Could not load background image:", e)
    label_1 = Label(root, text="No background image", fg="white", bg="black", font=('Arial', 16))
    label_1.place(x=13, y=10)

# ========== Entry Widget ==========
e1 = Entry(root, bg='white', fg='black', font=('Arial', 23, 'bold'))
e1.place(x=17, y=20, width=350)

# ========== Translate Function ==========
def convert_language():
    text_to_translate = e1.get()
    translator = Translator()
    selected_language = click_option.get()

    if not text_to_translate.strip() or selected_language == "Select language":
        label_2.config(text="Please enter text and select a language")
        return

    # Language code map
    lang_map = {
        "English": "en",
        "German": "de",
        "French": "fr",
        "Spanish": "es",
        "Urdu": "ur"
    }

    lang_code = lang_map.get(selected_language)
    
    try:
        translated = translator.translate(text_to_translate, dest=lang_code).text
        label_2.config(text=translated)

        # Save & play audio with a unique filename
        filename = f"translated_audio_{uuid.uuid4()}.mp3"
        speech = gTTS(text=translated, slow=False, lang=lang_code)
        speech.save(filename)
        os.system(f'start {filename}')  # For Windows

        # Save to log file
        with open('translator.txt', 'a', encoding='utf-8') as file:
            file.write(f"User entered: {text_to_translate}\n")
            file.write(f"Translated to {selected_language}: {translated}\n\n")

    except Exception as e:
        label_2.config(text=f"Error: {str(e)}")

# ========== Language Dropdown ==========
choices = ['English', 'German', 'French', 'Spanish', 'Urdu']
click_option = StringVar()
click_option.set('Select language')

list_drop = OptionMenu(root, click_option, *choices)
list_drop.configure(background='black', foreground='white', font=('Arial', 15, 'bold'))
list_drop.place(x=390, y=20)

# ========== Output Label ==========
label_2 = Label(root, text='Translated Text', bg='black', fg='white', font=('Arial', 22, 'bold'), wraplength=560, justify='center')
label_2.place(x=20, y=100)

# ========== Translate Button ==========
Button_1 = Button(root, text='Translate', bg='#1b03a3', fg='white', font=('Arial', 20, 'bold'), command=convert_language)
Button_1.place(x=220, y=200)

# Start GUI
root.mainloop()
