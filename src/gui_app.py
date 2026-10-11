import tkinter as tk
import os
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from logger import log
from avatars_manager import AvatarsManager


# ---------- Paleta ----------
BG_MAIN    = "#1e1e2e"
BG_PANEL   = "#2a2a3c"
BG_CARD    = "#313145"
BG_HOVER   = "#3d3d5c"
FG_TEXT    = "#e0e0f0"
FG_MUTED   = "#8a8aa8"
ACCENT     = "#7c5cff"
ACCENT_HOV = "#9b7fff"
DANGER     = "#ff5c7c"
DANGER_HOV = "#ff7d97"

# ---------- Placeholders padrão ----------
DEFAULT_AVATAR_NAME = "Novo Avatar"
DEFAULT_DIR         = str(Path.home() / "LukiTuber" / "avatars")


# =========================================================
#  Helpers: Entry com placeholder
# =========================================================
class PlaceholderEntry(tk.Entry):
    """Entry que mostra um texto cinza quando vazio."""

    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(parent, **kwargs)
        self.placeholder = placeholder
        self._is_placeholder = False
        self._apply_placeholder()
        self.bind("<FocusIn>",  self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def _apply_placeholder(self):
        self.insert(0, self.placeholder)
        self.configure(fg=FG_MUTED)
        self._is_placeholder = True

    def _on_focus_in(self, _):
        if self._is_placeholder:
            self.delete(0, "end")
            self.configure(fg=FG_TEXT)
            self._is_placeholder = False

    def _on_focus_out(self, _):
        if not self.get().strip():
            self._apply_placeholder()

    def get_value(self):
        """Retorna o valor real (ignora placeholder)."""
        return "" if self._is_placeholder else self.get().strip()

    def set_value(self, value):
        self.delete(0, "end")
        if value:
            self.insert(0, value)
            self.configure(fg=FG_TEXT)
            self._is_placeholder = False
        else:
            self._apply_placeholder()


# =========================================================
#  Diálogo base reutilizável
# =========================================================
class BaseDialog(tk.Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG_MAIN)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()          # modal
        self.result = None

        self.bind("<Escape>", lambda e: self._cancel())

    def _center_on(self, parent):
        self.update_idletasks()
        px, py = parent.winfo_rootx(), parent.winfo_rooty()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        w, h = self.winfo_width(), self.winfo_height()
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"+{max(x,0)}+{max(y,0)}")

    def _cancel(self):
        self.result = None
        self.destroy()


# =========================================================
#  Diálogo: Criar Avatar
# =========================================================
class CreateAvatarDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Criar Avatar")
        self._build()
        self._center_on(parent)
        self.wait_window()

    def _build(self):
        pad = {"padx": 20}
        tk.Label(self, text="Nome do Avatar",
                 bg=BG_MAIN, fg=FG_TEXT,
                 font=("Segoe UI", 10, "bold")
                 ).pack(anchor="w", pady=(20, 4), **pad)

        self.nome_entry = PlaceholderEntry(
            self, placeholder=DEFAULT_AVATAR_NAME,
            bg=BG_CARD, fg=FG_TEXT, insertbackground=FG_TEXT,
            relief="flat", font=("Segoe UI", 10), width=40,
        )
        self.nome_entry.pack(ipady=6, **pad)

        tk.Label(self, text="Diretório",
                 bg=BG_MAIN, fg=FG_TEXT,
                 font=("Segoe UI", 10, "bold")
                 ).pack(anchor="w", pady=(14, 4), **pad)

        dir_row = tk.Frame(self, bg=BG_MAIN)
        dir_row.pack(fill="x", **pad)

        self.dir_entry = PlaceholderEntry(
            dir_row, placeholder=DEFAULT_DIR,
            bg=BG_CARD, fg=FG_TEXT, insertbackground=FG_TEXT,
            relief="flat", font=("Segoe UI", 10),
        )
        self.dir_entry.pack(side="left", fill="x", expand=True, ipady=6)

        browse_btn = self._make_flat_button(dir_row, "📁", self._browse)
        browse_btn.pack(side="left", padx=(6, 0))

        # ---- Botões ----
        actions = tk.Frame(self, bg=BG_MAIN)
        actions.pack(fill="x", pady=20, **pad)

        self._make_flat_button(actions, "Cancelar", self._cancel)\
            .pack(side="right")
        self._make_primary_button(actions, "Criar", self._confirm)\
            .pack(side="right", padx=(0, 8))

        self.nome_entry.focus_set()

    def _browse(self):
        initial = self.dir_entry.get_value() or DEFAULT_DIR
        chosen = filedialog.askdirectory(
            parent=self, title="Escolha o diretório do avatar",
            initialdir=initial if Path(initial).exists() else str(Path.home()),
        )
        if chosen:
            self.dir_entry.set_value(chosen)

    def _confirm(self):
        nome = self.nome_entry.get_value() or DEFAULT_AVATAR_NAME
        diretorio = self.dir_entry.get_value() or DEFAULT_DIR
        self.result = {"name": nome, "path": diretorio}
        self.destroy()

    # -- helpers visuais --
    def _make_primary_button(self, parent, text, cmd):
        return self._styled_button(parent, text, cmd, ACCENT, ACCENT_HOV)

    def _make_flat_button(self, parent, text, cmd):
        return self._styled_button(parent, text, cmd, BG_CARD, BG_HOVER)

    def _styled_button(self, parent, text, cmd, bg, hover):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=bg, fg=FG_TEXT,
                      activebackground=hover, activeforeground=FG_TEXT,
                      relief="flat", bd=0, padx=14, pady=6,
                      font=("Segoe UI", 10, "bold"), cursor="hand2")
        b.bind("<Enter>", lambda e: b.configure(bg=hover))
        b.bind("<Leave>", lambda e: b.configure(bg=bg))
        return b


