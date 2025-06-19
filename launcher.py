#!/usr/bin/env python3
"""
AutoGen Voice Agent 图形界面启动器
提供三种模式选择：演示模式、文字交互、语音交互
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
from pathlib import Path
import threading

class VoiceAgentLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoGen 语音助手启动器 v3.0")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('default')
        
        # 设置工作目录
        self.working_dir = Path(__file__).parent
        os.chdir(self.working_dir)
        
        # 创建界面
        self.create_widgets()
        
        # 居中窗口
        self.center_window()
        
    def center_window(self):
        """居中显示窗口"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_frame = ttk.Frame(self.root, padding="20")
        title_frame.pack(fill=tk.X)
        
        title = ttk.Label(
            title_frame, 
            text="🤖 AutoGen 多智能体语音助手",
            font=('Arial', 18, 'bold')
        )
        title.pack()
        
        subtitle = ttk.Label(
            title_frame,
            text="基于 OpenAI Whisper 的本地语音识别系统",
            font=('Arial', 12)
        )
        subtitle.pack(pady=(5, 0))
        
        # 分隔线
        ttk.Separator(self.root, orient='horizontal').pack(fill=tk.X, padx=20, pady=10)
        
        # 按钮框架
        button_frame = ttk.Frame(self.root, padding="20")
        button_frame.pack(expand=True, fill=tk.BOTH)
        
        # 演示模式按钮
        demo_btn = tk.Button(
            button_frame,
            text="🎯 演示模式",
            font=('Arial', 14),
            bg='#4CAF50',
            fg='white',
            height=2,
            width=20,
            command=self.launch_demo,
            relief=tk.RAISED,
            bd=3
        )
        demo_btn.pack(pady=10)
        
        demo_desc = ttk.Label(
            button_frame,
            text="查看系统功能演示和使用说明",
            font=('Arial', 10),
            foreground='gray'
        )
        demo_desc.pack()
        
        # 文字交互模式按钮
        text_btn = tk.Button(
            button_frame,
            text="⌨️ 文字交互模式",
            font=('Arial', 14),
            bg='#2196F3',
            fg='white',
            height=2,
            width=20,
            command=self.launch_text,
            relief=tk.RAISED,
            bd=3
        )
        text_btn.pack(pady=10)
        
        text_desc = ttk.Label(
            button_frame,
            text="通过键盘输入与智能助手对话",
            font=('Arial', 10),
            foreground='gray'
        )
        text_desc.pack()
        
        # 语音交互模式按钮
        voice_btn = tk.Button(
            button_frame,
            text="🎙️ 语音交互模式",
            font=('Arial', 14),
            bg='#FF9800',
            fg='white',
            height=2,
            width=20,
            command=self.launch_voice,
            relief=tk.RAISED,
            bd=3
        )
        voice_btn.pack(pady=10)
        
        voice_desc = ttk.Label(
            button_frame,
            text="使用语音与智能助手自然对话",
            font=('Arial', 10),
            foreground='gray'
        )
        voice_desc.pack()
        
        # 底部信息
        info_frame = ttk.Frame(self.root, padding="10")
        info_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        info = ttk.Label(
            info_frame,
            text="© 2025 Rick | GitHub: RRiiiccckkk",
            font=('Arial', 9),
            foreground='gray'
        )
        info.pack()
        
    def run_command(self, command, mode_name):
        """在新线程中运行命令"""
        def run():
            try:
                # 显示启动中的消息
                self.root.withdraw()  # 隐藏主窗口
                
                # 创建等待窗口
                wait_window = tk.Toplevel()
                wait_window.title("启动中...")
                wait_window.geometry("300x100")
                wait_window.resizable(False, False)
                
                # 居中等待窗口
                wait_window.update_idletasks()
                x = (wait_window.winfo_screenwidth() // 2) - 150
                y = (wait_window.winfo_screenheight() // 2) - 50
                wait_window.geometry(f'300x100+{x}+{y}')
                
                wait_label = ttk.Label(
                    wait_window,
                    text=f"正在启动 {mode_name}...\n请稍候",
                    font=('Arial', 12)
                )
                wait_label.pack(expand=True)
                
                # 运行命令
                if sys.platform == "win32":
                    # Windows: 在新的命令提示符窗口中运行
                    subprocess.Popen(
                        f'start cmd /k "{sys.executable} {command}"',
                        shell=True,
                        cwd=self.working_dir
                    )
                elif sys.platform == "darwin":
                    # macOS: 在新的终端窗口中运行
                    apple_script = f'''
                    tell application "Terminal"
                        do script "cd '{self.working_dir}' && {sys.executable} {command}"
                        activate
                    end tell
                    '''
                    subprocess.run(['osascript', '-e', apple_script])
                else:
                    # Linux: 尝试常见的终端模拟器
                    terminals = [
                        ['gnome-terminal', '--', 'bash', '-c'],
                        ['konsole', '-e', 'bash', '-c'],
                        ['xterm', '-e', 'bash', '-c'],
                        ['xfce4-terminal', '-e', 'bash', '-c']
                    ]
                    
                    cmd = f'cd "{self.working_dir}" && {sys.executable} {command}; read -p "按Enter键退出..."'
                    
                    for terminal in terminals:
                        try:
                            subprocess.Popen(terminal + [cmd])
                            break
                        except:
                            continue
                
                # 等待一下然后关闭等待窗口
                wait_window.after(2000, wait_window.destroy)
                wait_window.after(2100, self.root.deiconify)  # 重新显示主窗口
                
            except Exception as e:
                messagebox.showerror("启动失败", f"无法启动 {mode_name}:\n{str(e)}")
                self.root.deiconify()
                
        # 在新线程中运行
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        
    def launch_demo(self):
        """启动演示模式"""
        self.run_command("demo_voice.py", "演示模式")
        
    def launch_text(self):
        """启动文字交互模式"""
        self.run_command("start_voice.py --mode text", "文字交互模式")
        
    def launch_voice(self):
        """启动语音交互模式"""
        self.run_command("start_voice.py --mode voice", "语音交互模式")

def main():
    """主函数"""
    root = tk.Tk()
    app = VoiceAgentLauncher(root)
    
    # 设置图标（如果有的话）
    try:
        if sys.platform == "win32":
            root.iconbitmap(default='icon.ico')
    except:
        pass
    
    root.mainloop()

if __name__ == "__main__":
    main()
