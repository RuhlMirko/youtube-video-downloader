import re
from functools import partial
from kivy.uix.dropdown import DropDown
from pytube import YouTube
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
Window.size = (500, 600)


class MyApp(MDApp):
    def getLinkInfo(self, event, layout):
        self.titleLabel.text = ""
        self.titleLabel.pos_hint = {'center_x': 0.5, 'center_y': .40}

        if self.linkInput.text == "":
            self.titleLabel.text = "Invalid link"
        else:
            self.link = self.linkInput.text
            self.checkLink = re.match("^https://www.youtube.com/.*", self.link)
            print(self.checkLink)

            if (self.checkLink):
                try:
                    self.yt = YouTube(self.link)

                    self.titleLabel.text = "Title: " + self.yt.title
                    self.viewsLabel.text = "Views: " + str(self.yt.views)
                    self.lengthLabel.text = "Lenght: " + str(self.yt.length)

                    self.downloadButton.pos_hint = {'center_x': 0.5, 'center_y': .20}

                    self.video = self.yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
                    print(self.video)

                    self.dropDown = DropDown()
                    for video in self.video:
                        btn = Button(text=video.resolution, size_hint=(None, None), height=30)
                        btn.bind(on_release=lambda btn: self.dropDown.select(btn.text))
                        self.dropDown.add_widget(btn)

                    self.mainButton = Button(text="Resolution", size_hint=(None, None), pos=(350, 90), height=50)
                    self.mainButton.bind(on_release=self.dropDown.open)
                    self.dropDown.bind(on_select=lambda instance, x: setattr(self.mainButton, 'text', x))
                    layout.add_widget(self.mainButton)

                    print("Title: " + self.yt.title)
                    print("Views: " + str(self.yt.views))
                    print("Lenght: " + str(self.yt.length))
                except:
                    self.titleLabel.text = "Error"
                    self.titleLabel.pos_hint = {'center_x': 0.5, 'center_y': .40}
            else:
                self.titleLabel.text = "Invalid link"

    def download(self, event, window):
        self.ys = self.yt.streams.filter(file_extension='mp4').filter(resolution=self.mainButton.text).first()
        print("Download started")
        self.ys.download('./videos')
        print("Download complete")

    def build(self):
        layout = MDRelativeLayout(md_bg_color=[210 / 255, 215 / 255, 217 / 255])
        self.img = Image(source='Youtube_Logo.png',
                         size_hint=(.5, .5),
                         pos_hint={'center_x': .5, 'center_y': 0.85}
                         )

        self.youtubeLink = Label(text="Enter youtube link",
                                 size_hint=(.5, .5),
                                 pos_hint={'center_x': 0.5, 'center_y': .70},
                                 font_size=20, color=(1, 0, 0),
                                 font_name="Segoeuil"
                                 )

        self.linkInput = TextInput(text="",
                                   hint_text="Youtube link",
                                   size_hint=(0.9, None),
                                   pos_hint={'center_x': 0.5, 'center_y': .60},
                                   height=48, font_size=20, foreground_color=(.5, .5, .5),
                                   font_name="Lucon",
                                   )

        self.linkButton = Button(text="Get video info",
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                 size_hint=(.3, .1),
                                 font_name="Segoeuil",
                                 font_size=20,
                                 background_color=[1, 0.5, 0.5]
                                 )

        self.linkButton.bind(on_press=partial(self.getLinkInfo, layout))

        self.titleLabel = Label(text="",
                                size_hint=(.5, .5),
                                pos_hint={'center_x': 0.5, 'center_y': .40},
                                font_size=20, color=(0, 0, 0),
                                font_name="Segoeuil"
                                )

        self.viewsLabel = Label(text="",
                                size_hint=(.5, .5),
                                pos_hint={'center_x': 0.5, 'center_y': .35},
                                font_size=20, color=(0, 0, 0),
                                font_name="Segoeuil"
                                )

        self.lengthLabel = Label(text="",
                                 size_hint=(.5, .5),
                                 pos_hint={'center_x': 0.5, 'center_y': .30},
                                 font_size=20, color=(0, 0, 0),
                                 font_name="Segoeuil"
                                 )

        self.downloadButton = Button(text="Download video",
                                     pos_hint={'center_x': 0.5, 'center_y': 20},
                                     size_hint=(.3, .1),
                                     size=(75, 75),
                                     font_name="Segoeuil",
                                     font_size=20,
                                     background_color=[1, 0, 0]
                                     )
        self.downloadButton.bind(on_press=partial(self.download, layout))

        layout.add_widget(self.img)
        layout.add_widget(self.youtubeLink)
        layout.add_widget(self.linkInput)
        layout.add_widget(self.linkButton)
        layout.add_widget(self.titleLabel)
        layout.add_widget(self.viewsLabel)
        layout.add_widget(self.lengthLabel)
        layout.add_widget(self.downloadButton)
        return layout

if __name__ == "__main__":
    MyApp().run()
