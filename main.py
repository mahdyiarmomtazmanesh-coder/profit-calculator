#------مهدیار ممتازمنش------
import tkinter as tk
from tkinter import ttk
import math

# ---------- Logic ----------
#---ساخت تابع برای محاسبه ی سود---
def anbar(buy, sell):
#---حساب کردن درصد سود
    profit = sell - buy
    sood = profit / (buy / 100)
#---شرط گذاری---
#---مشخص کردن رنگ---  
    if sood >= 70: status, color = 'Wonderful', '#27ae60'
    elif sood >= 50: status, color = 'Excellent', '#2980b9'
    elif sood >= 20: status, color = 'Good', '#e67e22'
    else: status, color = 'Bad', '#e74c3c'
    return sood, status, color

# ---------- Color helpers ----------
def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def interpolate(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex((int(r1+(r2-r1)*t), int(g1+(g2-g1)*t), int(b1+(b2-b1)*t)))

def draw_gradient_rect(canvas, x1, y1, x2, y2, c1, c2, steps=30):
    for i in range(steps):
        t = i / steps
        y_a = y1 + (y2 - y1) * (i / steps)
        y_b = y1 + (y2 - y1) * ((i + 1) / steps)
        canvas.create_rectangle(x1, y_a, x2, y_b, fill=interpolate(c1, c2, t), outline="")

def round_rect(canvas, x1, y1, x2, y2, r=15, **kwargs):
    points = [x1+r,y1, x2-r,y1, x2,y1, x2,y1+r, x2,y2-r, x2,y2,
              x2-r,y2, x1+r,y2, x1,y2, x1,y2-r, x1,y1+r, x1,y1]
    canvas.create_polygon(points, smooth=True, **kwargs)

# ---------- Charts ----------
def clear_canvas():
    canvas.delete("all")

def draw_bar_chart(data):
    clear_canvas()
    buy, sell, profit = data["buy"], data["sell"], data["profit"]
    values = [buy, sell, profit]
    labels = ['Buy', 'Sell', 'Profit']
    colors = [('#74b9ff', '#0984e3'), ('#55efc4', '#00b894'), ('#ffeaa7', '#fdcb6e')]
#---جلوگیری از تقسیم بر صفر---
    max_val = max(values) if max(values) > 0 else 1
    bar_width, gap, base_y, max_h = 90, 45, 260, 210

    for i, (val, label, (c1, c2)) in enumerate(zip(values, labels, colors)):
        x = gap + i * (bar_width + gap)
    #---تنظیم ارتفاع میله
        h = (abs(val) / max_val) * max_h
        canvas.create_rectangle(x+4, base_y-h+4, x+bar_width+4, base_y+4, fill='#dcdde1', outline="")
        draw_gradient_rect(canvas, x, base_y - h, x + bar_width, base_y, c1, c2)
        round_rect(canvas, x, base_y - h, x + bar_width, base_y, r=8, fill="", outline=c2, width=2)
        canvas.create_text(x + bar_width//2, base_y + 20, text=label, font=("Segoe UI", 11, "bold"))
        canvas.create_text(x + bar_width//2, base_y - h - 15, text=str(val), font=("Segoe UI", 11, "bold"))

def draw_pie_chart(data):
    clear_canvas()
    buy, profit = data["buy"], data["profit"]
    total = buy + max(profit, 0)
    if total <= 0: total = 1
    cx, cy, r = 200, 150, 110
    start = 0
    for val, color, label in [(buy, '#74b9ff', 'Buy'), (max(profit,0), '#00b894', 'Profit')]:
        extent = (val / total) * 360
        canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start, extent=extent,
                           fill=color, outline="white", width=2)
        mid_angle = math.radians(start + extent/2)
        lx = cx + (r+30) * math.cos(mid_angle)
        ly = cy - (r+30) * math.sin(mid_angle)
        canvas.create_text(lx, ly, text=f"{label}\n{val}", font=("Segoe UI", 10, "bold"))
        start += extent

def draw_gauge_chart(data):
    clear_canvas()
    sood = data["sood"]
    cx, cy, r = 200, 220, 140
    zones = [(0, 20, '#e74c3c'), (20, 50, '#e67e22'), (50, 70, '#2980b9'), (70, 100, '#27ae60')]
    for a1, a2, color in zones:
        start = 180 - (a1/100)*180
        extent = -((a2-a1)/100)*180
        canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start, extent=extent,
                           style="arc", outline=color, width=25)

    clamped = max(0, min(sood, 100))
    angle = math.radians(180 - (clamped/100)*180)
    nx = cx + (r-30) * math.cos(angle)
    ny = cy - (r-30) * math.sin(angle)
    canvas.create_line(cx, cy, nx, ny, width=4, fill='#2d3436', arrow=tk.LAST)
    canvas.create_oval(cx-8, cy-8, cx+8, cy+8, fill='#2d3436')
    canvas.create_text(cx, cy+40, text=f"{sood:.1f}%", font=("Segoe UI", 18, "bold"))

CHART_FUNCS = {"Bar Chart": draw_bar_chart, "Pie Chart": draw_pie_chart, "Gauge Chart": draw_gauge_chart}
#---داده‌های آخرین محاسبه ذخیره می‌شن تا وقتی نوع نمودار عوض می‌شه، نیازی به وارد کردن دوباره اعداد نباشه---
last_data = None

def render_chart():
    global last_data
    if last_data:
        CHART_FUNCS[chart_type.get()](last_data)

def calculate():
    global last_data
    buy, sell = int(entry_buy.get()), int(entry_sell.get())
    product = entry_product.get()
    sood, status, color = anbar(buy, sell)
    profit = sell - buy
    last_data = {"buy": buy, "sell": sell, "profit": profit, "sood": sood}
    label_result.config(text=f"{product}: {sood:.1f}%  —  {status}", foreground=color)
    render_chart()

# ---------- UI ----------
root = tk.Tk()
root.title("Profit Calculator")
root.configure(bg="#f5f6fa")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#f5f6fa", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=8)
style.configure("Result.TLabel", font=("Segoe UI", 13, "bold"), background="#f5f6fa")

header = tk.Label(root, text="📊 Profit Calculator", font=("Segoe UI", 18, "bold"),
                   bg="#f5f6fa", fg="#2d3436")
header.grid(row=0, column=0, columnspan=2, pady=(15, 10))

form = ttk.Frame(root)
form.grid(row=1, column=0, columnspan=2, padx=20)

for text, row in [("Product:", 0), ("Buy Price:", 1), ("Sell Price:", 2)]:
    ttk.Label(form, text=text).grid(row=row, column=0, padx=10, pady=6, sticky="e")

entry_product = ttk.Entry(form); entry_product.grid(row=0, column=1)
entry_buy = ttk.Entry(form); entry_buy.grid(row=1, column=1)
entry_sell = ttk.Entry(form); entry_sell.grid(row=2, column=1)

chart_type = tk.StringVar(value="Bar Chart")
ttk.Label(form, text="Chart Type:").grid(row=3, column=0, padx=10, pady=6, sticky="e")
combo = ttk.Combobox(form, textvariable=chart_type, values=list(CHART_FUNCS.keys()), state="readonly")
combo.grid(row=3, column=1)
combo.bind("<<ComboboxSelected>>", lambda e: render_chart())

ttk.Button(root, text="Calculate", command=calculate).grid(row=2, column=0, columnspan=2, pady=12)
label_result = ttk.Label(root, text="", style="Result.TLabel")
label_result.grid(row=3, column=0, columnspan=2, pady=(0, 10))

canvas = tk.Canvas(root, width=400, height=300, bg="white", highlightthickness=1, highlightbackground="#dcdde1")
canvas.grid(row=4, column=0, columnspan=2, padx=20, pady=15)

root.mainloop()
