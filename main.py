import urllib.request
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import webbrowser

class CodeIPTV(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.toutes_les_chaines = []  # Stocke la liste complète des chaînes [(nom, url), ...]

        # Titre de l'application
        self.add_widget(Label(
            text="⚡ NEXUS IPTV MOBILE", 
            font_size=24, 
            size_hint_y=None, 
            height=40, 
            color=(0.4, 0.4, 1, 1)
        ))

        # Zone de saisie du lien M3U
        self.url_input = TextInput(
            text="https://iptv-org.github.io/iptv/countries/fr.m3u",
            multiline=False,
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.url_input)

        # Bouton pour charger la playlist
        btn_charger = Button(
            text="CHARGER LA PLAYLIST", 
            size_hint_y=None, 
            height=50, 
            background_color=(0.3, 0.3, 0.9, 1)
        )
        btn_charger.bind(on_press=self.charger_playlist)
        self.add_widget(btn_charger)

        # Barre de recherche (masquée au début, s'active une fois chargé)
        self.search_input = TextInput(
            hint_text="Rechercher une chaîne...",
            multiline=False,
            size_hint_y=None,
            height=45,
            disabled=True
        )
        self.search_input.bind(text=self.filtrer_chaines)
        self.add_widget(self.search_input)

        # Statut de l'application
        self.lbl_status = Label(text="Entrez une URL et cliquez sur Charger.", size_hint_y=None, height=40)
        self.add_widget(self.lbl_status)

        # Zone de défilement (Scroll) pour la liste des chaînes
        self.scroll = ScrollView()
        self.liste_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.liste_layout.bind(minimum_height=self.liste_layout.setter('height'))
        self.scroll.add_widget(self.liste_layout)
        self.add_widget(self.scroll)

    def charger_playlist(self, instance):
        url = self.url_input.text.strip()
        self.lbl_status.text = "Téléchargement en cours..."
        self.liste_layout.clear_widgets()
        self.toutes_les_chaines = []

        try:
            # Simulation d'un navigateur pour éviter les blocages de sécurité des serveurs M3U
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                lignes = response.read().decode('utf-8').splitlines()

            nom_chaine = ""
            for ligne in lignes:
                ligne = ligne.strip()
                if ligne.startswith("#EXTINF"):
                    # On extrait le nom de la chaîne situé après la dernière virgule
                    nom_chaine = ligne.split(",")[-1].strip()
                elif ligne.startswith("http") and nom_chaine:
                    self.toutes_les_chaines.append((nom_chaine, ligne))
                    nom_chaine = ""

            # Activer la barre de recherche et afficher le résultat
            self.search_input.disabled = False
            self.lbl_status.text = f"Succès : {len(self.toutes_les_chaines)} chaînes chargées !"
            self.afficher_liste(self.toutes_les_chaines)

        except Exception as e:
            self.lbl_status.text = "Erreur : Impossible de charger ou lire l'URL"
            self.search_input.disabled = True

    def afficher_liste(self, liste_chaines):
        """Vide l'écran et recrée les boutons pour les chaînes de la liste fournie"""
        self.liste_layout.clear_widgets()
        
        for nom, lien in liste_chaines:
            item_box = BoxLayout(orientation='vertical', size_hint_y=None, height=75, spacing=2)
            
            # Nom de la chaîne
            lbl = Label(text=nom, font_size=16, halign='left', valign='middle')
            lbl.bind(size=lbl.setter('text_size')) # Permet le bon centrage du texte
            
            # Bouton de lecture
            btn_flux = Button(
                text="▶ Lancer la chaîne", 
                size_hint_y=None, 
                height=35, 
                background_color=(0.2, 0.7, 0.2, 1)
            )
            # Liaison du bouton pour ouvrir le lien vidéo dans le lecteur par défaut du téléphone
            btn_flux.bind(on_press=lambda inst, link=lien: webbrowser.open(link))
            
            item_box.add_widget(lbl)
            item_box.add_widget(btn_flux)
            self.liste_layout.add_widget(item_box)

    def filtrer_chaines(self, instance, texte_recherche):
        """Filtre la liste en temps réel selon la saisie de l'utilisateur"""
        texte = texte_recherche.lower().strip()
        if not texte:
            self.afficher_liste(self.toutes_les_chaines)
            return

        resultats = [c for c in self.toutes_les_chaines if texte in c[0].lower()]
        self.afficher_liste(resultats)


class NexusApp(App):
    def build(self):
        return CodeIPTV()

if __name__ == '__main__':
    NexusApp().run()
