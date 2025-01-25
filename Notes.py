import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import font, messagebox, simpledialog


class NoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestionnaire de Notes")
        self.geometry("500x600")
        self.configure(bg='black')
        self.create_database()
        self.create_widgets()

    def create_database(self):
        # Création ou connexion à la base de données SQLite
        self.conn = sqlite3.connect("notes.db")
        self.cursor = self.conn.cursor()
        # Création de la table notes si elle n'existe pas
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS notes
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             title TEXT,
                             content TEXT,
                             created_at TIMESTAMP)''')
        self.conn.commit()

    def create_widgets(self):
        # Configuration des polices
        title_font = font.Font(family="Helvetica", size=14, weight="bold")
        button_font = font.Font(family="Helvetica", size=10, weight="bold")

        # Champ de titre
        tk.Label(self, text="Titre:", bg='black', fg='red', font=title_font).pack(pady=5)
        self.title_entry = tk.Entry(self, width=50, bg='black', fg='red', insertbackground='red')
        self.title_entry.pack()

        # Champ de contenu
        tk.Label(self, text="Contenu:", bg='black', fg='red', font=title_font).pack(pady=5)
        self.content_text = tk.Text(self, height=10, width=50, bg='black', fg='red', insertbackground='red')
        self.content_text.pack()

        # Boutons
        button_frame = tk.Frame(self, bg='black')
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Ajouter Note", command=self.add_note, bg='red', fg='black', font=button_font).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Voir Notes", command=self.view_notes, bg='red', fg='black', font=button_font).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Supprimer Note", command=self.delete_note, bg='red', fg='black', font=button_font).pack(side=tk.LEFT, padx=5)

        # Liste des notes
        tk.Label(self, text="Notes existantes:", bg='black', fg='red', font=title_font).pack(pady=5)
        self.notes_listbox = tk.Listbox(self, width=60, height=10, bg='black', fg='red')
        self.notes_listbox.pack(pady=10)
        self.update_notes_list()

    def add_note(self):
        # Récupération du titre et du contenu
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()
        if title and content:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Insertion de la nouvelle note dans la base de données
            self.cursor.execute("INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)",
                                (title, content, created_at))
            self.conn.commit()
            messagebox.showinfo("Succès", "Note ajoutée avec succès!")
            # Nettoyage des champs
            self.title_entry.delete(0, tk.END)
            self.content_text.delete("1.0", tk.END)
            self.update_notes_list()
        else:
            messagebox.showerror("Erreur", "Le titre et le contenu sont requis!")

    def view_notes(self):
        selected = self.notes_listbox.curselection()
        if selected:
            note_id = self.notes_listbox.get(selected[0]).split(":")[0]
            # Récupération de la note sélectionnée
            self.cursor.execute("SELECT title, content FROM notes WHERE id=?", (note_id,))
            note = self.cursor.fetchone()
            if note:
                # Affichage de la note dans une nouvelle fenêtre
                view_window = tk.Toplevel(self)
                view_window.title(note[0])
                view_window.geometry("400x300")
                view_window.configure(bg='black')
                tk.Label(view_window, text=note[1], wraplength=380, bg='black', fg='red', justify=tk.LEFT).pack(padx=10, pady=10)
        else:
            messagebox.showinfo("Info", "Veuillez sélectionner une note à afficher.")

    def delete_note(self):
        selected = self.notes_listbox.curselection()
        if selected:
            note_id = self.notes_listbox.get(selected[0]).split(":")[0]
            if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette note?"):
                # Suppression de la note de la base de données
                self.cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
                self.conn.commit()
                messagebox.showinfo("Succès", "Note supprimée avec succès!")
                self.update_notes_list()
        else:
            messagebox.showinfo("Info", "Veuillez sélectionner une note à supprimer.")

    def update_notes_list(self):
        # Mise à jour de la liste des notes affichées
        self.notes_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT id, title FROM notes ORDER BY created_at DESC")
        for note in self.cursor.fetchall():
            self.notes_listbox.insert(tk.END, f"{note[0]}: {note[1]}")

if __name__ == "__main__":
    app = NoteApp()
    app.mainloop()
