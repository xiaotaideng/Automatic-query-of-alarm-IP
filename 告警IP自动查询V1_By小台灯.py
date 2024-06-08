import tkinter as tk

# 创建一个函数来显示输入弹窗并展示IP地址列表
def get_ip_list():
    def on_submit():
        ip_list = text.get("1.0", tk.END).strip().split('\n')
        root.ip_list = [ip.strip() for ip in ip_list if ip.strip()]
        update_ip_list_display()

    def update_ip_list_display():
        ip_display.config(state=tk.NORMAL)  # 允许编辑
        ip_display.delete("1.0", tk.END)
        for ip in root.ip_list:
            ip_display.insert(tk.END, ip + '\n')
        ip_display.config(state=tk.DISABLED)  # 禁止编辑

    def create_context_menu(widget):
        menu = tk.Menu(widget, tearoff=0)
        menu.add_command(label="复制", command=lambda: widget.event_generate('<<Copy>>'))
        menu.add_command(label="粘贴", command=lambda: widget.event_generate('<<Paste>>'))
        menu.add_command(label="剪切", command=lambda: widget.event_generate('<<Cut>>'))
        widget.bind("<Button-3>", lambda event: menu.tk_popup(event.x_root, event.y_root))

    root = tk.Tk()
    root.title("批量IP查询脚本生成器v1-By小台灯")
    root.geometry("600x700")

    tk.Label(root, text="请输入IP地址，每行一个:").pack(pady=10)

    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    text = tk.Text(input_frame, height=10, width=50)
    text.pack(side=tk.LEFT)
    create_context_menu(text)

    input_scrollbar = tk.Scrollbar(input_frame)
    input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text.config(yscrollcommand=input_scrollbar.set)
    input_scrollbar.config(command=text.yview)

    submit_button = tk.Button(root, text="提交", command=on_submit)
    submit_button.pack(pady=10)

    tk.Label(root, text="已输入的IP地址列表:").pack(pady=10)

    output_frame = tk.Frame(root)
    output_frame.pack(pady=10)

    ip_display = tk.Text(output_frame, height=27, width=50, state=tk.DISABLED)
    ip_display.pack(side=tk.LEFT)
    create_context_menu(ip_display)

    output_scrollbar = tk.Scrollbar(output_frame)
    output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    ip_display.config(yscrollcommand=output_scrollbar.set)
    output_scrollbar.config(command=ip_display.yview)

    root.ip_list = []
    root.mainloop()

    return getattr(root, 'ip_list', [])

# 获取IP列表
ips = get_ip_list()

# 将IP列表写入文件
with open('ip.txt', 'w') as f:
    for ip in ips:
        f.write(ip + '\n')

# 读取文件内容并处理
with open("ip.txt", "r") as f:
    ips = f.readlines()
    ip_lists = [ip.strip() for ip in ips if ip.strip()]

# 打印最终的IP地址列表（可选）
print("Final IP List:", ip_lists)
