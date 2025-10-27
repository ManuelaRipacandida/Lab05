import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio



FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)

    # TODO
    input_marca = ft.TextField( label="Marca")
    input_modello = ft.TextField( label="Modello")
    input_anno = ft.TextField(label="Anno")
    txt_n_posti = ft.TextField(
        width=60,
        value="0",
        text_align=ft.TextAlign.CENTER,
        border_color="green",
        disabled=True
    )
    txt_output = ft.Text(value="", size=16, color="green")

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO



    def aggiungi_automobile(e):
        marca=input_marca.value
        modello=input_modello.value
        anno=input_anno.value
        n_posti=txt_n_posti.value
        #mostra un errore se il valore inserito non è numerico
        if not anno.isdigit():
            alert.show_alert("❌Errore: il campo 'Anno' deve essere un numero!")
            return
        try:
            autonoleggio.aggiungi_automobile(marca, modello, anno, n_posti) #uso la funzione aggiungi_automobile()
            txt_output.value = f"✅ Auto aggiunta: {marca} {modello} ({anno}, {n_posti} posti)"
            # pulisci i campi
            input_marca.value = ""
            input_modello.value = ""
            input_anno.value = ""
            txt_n_posti.value = 0
            aggiorna_lista_auto()
        except Exception as ex:
            txt_output.value = f"❌ Errore: {ex}"

        page.update()

    def handle_add(e):
            current_val = int(txt_n_posti.value)
            txt_n_posti.value = str(current_val + 1)
            txt_n_posti.update()

    def handle_remove(e):
            current_val = int(txt_n_posti.value)
            txt_n_posti.value = str(current_val - 1)
            txt_n_posti.update()






    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)



    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    btn_minus = ft.IconButton(icon=ft.Icons.REMOVE, icon_color="red",
                              icon_size=24, on_click=handle_remove)
    btn_add = ft.IconButton(icon=ft.Icons.ADD,
                            icon_color="green",
                            icon_size=24, on_click=handle_add)
    pulsante_aggiungi_automobile = ft.ElevatedButton("Aggiungi automobile", on_click=aggiungi_automobile)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Text("Aggiungi nuova automobile", size=20),
        ft.Row(spacing=100,controls=[input_marca,input_modello,input_anno,btn_minus,txt_n_posti,btn_add],alignment=ft.MainAxisAlignment.CENTER),
        pulsante_aggiungi_automobile,

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
