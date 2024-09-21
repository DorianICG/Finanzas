import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkcalendar import DateEntry
from backend.operations import run_operations, update_operations, show_all_businesses
from src.data_loader import load_excel  # Ajuste aquí


def create_gui():
    root = tk.Tk()
    root.title("Finanzas")
    root.configure(background="#f0f0f0")

    def show_menu():
        for widget in root.winfo_children():
            widget.destroy()

        ttk.Label(
            root, text="Seleccione una opción:", background="#f0f0f0", anchor="center"
        ).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(root, text="Agregar acción", command=show_add_action).grid(
            row=1, column=0, columnspan=2, pady=5
        )
        ttk.Button(root, text="Actualizar acción", command=show_update_action).grid(
            row=2, column=0, columnspan=2, pady=5
        )
        ttk.Button(
            root, text="Mostrar todas las acciones", command=show_all_businesses_action
        ).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(root, text="Cargar archivo Excel", command=load_excel_action).grid(
            row=4, column=0, columnspan=2, pady=5
        )

    def show_add_action():
        for widget in root.winfo_children():
            widget.destroy()

        ttk.Label(root, text="Ticker:", background="#f0f0f0", anchor="center").grid(
            row=0, column=0, padx=10, pady=5
        )
        ttk.Label(
            root, text="Fecha de inicio:", background="#f0f0f0", anchor="center"
        ).grid(row=1, column=0, padx=10, pady=5)
        ttk.Label(
            root, text="Fecha de fin:", background="#f0f0f0", anchor="center"
        ).grid(row=2, column=0, padx=10, pady=5)

        ticker_entry = ttk.Entry(root, justify="center")
        start_date_entry = DateEntry(root, date_pattern="yyyy-mm-dd", justify="center")
        end_date_entry = DateEntry(root, date_pattern="yyyy-mm-dd", justify="center")

        ticker_entry.grid(row=0, column=1, padx=10, pady=5)
        start_date_entry.grid(row=1, column=1, padx=10, pady=5)
        end_date_entry.grid(row=2, column=1, padx=10, pady=5)

        def on_submit():
            ticker = ticker_entry.get().upper()
            start_date = start_date_entry.get_date().strftime("%Y-%m-%d")
            end_date = end_date_entry.get_date().strftime("%Y-%m-%d")
            result = run_operations(ticker, start_date, end_date)
            messagebox.showinfo("Resultado", result)

        submit_button = ttk.Button(root, text="Ejecutar", command=on_submit)
        submit_button.grid(row=3, column=0, columnspan=2, pady=10)

        back_button = ttk.Button(root, text="Volver", command=show_menu)
        back_button.grid(row=4, column=0, columnspan=2, pady=10)

    def show_update_action():
        for widget in root.winfo_children():
            widget.destroy()

        ttk.Label(root, text="Ticker:", background="#f0f0f0", anchor="center").grid(
            row=0, column=0, padx=10, pady=5
        )

        ticker_entry = ttk.Entry(root, justify="center")
        ticker_entry.grid(row=0, column=1, padx=10, pady=5)

        def on_submit():
            ticker = ticker_entry.get().upper()
            result = update_operations(ticker)
            messagebox.showinfo("Resultado", result)

        submit_button = ttk.Button(root, text="Ejecutar", command=on_submit)
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

        back_button = ttk.Button(root, text="Volver", command=show_menu)
        back_button.grid(row=2, column=0, columnspan=2, pady=10)

    def show_all_businesses_action():
        businesses = show_all_businesses()
        messagebox.showinfo("Acciones", "\n".join(businesses))

    def load_excel_action():
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                load_excel(file_path)
                messagebox.showinfo(
                    "Éxito", "Archivo cargado y procesado correctamente."
                )
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {e}")

    show_menu()
    root.mainloop()


if __name__ == "__main__":
    create_gui()