# =========================================================
#  Diálogo: Renomear Avatar
# =========================================================
class RenameAvatarDialog(BaseDialog):
    def __init__(self, parent, current_name):
        super().__init__(parent, "Renomear Avatar")
        self._current = current_name
        self._build()
        self._center_on(parent)
        self.wait_window()

    def _build(self):
        tk.Label(self, text="Novo nome",
                 bg=BG_MAIN, fg=FG_TEXT,
                 font=("Segoe UI", 10, "bold")
                 ).pack(anchor="w", padx=20, pady=(20, 4))

        self.entry = PlaceholderEntry(
            self, placeholder=self._current,
            bg=BG_CARD, fg=FG_TEXT, insertbackground=FG_TEXT,
            relief="flat", font=("Segoe UI", 10), width=36,
        )
        self.entry.pack(ipady=6, padx=20)
        self.entry.focus_set()
        self.entry.select_range(0, "end")

        actions = tk.Frame(self, bg=BG_MAIN)
        actions.pack(fill="x", padx=20, pady=20)

        tk.Button(actions, text="Cancelar", command=self._cancel,
                  bg=BG_CARD, fg=FG_TEXT, relief="flat", bd=0,
                  padx=14, pady=6, font=("Segoe UI", 10),
                  activebackground=BG_HOVER, activeforeground=FG_TEXT,
                  cursor="hand2").pack(side="right")

        tk.Button(actions, text="Salvar", command=self._confirm,
                  bg=ACCENT, fg=FG_TEXT, relief="flat", bd=0,
                  padx=14, pady=6, font=("Segoe UI", 10, "bold"),
                  activebackground=ACCENT_HOV, activeforeground=FG_TEXT,
                  cursor="hand2").pack(side="right", padx=(0, 8))

    def _confirm(self):
        nome = self.entry.get_value() or self._current
        self.result = nome
        self.destroy()


