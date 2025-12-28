import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import discord
import threading
import asyncio

COLOR_BG = "#050505"
COLOR_PANEL = "#111111"
COLOR_HEADER_BG = "#0000FF"
COLOR_ACCENT = "#00F3FF"
COLOR_TEXT = "#E0E0E0"
COLOR_SUCCESS = "#00FF41"
COLOR_WARN = "#FF3333"
FONT_TECH = ("Consolas", 10)
FONT_HEADER = ("Consolas", 14, "bold")


def log(message, color=COLOR_SUCCESS):
    def _update():
        log_area.configure(state='normal')
        log_area.insert(tk.END, f"> {message}\n")
        log_area.see(tk.END)
        log_area.configure(state='disabled')

    if window:
        window.after(0, _update)


def set_status(text, color=COLOR_ACCENT):
    window.after(0, lambda: status_label.config(text=f"STATUS: {text}", fg=color))


class MyClient(discord.Client):
    def __init__(self, channel_id, message_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_channel_id = channel_id
        self.target_message_id = message_id

    async def on_ready(self):
        log(f"CONNECTION ESTABLISHED. USER: {self.user}", COLOR_ACCENT)
        set_status("SCRAPING DATA...", COLOR_SUCCESS)

        try:
            log("SCANNING FOR CHANNEL TARGET...")
            channel = self.get_channel(self.target_channel_id)
            if not channel:
                channel = await self.fetch_channel(self.target_channel_id)
            log(f"TARGET ACQUIRED: {channel.name}")

            log("LOCATING MESSAGE PACKET...")
            try:
                msg = await channel.fetch_message(self.target_message_id)
                log(f"MSG FOUND. CONTENT: {msg.content[:20]}...")
            except discord.NotFound:
                log("ERROR: INVALID MESSAGE ID", COLOR_WARN)
                set_status("ERROR", COLOR_WARN)
                await self.close()
                return

            unique_users = set()
            log("EXTRACTING ENTITIES...")

            for reaction in msg.reactions:
                emoji_name = reaction.emoji if isinstance(reaction.emoji, str) else reaction.emoji.name
                log(f" [ ANALYZING EMOJI: {emoji_name} ]")

                count = 0
                async for user in reaction.users(limit=None):
                    user_str = f"{user.name} | ID: {user.id}"
                    if user_str not in unique_users:
                        unique_users.add(user_str)
                        count += 1
                        if count % 100 == 0:
                            log(f"   ...extracted {count} users...")
                            await asyncio.sleep(0.01)

            filename = f"reactions_{self.target_message_id}.txt"
            log(f"WRITING DATABASE: {filename}")

            with open(filename, "w", encoding="utf-8") as f:
                f.write("-- MADE BY THENOTFUEL --\n")
                f.write("Discord: @face.punch\n")
                f.write("=" * 30 + "\n")
                for u in unique_users:
                    f.write(u + "\n")

            log("PROCESS COMPLETE.", COLOR_SUCCESS)
            set_status("FINISHED", COLOR_SUCCESS)
            messagebox.showinfo("SYSTEM", f"Extraction successful.\nSaved to: {filename}")
            await self.close()

        except Exception as e:
            log(f"RUNTIME ERROR: {e}", COLOR_WARN)
            set_status("CRITICAL FAILURE", COLOR_WARN)
            await self.close()


def start_process():
    token = entry_token.get().strip().replace('"', '')
    try:
        c_id = int(entry_channel.get().strip())
        m_id = int(entry_msg.get().strip())
    except ValueError:
        messagebox.showerror("INPUT ERROR", "ID must be numeric.")
        return

    if not token:
        messagebox.showerror("INPUT ERROR", "Authorization token missing.")
        return

    btn_start.config(state="disabled", text="[ PROCESSING ]", bg=COLOR_WARN)
    progress.start(15)
    set_status("INITIALIZING...", COLOR_ACCENT)

    log("LOGGING IN...")
    log("CONNECTING TO DISCORD GATEWAY (WAIT)...")

    def run_async():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = MyClient(c_id, m_id)
        try:
            client.run(token)
        except Exception as e:
            log(f"CONNECTION FAILED: {e}", COLOR_WARN)
            set_status("AUTH ERROR", COLOR_WARN)
        finally:
            window.after(0, stop_ui_loading)

    threading.Thread(target=run_async, daemon=True).start()


def stop_ui_loading():
    progress.stop()
    btn_start.config(state="normal", text="[ EXECUTE ]", bg="black")
    set_status("STANDBY", COLOR_TEXT)


window = tk.Tk()
window.title("REACTION2USER")
window.geometry("600x680")
window.configure(bg=COLOR_BG)
window.resizable(False, False)

style = ttk.Style()
style.theme_use('alt')
style.configure("Horizontal.TProgressbar", background=COLOR_ACCENT, troughcolor=COLOR_PANEL, thickness=6)

frame_top = tk.Frame(window, bg=COLOR_HEADER_BG)
frame_top.pack(fill="x", pady=(0, 20))
tk.Label(frame_top, text="/// Reaction2User ///", font=("Consolas", 16, "bold"), fg="white",
         bg=COLOR_HEADER_BG).pack(pady=(15, 5))
status_label = tk.Label(frame_top, text="???", font=("Consolas", 10), fg="white", bg=COLOR_HEADER_BG)
status_label.pack(pady=(0, 15))


def create_input(label, parent):
    wrapper = tk.Frame(parent, bg=COLOR_BG, pady=5)
    wrapper.pack(fill="x", padx=40)
    tk.Label(wrapper, text=label, font=("Consolas", 9, "bold"), fg=COLOR_TEXT, bg=COLOR_BG, anchor="w").pack(fill="x")
    border_frame = tk.Frame(wrapper, bg=COLOR_ACCENT, padx=1, pady=1)
    border_frame.pack(fill="x", pady=2)
    ent = tk.Entry(border_frame, bg=COLOR_PANEL, fg="white", font=("Consolas", 11), insertbackground="white",
                   relief="flat")
    ent.pack(fill="x", ipady=4)
    return ent


frame_inputs = tk.Frame(window, bg=COLOR_BG)
frame_inputs.pack(fill="x", pady=10)

entry_token = create_input("DISCORD_TOKEN :", frame_inputs)
entry_channel = create_input("TARGET_CHANNEL_ID :", frame_inputs)
entry_msg = create_input("TARGET_MESSAGE_ID :", frame_inputs)

progress = ttk.Progressbar(window, style="Horizontal.TProgressbar", orient="horizontal", length=520,
                           mode="indeterminate")
progress.pack(pady=20)


def on_enter(e):
    if btn_start['state'] == 'normal':
        btn_start.config(bg=COLOR_ACCENT, fg="black")


def on_leave(e):
    if btn_start['state'] == 'normal':
        btn_start.config(bg="black", fg=COLOR_ACCENT)


btn_start = tk.Button(window, text="[ EXECUTE ]", command=start_process,
                      font=("Consolas", 14, "bold"),
                      bg="black", fg=COLOR_ACCENT,
                      activebackground=COLOR_ACCENT, activeforeground="black",
                      relief="flat", bd=0, cursor="hand2")
btn_start.pack(fill="x", padx=40, ipady=5)

btn_start.bind("<Enter>", on_enter)
btn_start.bind("<Leave>", on_leave)

tk.Label(window, text="SYSTEM_LOGS:", font=("Consolas", 8), fg="gray", bg=COLOR_BG).pack(anchor="w", padx=40,
                                                                                         pady=(20, 0))

log_area = scrolledtext.ScrolledText(window, width=70, height=10, state='disabled',
                                     font=("Courier New", 9), bg="#000000", fg=COLOR_SUCCESS,
                                     relief="flat", highlightthickness=1, highlightbackground=COLOR_ACCENT)
log_area.pack(pady=5, padx=40)

tk.Label(window, text="by TheNotFuel", font=("Consolas", 8), fg="#333333", bg=COLOR_BG).pack(side="bottom", pady=10)

window.mainloop()


