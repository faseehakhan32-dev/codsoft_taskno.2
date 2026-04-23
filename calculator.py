import customtkinter as ctk
import tkinter as tk
from typing import Optional, Dict

# --- Design Tokens ---
COLORS = {
    "bg_primary": "#141B2D",
    "bg_card": "#1D2A3D",
    "bg_input": "#2D3E50",
    "bg_input_focus": "#374B5F",
    "text_primary": "#FFF5D6",
    "text_secondary": "#829A9C",
    "text_muted": "#4E6070",
    "accent_steel": "#5E727A",
    "accent_teal": "#829A9C",
    "accent_error": "#EF4444",
    "op_purple": "#8B5CF6",
    "op_cyan": "#06B6D4",
    "op_pink": "#EC4899",
    "op_orange": "#F59E0B"
}

OP_SYMBOLS = {"+": "+", "-": "−", "*": "×", "/": "÷"}
OP_NAMES = {"+": "Add", "-": "Subtract", "*": "Multiply", "/": "Divide"}

class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Calculator — Modern Arithmetic")
        self.geometry("450x800")
        self.configure(fg_color=COLORS["bg_primary"])
        
        # State
        self.selected_op = None
        self.history = []

        # UI Initialization
        self.setup_ui()

    def setup_ui(self):
        # Main Container
        self.main_container = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], corner_radius=28, border_width=1, border_color="#26364A")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # 1. Display Section
        self.display_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.display_frame.pack(fill="x", padx=30, pady=(30, 10))

        self.expr_label = ctk.CTkLabel(self.display_frame, text="", font=("Inter", 14), text_color=COLORS["text_muted"])
        self.expr_label.pack(anchor="e")

        self.result_label = ctk.CTkLabel(self.display_frame, text="0", font=("Inter", 48, "bold"), text_color=COLORS["text_primary"])
        self.result_label.pack(anchor="e")

        # Separator
        self.sep = ctk.CTkFrame(self.main_container, fg_color="#26364A", height=1)
        self.sep.pack(fill="x", padx=20, pady=10)

        # 2. Input Section
        self.input_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.input_container.pack(fill="both", expand=True, padx=30, pady=10)

        ctk.CTkLabel(self.input_container, text="ENTER VALUES", font=("Inter", 11, "bold"), text_color=COLORS["text_muted"]).pack(anchor="w", pady=(0, 15))

        # Number 1
        ctk.CTkLabel(self.input_container, text="First Number", font=("Inter", 13), text_color=COLORS["text_secondary"]).pack(anchor="w")
        self.num1_entry = ctk.CTkEntry(self.input_container, placeholder_text="e.g. 42", height=45, fg_color=COLORS["bg_input"], border_color="#26364A", text_color=COLORS["text_primary"], placeholder_text_color=COLORS["text_muted"])
        self.num1_entry.pack(fill="x", pady=(5, 15))

        # Number 2
        ctk.CTkLabel(self.input_container, text="Second Number", font=("Inter", 13), text_color=COLORS["text_secondary"]).pack(anchor="w")
        self.num2_entry = ctk.CTkEntry(self.input_container, placeholder_text="e.g. 7", height=45, fg_color=COLORS["bg_input"], border_color="#26364A", text_color=COLORS["text_primary"], placeholder_text_color=COLORS["text_muted"])
        self.num2_entry.pack(fill="x", pady=(5, 15))

        # Operations
        ctk.CTkLabel(self.input_container, text="Operation", font=("Inter", 13), text_color=COLORS["text_secondary"]).pack(anchor="w", pady=(0, 5))
        self.op_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        self.op_frame.pack(fill="x", pady=(0, 15))

        self.op_buttons = {}
        ops = [("+", COLORS["op_purple"]), ("-", COLORS["op_cyan"]), ("*", COLORS["op_pink"]), ("/", COLORS["op_orange"])]
        
        for i, (op, color) in enumerate(ops):
            self.op_frame.columnconfigure(i, weight=1)
            btn = ctk.CTkButton(self.op_frame, text=OP_SYMBOLS[op], font=("Inter", 18, "bold"), fg_color=COLORS["bg_input"], text_color=COLORS["text_secondary"], border_color="#26364A", border_width=1, corner_radius=10, height=50, hover_color=COLORS["bg_input_focus"], command=lambda o=op: self.select_operation(o))
            btn.grid(row=0, column=i, padx=4)
            self.op_buttons[op] = btn

        # Calculate Button
        self.calc_btn = ctk.CTkButton(self.input_container, text="Calculate ⏎", font=("Inter", 15, "bold"), fg_color=COLORS["accent_steel"], hover_color="#4A5B61", height=50, corner_radius=14, command=self.perform_calculation)
        self.calc_btn.pack(fill="x", pady=10)

        # New Calculation button (reset)
        self.new_calc_input_btn = ctk.CTkButton(self.input_container, text="New Calculation", font=("Inter", 14), fg_color=COLORS["bg_input"], hover_color=COLORS["bg_input_focus"], text_color=COLORS["text_secondary"], height=45, corner_radius=12, command=self.reset_ui)
        self.new_calc_input_btn.pack(fill="x", pady=5)

        # 3. Result Section (Hidden by default)
        self.result_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        
        self.res_card = ctk.CTkFrame(self.result_container, fg_color=COLORS["bg_input"], corner_radius=22, border_width=1, border_color="#374B5F")
        self.res_card.pack(fill="x", padx=30, pady=20)
        
        self.res_expr_val = ctk.CTkLabel(self.res_card, text="", font=("Inter", 16), text_color=COLORS["text_secondary"])
        self.res_expr_val.pack(pady=(20, 5))
        
        ctk.CTkLabel(self.res_card, text="=", font=("Inter", 20), text_color=COLORS["text_muted"]).pack()
        
        self.res_result_val = ctk.CTkLabel(self.res_card, text="", font=("Inter", 36, "bold"), text_color=COLORS["text_primary"])
        self.res_result_val.pack(pady=(5, 20))
        
        self.new_calc_btn = ctk.CTkButton(self.result_container, text="↺ New Calculation", font=("Inter", 14), fg_color=COLORS["bg_input"], text_color=COLORS["text_secondary"], hover_color=COLORS["bg_input_focus"], height=45, corner_radius=12, command=self.reset_ui)
        self.new_calc_btn.pack(fill="x", padx=30, pady=10)

        # 4. History Section
        self.history_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.history_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))

        hist_header = ctk.CTkFrame(self.history_frame, fg_color="transparent")
        hist_header.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(hist_header, text="HISTORY", font=("Inter", 11, "bold"), text_color=COLORS["text_muted"]).pack(side="left")
        
        self.clear_hist_btn = ctk.CTkButton(hist_header, text="🗑", width=30, height=20, fg_color="transparent", text_color=COLORS["text_muted"], hover_color=COLORS["bg_input_focus"], command=self.clear_history)
        self.clear_hist_btn.pack(side="right")

        self.history_list = ctk.CTkScrollableFrame(self.history_frame, fg_color="transparent", height=150)
        self.history_list.pack(fill="both", expand=True)

        # Initialize empty history message
        self.empty_label = ctk.CTkLabel(self.history_list, text="No calculations yet", font=("Inter", 12, "italic"), text_color=COLORS["text_muted"])
        self.empty_label.pack(pady=20)

    def select_operation(self, op):
        self.selected_op = op
        for o, btn in self.op_buttons.items():
            if o == op:
                btn.configure(fg_color=COLORS["bg_input_focus"], border_color=COLORS["accent_teal"], text_color=COLORS["text_primary"])
            else:
                btn.configure(fg_color=COLORS["bg_input"], border_color="#26364A", text_color=COLORS["text_secondary"])

    def perform_calculation(self):
        try:
            v1 = self.num1_entry.get()
            v2 = self.num2_entry.get()

            if not v1 or not v2:
                self.show_error("Please enter both numbers")
                return

            if not self.selected_op:
                self.show_error("Please select an operation")
                return

            num1 = float(v1)
            num2 = float(v2)
            
            if self.selected_op == "+": result = num1 + num2
            elif self.selected_op == "-": result = num1 - num2
            elif self.selected_op == "*": result = num1 * num2
            elif self.selected_op == "/":
                if num2 == 0:
                    self.show_error("Cannot divide by zero")
                    return
                result = num1 / num2
            
            # Format numbers for display
            num1_str = f"{num1:g}"
            num2_str = f"{num2:g}"
            res_str = f"{result:g}"
            expr = f"{num1_str} {OP_SYMBOLS[self.selected_op]} {num2_str}"

            # Update Display
            self.expr_label.configure(text=expr)
            self.result_label.configure(text=res_str)

            # Show result section, hide input section
            self.input_container.pack_forget()
            self.result_container.pack(fill="both", expand=True, padx=30, pady=10)
            self.res_expr_val.configure(text=expr)
            self.res_result_val.configure(text=res_str)

            # Add to history
            self.add_to_history(expr, res_str)

        except ValueError:
            self.show_error("Invalid input numbers")

    def reset_ui(self):
        # Hide result section if visible
        self.result_container.pack_forget()
        # Show input section
        self.input_container.pack(fill="both", expand=True, padx=30, pady=10)
        # Clear fields
        self.num1_entry.delete(0, "end")
        self.num2_entry.delete(0, "end")
        self.selected_op = None
        for btn in self.op_buttons.values():
            btn.configure(fg_color=COLORS["bg_input"], border_color="#26364A", text_color=COLORS["text_secondary"])
        self.expr_label.configure(text="")
        self.result_label.configure(text="0")
        # Reset result display values
        self.res_expr_val.configure(text="")
        self.res_result_val.configure(text="")

    def add_to_history(self, expr, result):
        if self.empty_label:
            self.empty_label.destroy()
            self.empty_label = None

        item = ctk.CTkFrame(self.history_list, fg_color=COLORS["bg_input"], corner_radius=8)
        item.pack(fill="x", pady=4)
        
        ctk.CTkLabel(item, text=expr, font=("Inter", 12), text_color=COLORS["text_secondary"]).pack(side="left", padx=10, pady=8)
        ctk.CTkLabel(item, text=result, font=("Inter", 13, "bold"), text_color=COLORS["text_primary"]).pack(side="right", padx=10, pady=8)

    def clear_history(self):
        for widget in self.history_list.winfo_children():
            widget.destroy()
        self.empty_label = ctk.CTkLabel(self.history_list, text="No calculations yet", font=("Inter", 12, "italic"), text_color=COLORS["text_muted"])
        self.empty_label.pack(pady=20)

    def show_error(self, message):
        # Simple error display using result label temporarily
        original_text = self.result_label.cget("text")
        self.result_label.configure(text=message, font=("Inter", 20, "bold"), text_color=COLORS["accent_error"])
        self.after(2000, lambda: self.result_label.configure(text=original_text, font=("Inter", 48, "bold"), text_color=COLORS["text_primary"]))

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
