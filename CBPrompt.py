from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
import re
import os
import webbrowser


def get_list():
    f = open('Prompt.txt', encoding='utf-8')
    content = f.read()
    f.close()
    list_1 = []
    list_2 = []
    pattern_1 = re.compile(r'%(.*?)%')
    pattern_2 = re.compile(r'%(.*?)%(.*?)\((.*?)\)')
    list_1 = re.findall(pattern_1, content)
    list_1 = list(set(list_1))
    list_2 = re.findall(pattern_2, content)
    return list_1, list_2


def sort():
    f = open('Prompt.txt', encoding='utf-8')
    content_all = f.readlines()
    f.close()
    content_all = sorted(list(set(content_all)))
    if '\n' in content_all:
        content_all.remove('\n')
    f = open('Prompt.txt', 'w', encoding='utf-8')
    for i in range(0, len(content_all)):
        f.write(content_all[i])
    f.close()


def open_pro():
    os.startfile(r'Prompt.txt')


def open_pre():
    path = os.getcwd()
    os.startfile(path + "\\Presets")


def open_help():
    path = os.getcwd()
    os.startfile(r'Prompt.txt')


def open_git():
    



sort()
list1, list2 = get_list()
path = os.getcwd()
window = Tk()
window.title("Prompt")
window.geometry("590x300")
# 菜单
main_menu = Menu(window)
file_menu = Menu(main_menu, tearoff=False)
help_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="文件", menu=file_menu)
file_menu.add_command(label="打开Prompt.txt", command=open_pro)
file_menu.add_command(label="打开Presets文件夹", command=open_pre)
main_menu.add_cascade(label="帮助", menu=help_menu)
help_menu.add_command(label="帮助文档", command=open_help)
help_menu.add_command(label="打开Github")
window.config(menu=main_menu)
# 文字
lab_1 = Label(window, text="Tag类型")
lab_1.grid(column=0, row=0)
lab_2 = Label(window, text="Tag选择")
lab_2.grid(column=1, row=0)
lab_3 = Label(window, text="正面Tag")
lab_3.grid(column=0, row=2, sticky='w')
lab_3 = Label(window, text="负面Tag")
lab_3.grid(column=0, row=4, sticky='w')
lab_4 = Label(window, text="预设")
lab_4.grid(column=0, row=6)
lab_5 = Label(window, text="预设保存名")
lab_5.grid(column=1, row=6)
# 复选框
combo_1 = Combobox(window, state="readonly")
combo_1['values'] = sorted(list1)
combo_1.grid(column=0, row=1)


def get1(event):
    list3 = []
    type1 = combo_1.get()
    for i in range(len(list2)):
        if list2[i][0] == type1:
            list3.append(list2[i][2])
    combo_2['values'] = list3


combo_1.bind("<<ComboboxSelected>>", get1)
combo_2 = Combobox(window, state="readonly")
combo_2.grid(column=1, row=1)
combo_3 = Combobox(window, state="readonly")
combo_3.grid(column=0, row=7)
combo_3['values'] = os.listdir(path+'\\Presets')
# Positive Prompt文本框
txt_1 = scrolledtext.ScrolledText(window, width=80, height=4, undo=True)
txt_1.grid(column=0, row=3, columnspan=3)
# Negative Prompt文本框
txt_2 = scrolledtext.ScrolledText(window, width=80, height=4, undo=True)
txt_2.grid(column=0, row=5, columnspan=3)
f = open(path + "\\Presets\\预设.txt", "r", encoding='utf-8')
txt_1.insert('insert', f.readline().rstrip())
txt_2.insert('insert', f.readline().rstrip())
f.close()
# enter
entry_1 = Entry(window)
entry_1.grid(column=1, row=7)


def func(event):
    list4 = []
    type1 = combo_1.get()
    for i in range(len(list2)):
        if list2[i][0] == type1:
            list4.append(list2[i][1])
    a = combo_2.current()
    txt_1.insert('insert', list4[a]+",")


def save():
    i = 1
    path = os.getcwd()
    if len(entry_1.get()) == 0:
        while 1:
            if os.path.exists(path+"\\Presets\\预设"+str(i)+".txt"):
                i = i+1
            else:
                f = open(path + "\\Presets\\预设" + str(i) + ".txt", "w", encoding='utf-8')
                break
    else:
        f = open(path + "\\Presets\\" + entry_1.get() + ".txt", "a", encoding='utf-8')
        entry_1.delete(0, "end")
    p_prompt = txt_1.get("1.0", "end")
    n_prompt = txt_2.get("1.0", "end")
    f.write(p_prompt+"\n"+n_prompt)
    combo_3['values'] = os.listdir(path + '\\Presets')


def load():
    if len(txt_1.get("1.0", "end")) != 1 and len(txt_2.get("1.0", "end")) != 1:
        txt_1.edit_undo()
        txt_2.edit_undo()
    path = os.getcwd()
    fill_name = combo_3.get()
    f = open(path + "\\Presets\\"+fill_name, "r", encoding='utf-8')
    txt_1.insert('insert', f.readline().rstrip())
    txt_2.insert('insert', f.readline().rstrip())
    f.close()


def copy_po():
    window.clipboard_append(txt_1.get("1.0", "end"))


def copt_ne():
    window.clipboard_append(txt_2.get("1.0", "end"))


combo_2.bind("<<ComboboxSelected>>", func)
# 插入按钮
btn_1 = Button(window, text="保存预设", command=save)
btn_1.grid(column=2, row=6)
btn_2 = Button(window, text="加载预设", command=load)
btn_2.grid(column=2, row=7)
btn_3 = Button(window, text="复制正面tag", command=copy_po)
btn_3.grid(column=2, row=0)
btn_4 = Button(window, text="复制负面tag", command=copt_ne)
btn_4.grid(column=2, row=1)


window.mainloop()
