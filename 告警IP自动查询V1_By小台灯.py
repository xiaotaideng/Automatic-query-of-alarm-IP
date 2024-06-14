import tkinter as tk
from tkinter import messagebox

def get_screen_dimensions(window):
    # Function to get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    return screen_width, screen_height


def center_window(window, width, height):
    # Function to center the window on the screen
    screen_width, screen_height = get_screen_dimensions(window)
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))
    window.geometry(f'{width}x{height}+{x_coordinate}+{y_coordinate}')

def get_ip_list():
    def on_submit():
        ip_list = text.get("1.0", tk.END).strip().split('\n')
        root.ip_list = [ip.strip() for ip in ip_list if ip.strip()]

        if not root.ip_list:
            messagebox.showerror("错误", "请输入IP列表")
            return

        update_query_result()

    def update_query_result():
        query_result.config(state=tk.NORMAL)
        query_result.delete("1.0", tk.END)

        ip_list = root.ip_list
        selected_queries = [query_var.get() for query_var in query_vars if query_var.get()]

        if any(selected_queries):
            for selected_query in selected_queries:
                if selected_query == "nginx_query":
                    ip_str_nginx = '\n or '.join([f'client_ip="{ip}"' for ip in ip_list])
                    nginx_query = f'\n---------nginx_query---------\nselect * from nginx_log where {ip_str_nginx}'
                    query_result.insert(tk.END, nginx_query + '\n')
                elif selected_query == "waf_query":
                    ip_str_waf = '\n or '.join([f'client_ip="{ip}"' for ip in ip_list])
                    waf_query = f'\n---------waf_query---------\nselect * from waf_log where {ip_str_waf}'
                    query_result.insert(tk.END, waf_query + '\n')
                elif selected_query == "elb_query":
                    ip_str_elb = '\n or '.join([f'client_ip="{ip}"' for ip in ip_list])
                    elb_query = f'\n---------elb_query---------\nselect * from elb_log where {ip_str_elb}'
                    query_result.insert(tk.END, elb_query + '\n')
                elif selected_query == "ioc_query":
                    ip_str_ioc = '\n or '.join([f'client_ip="{ip}"' for ip in ip_list])
                    ioc_query = f'\n---------ioc_query---------\nselect * from ioc_log where {ip_str_ioc}'
                    query_result.insert(tk.END, ioc_query + '\n')
        else:
            query_result.insert(tk.END, "请先选择要查询的条件")

        query_result.config(state=tk.DISABLED)

    def create_context_menu(widget):
        menu = tk.Menu(widget, tearoff=0)
        menu.add_command(label="复制", command=lambda: widget.event_generate('<<Copy>>'))
        menu.add_command(label="粘贴", command=lambda: widget.event_generate('<<Paste>>'))
        menu.add_command(label="剪切", command=lambda: widget.event_generate('<<Cut>>'))
        widget.bind("<Button-3>", lambda event: menu.tk_popup(event.x_root, event.y_root))

    def select_all():
        all_selected = select_all_var.get()
        for query_var, query in zip(query_vars, queries):
            query_var.set(query if all_selected else "")

    def clear_fields():
        text.delete("1.0", tk.END)
        query_result.config(state=tk.NORMAL)
        query_result.delete("1.0", tk.END)
        query_result.config(state=tk.DISABLED)

    root = tk.Tk()
    root.title("批量IP查询脚本生成器v1-By小台灯")
    root.geometry("900x700")
    # Center the window
    center_window(root, 900, 800)

    # Top frame for IP input and options
    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    input_frame = tk.Frame(top_frame)
    input_frame.pack(side=tk.LEFT, padx=10, pady=10)

    tk.Label(input_frame, text="请输入IP地址，每行一个:").pack(pady=10)

    text = tk.Text(input_frame, height=15, width=70)
    text.pack(side=tk.LEFT)
    create_context_menu(text)

    input_scrollbar = tk.Scrollbar(input_frame)
    input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text.config(yscrollcommand=input_scrollbar.set)
    input_scrollbar.config(command=text.yview)

    options_frame = tk.Frame(top_frame)
    options_frame.pack(side=tk.LEFT, padx=10, pady=10)

    submit_button = tk.Button(options_frame, text="查询", command=on_submit)
    submit_button.grid(row=0, column=1, padx=(0, 10), pady=20)

    clear_button = tk.Button(options_frame, text="清空", command=clear_fields)
    clear_button.grid(row=0, column=2, padx=(10, 0), pady=20)

    query_vars = []
    queries = ["nginx_query", "waf_query", "elb_query", "ioc_query"]
    display_queries = ["nginx", "waf", "elb", "ioc"]

    for idx, (query, display_query) in enumerate(zip(queries, display_queries)):
        query_var = tk.StringVar()
        query_vars.append(query_var)
        tk.Checkbutton(options_frame, text=display_query, variable=query_var, onvalue=query, offvalue="").grid(row=1,
                                                                                                               column=idx,
                                                                                                               padx=5)

    select_all_var = tk.BooleanVar()
    tk.Checkbutton(options_frame, text="全选", variable=select_all_var, command=select_all).grid(row=1,
                                                                                                 column=len(queries),
                                                                                                 padx=5)

    # Bottom frame for query results
    result_frame = tk.Frame(root)
    result_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(result_frame, text="查询结果:").pack(pady=10)

    query_result = tk.Text(result_frame, height=20, width=110, state=tk.DISABLED)
    query_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    create_context_menu(query_result)

    query_scrollbar = tk.Scrollbar(result_frame)
    query_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    query_result.config(yscrollcommand=query_scrollbar.set)
    query_scrollbar.config(command=query_result.yview)

    root.ip_list = []
    root.mainloop()

    return getattr(root, 'ip_list', [])


# 获取IP列表
ips = get_ip_list()
