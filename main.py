import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global variables
df = None
current_fig = None

def load_data():
    """Load CSV file and update column dropdown"""
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)

            if df.empty:
                raise ValueError("The selected file is empty or invalid.")

            # Update info label
            data_info.set(f"Data Loaded: {file_path.split('/')[-1]}\nColumns: {', '.join(df.columns)}")
            status_bar.config(text="✅ Data Loaded Successfully")

            # Update column dropdown menu
            columns = df.columns.tolist()
            if columns:
                plot_column.set(columns[0])  # default to first column
                menu = column_menu["menu"]
                menu.delete(0, "end")
                for col in columns:
                    menu.add_command(label=col, command=lambda value=col: plot_column.set(value))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            status_bar.config(text="❌ Failed to Load Data")

def show_statistics():
    """Show basic descriptive statistics"""
    if df is not None:
        stats_window = tk.Toplevel(root)
        stats_window.title("Data Statistics")
        stats_window.configure(bg="#1C1C1C")

        stats_text = tk.Text(stats_window, font=("Consolas", 10),
                             fg="#E0E0E0", bg="#2F2F2F", padx=10, pady=10)
        stats_text.insert(tk.END, str(df.describe()))
        stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    else:
        status_bar.config(text="⚠ No Data Loaded")

def plot_data():
    """Generate and display selected chart"""
    global current_fig
    if df is not None:
        column = plot_column.get()
        chart_type = chart_type_var.get()

        if column in df.columns:
            # Clear previous chart
            for widget in plot_frame.winfo_children():
                widget.destroy()

            current_fig, ax = plt.subplots(figsize=(8, 6))

            if chart_type == "Histogram":
                sns.histplot(df[column], kde=True, ax=ax)
            elif chart_type == "Scatter Plot":
                sns.scatterplot(x=df.index, y=df[column], ax=ax)
            elif chart_type == "Line Plot":
                sns.lineplot(x=df.index, y=df[column], ax=ax)
            elif chart_type == "Box Plot":
                sns.boxplot(data=df, y=column, ax=ax)
            elif chart_type == "Bar Plot":
                sns.barplot(x=df.index, y=df[column], ax=ax)

            ax.set_title(f"{chart_type} for {column}", fontsize=12)

            canvas = FigureCanvasTkAgg(current_fig, master=plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            status_bar.config(text=f"✅ {chart_type} Generated for Column: {column}")
        else:
            status_bar.config(text="⚠ Invalid Column Selected")
    else:
        status_bar.config(text="⚠ No Data Loaded")

def export_chart():
    """Save chart as PNG/JPEG"""
    global current_fig
    if current_fig is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("All Files", "*.*")])
        if file_path:
            try:
                current_fig.savefig(file_path)
                status_bar.config(text=f"✅ Chart saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export chart: {str(e)}")
    else:
        messagebox.showwarning("Warning", "⚠ No chart to export")

# ---------------- GUI DESIGN ----------------
root = tk.Tk()
root.title("EDA Tool - Dark Theme")
root.geometry("1100x650")
root.configure(bg="#121212")

# Header
header_frame = tk.Frame(root, bg="#2A2A2A", pady=10)
header_frame.pack(fill=tk.X)
header_label = tk.Label(header_frame, text="Exploratory Data Analysis Tool",
                        font=("Helvetica", 18, "bold"), fg="#E0E0E0", bg="#2A2A2A")
header_label.pack()

# Main area
main_frame = tk.Frame(root, bg="#121212", pady=10)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Left panel (controls)
left_frame = tk.Frame(main_frame, bg="#1C1C1C", bd=2, relief=tk.GROOVE, padx=10, pady=10)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

# Right panel (plots)
plot_frame = tk.Frame(main_frame, bg="#2A2A2A", relief=tk.SUNKEN, bd=2)
plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Info label
data_info = tk.StringVar()
info_label = tk.Label(left_frame, textvariable=data_info, wraplength=200,
                      fg="#E0E0E0", bg="#1C1C1C", font=("Helvetica", 10))
info_label.pack(pady=5)

# Buttons
tk.Button(left_frame, text="📂 Load Data", command=load_data, width=20).pack(pady=5)
tk.Button(left_frame, text="📊 Show Statistics", command=show_statistics, width=20).pack(pady=5)

# Column dropdown (instead of entry)
plot_column = tk.StringVar()
tk.Label(left_frame, text="Select Column:", fg="#E0E0E0", bg="#1C1C1C").pack(pady=5)
column_menu = tk.OptionMenu(left_frame, plot_column, "")
column_menu.config(width=18)
column_menu.pack(pady=5)

# Chart type dropdown
chart_type_var = tk.StringVar(value="Histogram")
tk.Label(left_frame, text="Chart Type:", fg="#E0E0E0", bg="#1C1C1C").pack(pady=5)
chart_menu = tk.OptionMenu(left_frame, chart_type_var, "Histogram", "Scatter Plot", "Line Plot", "Box Plot", "Bar Plot")
chart_menu.config(width=18)
chart_menu.pack(pady=5)

# Plot & Export buttons
tk.Button(left_frame, text="📈 Plot Column", command=plot_data, width=20).pack(pady=5)
tk.Button(left_frame, text="💾 Export Chart", command=export_chart, width=20).pack(pady=5)

# Status bar
status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor="w",
                      fg="#E0E0E0", bg="#2A2A2A")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
