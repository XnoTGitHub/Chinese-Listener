import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.config import Config  
from kivy.uix.checkbox import CheckBox 
from kivy.uix.screenmanager import ScreenManager, Screen

################################################################
is_debug_mode = 0
################################################################

if(is_debug_mode):
	from google_speech import Speech
else:
	from plyer import tts

import csv
import random

ExludedList = [1] * 20

class Phrase:

	def __init__(self, Chapter_Numb, Chapter_Name, Chinese_Phrase, English_Translations, Chapter_is_active = 1):
		self.Chapter_is_active = Chapter_is_active
		self.Chapter_Numb = Chapter_Numb
		self.Chapter_Name = Chapter_Name
		self.Chinese_Phrase = Chinese_Phrase
		self.English_Translations = English_Translations

class MainWindow(Screen):

	First = 0

	PhraseList = []
	Phrase_Current = Phrase(0,"Default","你好","Hello")

	#ExludedList = np.ones(20)

	NumberOfTrials = 0;
	
	answer = ObjectProperty(None)
	message = ObjectProperty(None)
	button = ObjectProperty(None)

	def load_data(self):
		self.First = 1
		self.NumberOfTrials = 3
		print("Load Phrases..")
		ChapterNumber = -1
		ChapterName = "test"
		self.PhraseList = []
		with open('PhraseFile.csv', newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter='|', quotechar='|')
			for row in spamreader:
				if(row[0][0] == '$'):
					#chapter beginning
					ChapterNumber = ChapterNumber + 1
					ChapterName = row[0][1:].split(',')[0]
					print(ChapterNumber," ",ChapterName)
					continue
				elif(row[0][0] == '*'):
					#this is a commentline
					continue
				words = row[0].split(',')
				#if(not ChapterNumber in self.ExludedList):
				if(ExludedList[ChapterNumber]):
					self.PhraseList.append(Phrase(Chapter_Numb = ChapterNumber,Chapter_Name = ChapterName, Chinese_Phrase = words[0], English_Translations = words[1:]))

		self.Phrase_Current = random.choice(self.PhraseList)
		self.text = self.Phrase_Current.Chinese_Phrase
		print(self.text)
		print(self.Phrase_Current.English_Translations)
		print(ExludedList)
		self.speak()


	def btn(self):
		if(not self.First):
			self.button.text = "Submit"
			self.load_data()
			self.answer.text = ""

		else:
			print("Your Answer:", self.answer.text)
			print("NumberOfTrials: ", self.NumberOfTrials)
			#self.answer.text = ""
			if(self.NumberOfTrials>=0):
				if( self.answer.text.lower() and self.answer.text.lower() in [ElementofenP.lower() for ElementofenP in self.Phrase_Current.English_Translations[:-1]]):
					self.message.text = "true!"
					print("true!")
					self.First = 0
					self.button.text = "Next Game"
					
				elif(not self.answer.text):
					self.message.text = "listen again! You still have " + str(self.NumberOfTrials+1) + " tries.."

					self.NumberOfTrials = self.NumberOfTrials - 1

					self.speak()

				else:
					print(self.answer.text.lower())
					print([ElementofenP.lower() for ElementofenP in self.Phrase_Current.English_Translations])
					self.message.text = "try again! You still have " + str(self.NumberOfTrials+1) + " tries.."

					if(self.button.text == "Submit"):
						print("Submit vs ", self.button.text)

						self.NumberOfTrials = self.NumberOfTrials - 1
						self.button.text = "Listen again"
						print("Submit vs ", self.button.text)
					else:
						print("listen again vs ",self.button.text)
						self.button.text = "Submit"
						self.speak()
			else: 
				self.message.text = str(self.Phrase_Current.English_Translations)
				self.button.text = "Next Chance"
				
				self.First = 0

	def speak(self):
		print("speech: ",self.text)
		if(is_debug_mode):
			lang = "zh-cn"
			self.speech = Speech(self.text, lang)
			self.speech.play()
		else:
			tts.speak(self.text)


class SecondWindow(Screen):
	
	def checkbox_click(self, instance, ident, value):
		if value is True:
			print(" ",ident, " Checked")
			ExludedList[ident] = 1
 
		else:
			print(" ",ident, " Unhecked")
			ExludedList[ident] = 0


class WindowManager(ScreenManager):
	pass


kv = Builder.load_file("my.kv")


class MyMainApp(App):
	def build(self):
		return kv


if __name__ == "__main__":
	MyMainApp().run()