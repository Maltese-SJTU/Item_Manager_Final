import tkinter as tk
from tkinter import messagebox

class ItemManager:
    def __init__(self):
        self.items = []
        self.root = tk.Tk()
        self.root.title("物品复活软件")

        # 标签和输入框
        tk.Label(self.root, text="物品名称：").grid(row=0, column=0)
        self.item_name_entry = tk.Entry(self.root)
        self.item_name_entry.grid(row=0, column=1)

        tk.Label(self.root, text="物品描述：").grid(row=1, column=0)
        self.item_description_entry = tk.Entry(self.root)
        self.item_description_entry.grid(row=1, column=1)

        tk.Label(self.root, text="联系人信息：").grid(row=2, column=0)
        self.contact_info_entry = tk.Entry(self.root)
        self.contact_info_entry.grid(row=2, column=1)

        # 按钮
        self.add_button = tk.Button(self.root, text="添加物品", command=self.add_item)
        self.add_button.grid(row=3, column=0)

        self.delete_button = tk.Button(self.root, text="删除物品", command=self.delete_item)
        self.delete_button.grid(row=3, column=1)

        self.search_button = tk.Button(self.root, text="查找物品", command=self.search_item)
        self.search_button.grid(row=4, column=0)

        self.show_all_button = tk.Button(self.root, text="显示物品列表", command=self.show_all_items)
        self.show_all_button.grid(row=4, column=1)

    def add_item(self):
        name = self.item_name_entry.get()
        description = self.item_description_entry.get()
        contact_info = self.contact_info_entry.get()
        if name and description and contact_info:
            self.items.append({"name": name, "description": description, "contact_info": contact_info})
            messagebox.showinfo("成功", "物品信息已添加。")
            self.clear_entries()
        else:
            messagebox.showerror("错误", "请填写完整的物品信息。")

    def delete_item(self):
        name_to_delete = self.item_name_entry.get()
        for item in self.items:
            if item["name"] == name_to_delete:
                self.items.remove(item)
                messagebox.showinfo("成功", "物品信息已删除。")
                self.clear_entries()
                return
        messagebox.showerror("错误", "未找到该物品。")

    def search_item(self):
        name_to_search = self.item_name_entry.get()
        for item in self.items:
            if item["name"] == name_to_search:
                messagebox.showinfo("物品信息", f"名称：{item['name']}\n描述：{item['description']}\n联系人信息：{item['contact_info']}")
                return
        messagebox.showerror("错误", "未找到该物品。")

    def show_all_items(self):
        if not self.items:
            messagebox.showinfo("物品列表", "无物品信息。")
        else:
            all_items_text = ""
            for item in self.items:
                all_items_text += f"名称：{item['name']}\n描述：{item['description']}\n联系人信息：{item['contact_info']}\n\n"
            messagebox.showinfo("物品列表", all_items_text)

    def clear_entries(self):
        self.item_name_entry.delete(0, tk.END)
        self.item_description_entry.delete(0, tk.END)
        self.contact_info_entry.delete(0, tk.END)

if __name__ == "__main__":
    item_manager = ItemManager()
    item_manager.root.mainloop()
