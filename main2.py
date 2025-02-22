from tkinter import *
import math

# -----------------CONSTANTS---------------- #
LIGHT_PINK = "#FFD1DA"
DARK_PINK = "#F257A0"
YELLOW = "#FFFF9A"
PEACH = "#FA5600"
BLUE = "#b3d5e6"
FONT_NAME = "Courier"

TOTAL_CYCLES = 0
cycle = 1
timer = None

window = Tk()
window.config(padx=150, pady=40, background=BLUE)
window.title("Meditation Session")

med_session_label = Label(text="Meditation Session", bg=BLUE, fg="black", font=(FONT_NAME, 20, "bold"))
med_session_label.grid(row=0, column=0, columnspan=3)

# --------------------------------IMAGE-----------------------------------
canvas = Canvas(width=360, height=360, bg=BLUE, highlightthickness=0)
window.lotus_img = PhotoImage(file="./lotus_flower.png")
canvas.create_image(180, 180, image=window.lotus_img)
canvas.grid(row=1, column=0, columnspan=3)

# -------------------------------ASK TIME---------------------------------
med_time_label = Label(text="Add time to your \nmeditation session:", font=(FONT_NAME, 15, "normal"),
                       pady=10, height=2, width=20, bg=BLUE)
med_time_label.grid(row=2, column=0, columnspan=3)

time_spinbox = Spinbox(from_=5, to=30, increment=5, width=7, font=(FONT_NAME, 15, "normal"))
time_spinbox.grid(row=3, column=0)

min_label = Label(text="Minutes", bg=BLUE, width=11, anchor="w", font=(FONT_NAME, 15, "normal"))
min_label.grid(row=3, column=1)


def add_minutes():
    global TOTAL_CYCLES, cycle
    med_time = int(time_spinbox.get())
    TOTAL_CYCLES = int((med_time / 5) * 2)  # Convert to integer
    cycle = 1  # Reset cycle count

    # Remove input UI
    med_time_label.grid_remove()
    time_spinbox.grid_remove()
    min_label.grid_remove()
    add_min_button.grid_remove()

    meditation_start()


add_min_button = Button(text="Add", width=7, font=(FONT_NAME, 15, "normal"), command=add_minutes)
add_min_button.grid(row=3, column=2)


# ------------------------------MEDITATION START--------------------------
def meditation_start():
    global timer_text, cycles_label
    timer_text = canvas.create_text(180, 300, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

    start_button = Button(text="Start", font=(FONT_NAME, 15, "normal"), command=start_timer)
    start_button.grid(row=2, column=0)

    cycles_label = Label(text=f"Cycles\nCompleted: 0", bg=BLUE, font=(FONT_NAME, 15))
    cycles_label.grid(row=2, column=1)

    reset_button = Button(text="Reset", font=(FONT_NAME, 15, "normal"), command=reset_timer)
    reset_button.grid(row=2, column=2)


# ------------------------------COUNTDOWN TIMER---------------------------
def count_down(total_time):
    """Handles the countdown timer."""
    global timer
    minutes = math.floor(total_time / 60)
    sec = total_time % 60
    sec = f"0{sec}" if sec < 10 else sec  # Ensures two-digit seconds format

    canvas.itemconfig(timer_text, text=f"{minutes}:{sec}")

    if total_time > 0:
        timer = window.after(1000, count_down, total_time - 1)
    else:
        start_timer()  # Starts the next cycle after this one ends


def start_timer():
    """Manages the meditation cycle sequence."""
    global TOTAL_CYCLES, cycle

    if TOTAL_CYCLES > 0:
        if cycle % 2 == 1:  # Odd cycles (4-minute session)
            count_down(4 * 60)
        else:  # Even cycles (1-minute break)
            count_down(1 * 60)

        cycles_label.config(text=f"Cycles\nCompleted: {cycle // 2}")  # Updates cycle count
        cycle += 1
        TOTAL_CYCLES -= 1


def reset_timer():
    """Resets the timer and cycle count."""
    global TOTAL_CYCLES, cycle
    window.after_cancel(timer)  # Cancel ongoing countdown
    canvas.itemconfig(timer_text, text="00:00")
    cycles_label.config(text="Cycles\nCompleted: 0")
    cycle = 1
    TOTAL_CYCLES = 0


window.mainloop()