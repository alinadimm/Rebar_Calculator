import tkinter as tk
from tkinter import ttk
import math

def calculate_rebars():
    try:
        height = float(height_entry.get()) 
        width = float(width_entry.get()) 
        rebar_diameter = int(rebar_dropdown.get())
        moment_frame_type = moment_frame_dropdown.get()
        confinement_bar_size = int(confinement_dropdown.get())
        clear_cover = float(clear_cover_entry.get())
        min_allowable_spacing = float(min_spacing_entry.get())

        if moment_frame_type == "SMF":
            allowable_area_percentage = 0.06 / 2
        else:
            allowable_area_percentage = 0.08 / 2

        gross_area = width * height
        allowable_rebar_area = gross_area * allowable_area_percentage

        rebar_area = (math.pi * (rebar_diameter / 2) ** 2)
        
        # Calculate number of rebars for horizontal and vertical edges
        num_rebars = int((allowable_rebar_area / rebar_area))
        if num_rebars >= 4:
            num_edge_rebars = num_rebars - 4
        else:
            num_edge_rebars = 0
        
        num_rebars_horizontal = int(num_edge_rebars/4)
        num_rebars_vertical = int(num_edge_rebars/4)
       
        # Distribute rebars based on width-to-height ratio
        width_to_height_ratio = width / height

        if width_to_height_ratio < 1:
            num_rebars_vertical = int(num_rebars_vertical / width_to_height_ratio)

        elif width_to_height_ratio > 1:
            num_rebars_horizontal = int(num_rebars_horizontal * width_to_height_ratio)
    

        # Total number of rebars
        total_rebars = (num_rebars_horizontal + num_rebars_vertical) * 2 + 4
        
        num_rebars_3_dir = num_rebars_horizontal + 2
        num_rebars_2_dir = num_rebars_vertical + 2

        # Calculate clear spacing between bars
        clear_spacing_3_dir = (width - 2 * clear_cover - 2 * confinement_bar_size - rebar_diameter) / (num_rebars_3_dir - 1) - rebar_diameter
        clear_spacing_2_dir = (height - 2 * clear_cover - 2 * confinement_bar_size - rebar_diameter) / (num_rebars_2_dir - 1) - rebar_diameter

        # Check if clear spacing is greater than or equal to minimum allowable spacing
        while min(clear_spacing_2_dir, clear_spacing_3_dir) < min_allowable_spacing:
            if clear_spacing_2_dir < clear_spacing_3_dir:
                num_rebars_2_dir -= 1
            else:
                num_rebars_3_dir -= 1

            clear_spacing_3_dir = (width - 2 * clear_cover - 2 * confinement_bar_size - rebar_diameter) / (num_rebars_3_dir - 1) - rebar_diameter
            clear_spacing_2_dir = (height - 2 * clear_cover - 2 * confinement_bar_size - rebar_diameter) / (num_rebars_2_dir - 1) - rebar_diameter
            total_rebars = (num_rebars_2_dir - 2 + num_rebars_3_dir - 2) * 2 + 4

        # Check if allowable percentage is exceeded
        while total_rebars * rebar_area > allowable_area_percentage * gross_area:
            if clear_spacing_2_dir < clear_spacing_3_dir:
                num_rebars_2_dir -= 1
            else:
                num_rebars_3_dir -= 1

            clear_spacing_3_dir = (width - 2 * clear_cover - 2 * confinement_bar_size - rebar_diameter) / (num_rebars_3_dir - 1) - rebar_diameter
            clear_spacing_2_dir = (height - 2 * clear_cover - 2 * confinement_bar_size - rebar_diameter) / (num_rebars_2_dir - 1) - rebar_diameter
            total_rebars = (num_rebars_2_dir - 2 + num_rebars_3_dir - 2) * 2 + 4
            
            
        current_reinforcement_percentage = (total_rebars * rebar_area) / gross_area * 100

        result_label.config(text=f"Number of {rebar_diameter}-mm rebars: {total_rebars}")
        current_percentage_label.config(text=f"Current reinforcement percentage: {current_reinforcement_percentage:.2f}%")
        allowable_percentage_label.config(text=f"Allowable percentage (considering overlap): {allowable_area_percentage * 100}%")
        num_rebars_2_dir_label.config(text=f"Number of bars along 3-dir face (width): {num_rebars_3_dir}")
        num_rebars_3_dir_label.config(text=f"Number of bars along 2-dir face (height): {num_rebars_2_dir}")
        clear_spacing_2_dir_label.config(text=f"Clear spacing along 3-dir face: {clear_spacing_3_dir:.2f} mm")
        clear_spacing_3_dir_label.config(text=f"Clear spacing along 2-dir face: {clear_spacing_2_dir:.2f} mm")
    except ValueError:
        result_label.config(text="Please enter valid dimensions.")

