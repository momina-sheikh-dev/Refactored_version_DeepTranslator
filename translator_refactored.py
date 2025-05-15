from googletrans import Translator
from gtts import gTTS
from tkinter import *
from PIL import Image, ImageTk
import os
import uuid

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 280
LANGUAGES = {
    "English": "en",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Urdu": "ur"
}

FONT_ENTRY = ('Arial', 23, 'bold')
FONT_LABEL = ('Arial', 22, 'bold')
FONT_OPTION = ('Arial', 15, 'bold')
FONT_BUTTON = ('Arial', 20, 'bold')


class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Translator')
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.config(bg='black')

        self.click_option = StringVar()
        self.click_option.set('Select language')

        self.setup_ui()

    def setup_ui(self):
        """Initialize all GUI components"""
        try:
            bg_image = Image.open("bg.jpg")
            bg_image = bg_image.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.Resampling.LANCZOS)
            self.bg = ImageTk.PhotoImage(bg_image)
            bg_label = Label(self.root, image=self.bg)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("Could not load background image:", e)
            Label(self.root, text="No background image", fg="white", bg="black", font=('Arial', 16)).place(x=13, y=10)

        self.text_entry = Entry(self.root, bg='white', fg='black', font=FONT_ENTRY)
        self.text_entry.place(x=17, y=20, width=350)

        OptionMenu(self.root, self.click_option, *LANGUAGES.keys()).place(x=390, y=20)

        self.output_label = Label(self.root, text='Translated Text', bg='black', fg='white',
                                  font=FONT_LABEL, wraplength=560, justify='center')
        self.output_label.place(x=20, y=100)

        Button(self.root, text='Translate', bg='#1b03a3', fg='white', font=FONT_BUTTON,
               command=self.convert_language).place(x=220, y=200)

    def convert_language(self):
        """Controller for the translation and TTS process"""
        text = self.text_entry.get()
        selected_lang = self.click_option.get()

        if not self.validate_input(text, selected_lang):
            return

        try:
            translated_text = self.translate_text(text, selected_lang)
            self.output_label.config(text=translated_text)
            self.generate_audio(translated_text, selected_lang)
            self.log_translation(text, translated_text, selected_lang)
        except Exception as e:
            self.output_label.config(text=f"Error: {str(e)}")

    def validate_input(self, text, language):
        """Validate that input text and language are provided"""
        if not text.strip() or language == "Select language":
            self.output_label.config(text="Please enter text and select a language")
            return False
        return True

    def translate_text(self, text, language):
        """Translate text using googletrans"""
        translator = Translator()
        lang_code = LANGUAGES[language]
        return translator.translate(text, dest=lang_code).text

    def generate_audio(self, text, language):
        """Generate and play audio of translated text"""
        filename = f"translated_audio_{uuid.uuid4()}.mp3"
        speech = gTTS(text=text, slow=False, lang=LANGUAGES[language])
        speech.save(filename)
        os.system(f'start {filename}')  # For Windows

    def log_translation(self, original, translated, language):
        """Log translation to file"""
        with open('translator.txt', 'a', encoding='utf-8') as file:
            file.write(f"User entered: {original}\n")
            file.write(f"Translated to {language}: {translated}\n\n")


if __name__ == '__main__':
    root = Tk()
    app = TranslatorApp(root)
    root.mainloop()