# =========================================================
#  Aplicação principal
# =========================================================
class GUIApp:
    def __init__(self, width, height):
        self.window = tk.Tk()
        self.avatars_manager = AvatarsManager()

        log.info("Inicializando LukiTuber - GUI...")
        self.window.title("LukiTuber - GUI")
        self.window.geometry(f"{width}x{height}")
        self.window.configure(bg=BG_MAIN)
        self.window.minsize(500, 400)

        self._setup_styles()
        self._build_ui()
        self._load_avatars()

    # ---------- Estilos ----------
    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Vertical.TScrollbar",
                        background=BG_PANEL, troughcolor=BG_MAIN,
                        bordercolor=BG_MAIN, arrowcolor=FG_MUTED)

    # ---------- UI ----------
    def _build_ui(self):
        log.info("Criando elementos da Janela...")

        # Header
        header = tk.Frame(self.window, bg=BG_PANEL, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="🎬  LukiTuber", bg=BG_PANEL, fg=FG_TEXT,
                 font=("Segoe UI", 16, "bold")).pack(side="left", padx=20)
        tk.Label(header, text="Gerenciador de Avatars", bg=BG_PANEL,
                 fg=FG_MUTED, font=("Segoe UI", 10)).pack(side="left")

        # Corpo
        body = tk.Frame(self.window, bg=BG_MAIN)
        body.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(body, bg=BG_PANEL, width=180)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        self.create_avatar_btn = self._make_button(
            sidebar, text="＋  Criar Avatar",
            command=self._on_create_avatar, primary=True,
        )
        self.create_avatar_btn.pack(fill="x", padx=15, pady=(20, 10))

        # Conteúdo
        content = tk.Frame(body, bg=BG_MAIN)
        content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        tk.Label(content, text="Seus Avatars", bg=BG_MAIN, fg=FG_TEXT,
                 font=("Segoe UI", 13, "bold"), anchor="w"
                 ).pack(fill="x", pady=(0, 10))

        self.list_container = self._make_scrollable_area(content)

    # ---------- Helpers de layout ----------
    def _make_button(self, parent, text, command, primary=False):
        bg = ACCENT if primary else BG_CARD
        hover = ACCENT_HOV if primary else BG_HOVER
        btn = tk.Button(parent, text=text, command=command,
                        bg=bg, fg=FG_TEXT,
                        activebackground=hover, activeforeground=FG_TEXT,
                        font=("Segoe UI", 10, "bold" if primary else "normal"),
                        relief="flat", bd=0, padx=12, pady=8, cursor="hand2")
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
        return btn

    def _make_scrollable_area(self, parent):
        wrapper = tk.Frame(parent, bg=BG_MAIN)
        wrapper.pack(fill="both", expand=True)

        canvas = tk.Canvas(wrapper, bg=BG_MAIN, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        inner = tk.Frame(canvas, bg=BG_MAIN)
        canvas.create_window((0, 0), window=inner, anchor="nw")

        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(canvas.find_all()[0], width=e.width))

        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-e.delta / 120), "units"))
        return inner

    # ---------- Cards ----------
    def _make_avatar_card(self, parent, avatar):
        selecionado = (self.avatars_manager.settings.selected_avatar
                    == avatar.name)

        # cores mudam se estiver selecionado
        card_bg  = BG_HOVER if selecionado else BG_CARD
        icon_bg  = ACCENT if selecionado else BG_HOVER
        name_fg  = FG_TEXT
        border   = ACCENT if selecionado else card_bg

        card = tk.Frame(parent, bg=card_bg, cursor="hand2",
                        highlightthickness=2 if selecionado else 0,
                        highlightbackground=border,
                        highlightcolor=border)
        card.pack(fill="x", pady=6)

        icon = tk.Label(card,
                        text=avatar.name[:1].upper() if avatar.name else "?",
                        bg=icon_bg, fg=FG_TEXT,
                        font=("Segoe UI", 14, "bold"),
                        width=3, height=1)
        icon.pack(side="left", padx=(12, 12), pady=10)

        nome = tk.Label(card, text=avatar.name, bg=card_bg, fg=name_fg,
                        font=("Segoe UI", 11, "bold" if selecionado else "normal"),
                        anchor="w")
        nome.pack(side="left", fill="x", expand=True)

        # à direita: badge "ativo" ou o menu "⋮"
        if selecionado:
            seta = tk.Label(card, text="✓ ativo", bg=card_bg, fg=ACCENT,
                            font=("Segoe UI", 10, "bold"))
        else:
            seta = tk.Label(card, text="⋮", bg=card_bg, fg=FG_MUTED,
                            font=("Segoe UI", 14))
        seta.pack(side="right", padx=15)

        widgets = (card, icon, nome, seta)

        def on_enter(_):
            for w in widgets:
                # não muda a cor do card selecionado
                if not selecionado or w is not card:
                    w.configure(bg=BG_HOVER)

        def on_leave(_):
            for w in widgets:
                w.configure(bg=card_bg)
            # restaura ícone e card se estiver selecionado
            if selecionado:
                icon.configure(bg=icon_bg)
                card.configure(bg=BG_HOVER)

        for w in widgets:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>",
                lambda e, a=avatar, c=card: self._show_avatar_menu(e, a, c))
            w.bind("<Button-3>",
                lambda e, a=avatar, c=card: self._show_avatar_menu(e, a, c))

        return card

    def _show_avatar_menu(self, event, avatar, card):
        """Menu de contexto do avatar."""
        menu = tk.Menu(self.window, tearoff=0,
                    bg=BG_PANEL, fg=FG_TEXT,
                    activebackground=ACCENT, activeforeground=FG_TEXT,
                    bd=0, font=("Segoe UI", 10))

        ja_selecionado = (self.avatars_manager.settings.selected_avatar
                        == avatar.name)

        menu.add_command(
            label="✓  Selecionado" if ja_selecionado else "◯  Selecionar",
            command=(None if ja_selecionado
                    else lambda: self._on_select_avatar(avatar)),
            state=("disabled" if ja_selecionado else "normal"),
        )
        menu.add_separator()
        menu.add_command(label="✏️  Renomear",
                        command=lambda: self._on_rename_avatar(avatar, card))
        menu.add_separator()
        menu.add_command(label="🗑️  Apagar",
                        command=lambda: self._on_delete_avatar(avatar, card))

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    # ---------- Carregamento ----------
    def _load_avatars(self):
        for child in self.list_container.winfo_children():
            child.destroy()

        self.avatars_manager.load_avatars()

        avatars = self.avatars_manager.avatars
        selecionado = self.avatars_manager.settings.selected_avatar

        # selecionado primeiro, resto em ordem alfabética
        avatars_ordenados = sorted(
            avatars,
            key=lambda a: (a.name != selecionado, a.name.lower())
        )

        if avatars_ordenados:
            for avatar in avatars_ordenados:
                self._make_avatar_card(self.list_container, avatar)
        else:
            self._show_empty_state()

    def _show_empty_state(self):
        empty = tk.Frame(self.list_container, bg=BG_MAIN)
        empty.pack(fill="both", expand=True, pady=40)

        tk.Label(empty, text="🎭", bg=BG_MAIN, fg=FG_MUTED,
                 font=("Segoe UI", 32)).pack()
        tk.Label(empty, text="Nenhum avatar ainda", bg=BG_MAIN, fg=FG_TEXT,
                 font=("Segoe UI", 12, "bold")).pack(pady=(10, 4))
        tk.Label(empty, text="Clique em “Criar Avatar” para começar",
                 bg=BG_MAIN, fg=FG_MUTED, font=("Segoe UI", 10)).pack()

    # ---------- Ações ----------
    def _on_select_avatar(self, avatar):
        try:
            self.avatars_manager.select_avatar(avatar.name)
            self._load_avatars()   # redesenha pra mostrar o destaque
        except Exception as e:
            log.exception("Falha ao selecionar avatar")
            messagebox.showerror("Erro", f"Não foi possível selecionar:\n{e}",
                                parent=self.window)
            
    def _on_create_avatar(self):
        dlg = CreateAvatarDialog(self.window)
        if not dlg.result:
            return

        nome = dlg.result["name"]
        base_dir = dlg.result["path"]

        # ⚠️ a pasta DO avatar é base + nome
        avatar_dir = os.path.join(base_dir, nome)
        avatar_dir_formated = avatar_dir_formated = "avatars" + avatar_dir.split("avatars", 1)[1]
        avatar_dir_formated = avatar_dir_formated.replace("\\", "/")

        self.avatars_manager.create_avatar(nome, avatar_dir_formated)
        self.avatars_manager.save_avatars()
        self._load_avatars()


    def _on_rename_avatar(self, avatar, card):
        dlg = RenameAvatarDialog(self.window, avatar.name)
        if not dlg.result or dlg.result == avatar.name:
            return
        try:
            self.avatars_manager.rename_avatar(avatar, dlg.result)
            self.avatars_manager.save_avatars()   # ✅ SALVA
            self._load_avatars()
        except Exception as e:
            log.exception("Falha ao renomear avatar")
            messagebox.showerror("Erro", f"Não foi possível renomear:\n{e}",
                                parent=self.window)


    def _on_delete_avatar(self, avatar, card):
        confirm = messagebox.askyesno(
            "Apagar avatar",
            f"Tem certeza que deseja apagar '{avatar.name}'?\n\n"
            "A pasta do avatar NÃO será apagada.",
            parent=self.window, icon="warning",
        )
        if not confirm:
            return
        try:
            self.avatars_manager.delete_avatar(avatar, delete_files=False)
            self.avatars_manager.save_avatars()   # ✅ SALVA
            self._load_avatars()
        except Exception as e:
            log.exception("Falha ao apagar avatar")
            messagebox.showerror("Erro", f"Não foi possível apagar:\n{e}",
                                parent=self.window)

    def run(self):
        self.window.mainloop()


def main():
    app = GUIApp(700, 600)
    app.run()


if __name__ == "__main__":
    main()