root = tk.Tk()
root.title("Rebar Calculator")

main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0)


height_label = ttk.Label(main_frame, text="Depth (mm):")
height_label.grid(row=0, column=0, sticky="w")

height_entry = ttk.Entry(main_frame)
height_entry.grid(row=0, column=1)

width_label = ttk.Label(main_frame, text="Width (mm):")
width_label.grid(row=1, column=0, sticky="w")

width_entry = ttk.Entry(main_frame)
width_entry.grid(row=1, column=1)


rebar_label = ttk.Label(main_frame, text="Rebar Diameter (mm):")
rebar_label.grid(row=2, column=0, sticky="w")

rebar_values = [18, 20, 22, 25]
rebar_dropdown = ttk.Combobox(main_frame, values=rebar_values)
rebar_dropdown.grid(row=2, column=1)
rebar_dropdown.current(0)

confinement_label = ttk.Label(main_frame, text="Confinement Bar Size (mm):")
confinement_label.grid(row=3, column=0, sticky="w")

confinement_values = [8, 10, 12]
confinement_dropdown = ttk.Combobox(main_frame, values=confinement_values)
confinement_dropdown.grid(row=3, column=1)
confinement_dropdown.current(0)

clear_cover_label = ttk.Label(main_frame, text="Clear Cover (mm):")
clear_cover_label.grid(row=4, column=0, sticky="w")

clear_cover_entry = ttk.Entry(main_frame)
clear_cover_entry.grid(row=4, column=1)

min_spacing_label = ttk.Label(main_frame, text="Minimum Allowable Clear Spacing (mm):")
min_spacing_label.grid(row=5, column=0, sticky="w")

min_spacing_entry = ttk.Entry(main_frame)
min_spacing_entry.grid(row=5, column=1)

moment_frame_label = ttk.Label(main_frame, text="Moment Frame Type:")
moment_frame_label.grid(row=6, column=0, sticky="w")

moment_frame_values = ["SMF", "OMF/IMF"]
moment_frame_dropdown = ttk.Combobox(main_frame, values=moment_frame_values)
moment_frame_dropdown.grid(row=6, column=1)
moment_frame_dropdown.current(0)

calculate_button = ttk.Button(main_frame, text="Calculate", command=calculate_rebars)
calculate_button.grid(row=7, columnspan=2)

result_label = ttk.Label(main_frame, text="")
result_label.grid(row=8, columnspan=2)

current_percentage_label = ttk.Label(main_frame, text="")
current_percentage_label.grid(row=9, columnspan=2)

allowable_percentage_label = ttk.Label(main_frame, text="")
allowable_percentage_label.grid(row=10, columnspan=2)

num_rebars_2_dir_label = ttk.Label(main_frame, text="")
num_rebars_2_dir_label.grid(row=11, columnspan=2)

num_rebars_3_dir_label = ttk.Label(main_frame, text="")
num_rebars_3_dir_label.grid(row=12, columnspan=2)

clear_spacing_2_dir_label = ttk.Label(main_frame, text="")
clear_spacing_2_dir_label.grid(row=13, columnspan=2)

clear_spacing_3_dir_label = ttk.Label(main_frame, text="")
clear_spacing_3_dir_label.grid(row=14, columnspan=2)

root.mainloop()
