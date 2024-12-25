import tkinter as tk
from tkinter import messagebox
import json


class UserManager:
    def __init__(self):
        self.users = self.load_users()
        self.pending_registrations = self.load_pending_registrations()
        self.default_admin = {
            "username": "admin",
            "password": "admin123",
            "address": "上海市闵行区",
            "contact": "15223395662",
            "role": "admin",
            "is_approved": True
        }
        if not any(user["username"] == self.default_admin["username"] for user in self.users):
            self.users.append(self.default_admin)
            self.save_users()

    def load_users(self):
        try:
            with open('users.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def load_pending_registrations(self):
        try:
            with open('pending_registrations.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_pending_registrations(self):
        with open('pending_registrations.json', 'w', encoding='utf-8') as file:
            json.dump(self.pending_registrations, file, ensure_ascii=False, indent=4)

    def save_users(self):
        with open('users.json', 'w', encoding='utf-8') as file:
            json.dump(self.users, file, ensure_ascii=False, indent=4)

    def register_user(self, username, password, address, contact):
        for user in self.users:
            if user["username"] == username:
                return False
        new_registration = {
            "username": username,
            "password": password,
            "address": address,
            "contact": contact,
            "role": "user",
            "is_approved": False
        }
        self.pending_registrations.append(new_registration)
        self.save_pending_registrations()
        return True

    def approve_registration(self, username):
        for registration in self.pending_registrations:
            if registration["username"] == username:
                self.pending_registrations.remove(registration)
                registration["is_approved"] = True
                self.users.append(registration)
                self.save_users()
                self.save_pending_registrations()
                return True
        return False

    def login_user(self, username, password):
        for user in self.users:
            if user["username"] == username and user["password"] == password:
                return True
        return False



class ItemManager:
    def __init__(self):
        self.user_manager = UserManager()
        self.items = []
        self.load_items()
        self.item_types = self.load_item_types()
        self.root = tk.Tk()
        self.root.title("物品复活软件")

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="用户名：").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="密码：").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="登录", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.register_button = tk.Button(self.login_frame, text="注册", command=self.show_register_frame)
        self.register_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.admin_frame = None

    def load_item_types(self):
        try:
            with open('item_types.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return [
                {"name": "食品", "attributes": ["保质期", "数量"]},
                {"name": "书籍", "attributes": ["作者", "出版社"]},
                {"name": "工具", "attributes": []}
            ]

    def save_item_types(self):
        with open('item_types.json', 'w', encoding='utf-8') as file:
            json.dump(self.item_types, file, ensure_ascii=False, indent=4)

    def show_register_frame(self):
        self.login_frame.pack_forget()
        self.register_frame = tk.Frame(self.root)
        self.register_frame.pack(pady=20)

        tk.Label(self.register_frame, text="用户名：").grid(row=0, column=0)
        self.reg_username_entry = tk.Entry(self.register_frame)
        self.reg_username_entry.grid(row=0, column=1)

        tk.Label(self.register_frame, text="密码：").grid(row=1, column=0)
        self.reg_password_entry = tk.Entry(self.register_frame, show="*")
        self.reg_password_entry.grid(row=1, column=1)

        tk.Label(self.register_frame, text="住址：").grid(row=2, column=0)
        self.reg_address_entry = tk.Entry(self.register_frame)
        self.reg_address_entry.grid(row=2, column=1)

        tk.Label(self.register_frame, text="联系方式：").grid(row=3, column=0)
        self.reg_contact_entry = tk.Entry(self.register_frame)
        self.reg_contact_entry.grid(row=3, column=1)

        self.register_submit_button = tk.Button(self.register_frame, text="注册", command=self.register)
        self.register_submit_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.back_to_login_button = tk.Button(self.register_frame, text="返回登录", command=self.show_login_frame)
        self.back_to_login_button.grid(row=5, column=0, columnspan=2, pady=10)

    def show_login_frame(self):
        self.register_frame.pack_forget()
        self.login_frame.pack(pady=20)

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        address = self.reg_address_entry.get()
        contact = self.reg_contact_entry.get()
        if self.user_manager.register_user(username, password, address, contact):
            messagebox.showinfo("成功", "注册成功，请等待审核。")
            self.show_login_frame()
        else:
            messagebox.showerror("错误", "用户名已存在，请重新输入。")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.login_user(username, password):
            messagebox.showinfo("成功", "登录成功。")
            self.login_frame.pack_forget()
            if username == "admin":
                self.show_admin_frame()
            else:
                self.show_user_function_frames()
            self.create_item_management_widgets()
        else:
            messagebox.showerror("错误", "用户名或密码错误，请重新输入。")

    def show_admin_frame(self):
        if self.admin_frame is None:
            self.admin_frame = tk.Frame(self.root)
            self.admin_frame.pack(pady=20)

            tk.Label(self.admin_frame, text="待审批用户列表：").grid(row=0, column=0)
            self.pending_listbox = tk.Listbox(self.admin_frame)
            self.pending_listbox.grid(row=1, column=0, columnspan=2)

            self.update_pending_list()

            self.approve_button = tk.Button(self.admin_frame, text="批准", command=self.approve_selected)
            self.approve_button.grid(row=2, column=0, pady=10)

            self.new_type_button = tk.Button(self.admin_frame, text="设置新物品类型", command=self.show_new_type_frame)
            self.new_type_button.grid(row=3, column=0, pady=10)

            self.modify_type_button = tk.Button(self.admin_frame, text="修改物品类型", command=self.show_modify_type_frame)
            self.modify_type_button.grid(row=3, column=1, pady=10)

            self.back_button = tk.Button(self.admin_frame, text="返回", command=self.hide_admin_frame)
            self.back_button.grid(row=2, column=1, pady=10)

    def show_new_type_frame(self):
        new_type_frame = tk.Frame(self.root)
        new_type_frame.pack(pady=20)

        tk.Label(new_type_frame, text="新物品类型名称：").grid(row=0, column=0)
        self.new_type_name_entry = tk.Entry(new_type_frame)
        self.new_type_name_entry.grid(row=0, column=1)

        tk.Label(new_type_frame, text="属性（用逗号分隔）：").grid(row=1, column=0)
        self.new_type_attr_entry = tk.Entry(new_type_frame)
        self.new_type_attr_entry.grid(row=1, column=1)

        self.submit_new_type_button = tk.Button(new_type_frame, text="提交", command=self.submit_new_type)
        self.submit_new_type_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.back_to_admin_button = tk.Button(new_type_frame, text="返回", command=new_type_frame.pack_forget)

    def submit_new_type(self):
        new_type_name = self.new_type_name_entry.get()
        new_type_attr_str = self.new_type_attr_entry.get()
        new_type_attr = new_type_attr_str.split(',') if new_type_attr_str else []
        self.item_types.append({"name": new_type_name, "attributes": new_type_attr})
        self.save_item_types()
        messagebox.showinfo("成功", "新物品类型已添加。")
        self.show_admin_frame()

    def show_modify_type_frame(self):
        modify_type_frame = tk.Frame(self.root)
        modify_type_frame.pack(pady=20)

        tk.Label(modify_type_frame, text="物品名称：").grid(row=0, column=0)
        self.modify_item_name_entry = tk.Entry(modify_type_frame)
        self.modify_item_name_entry.grid(row=0, column=1)

        tk.Label(modify_type_frame, text="新物品类型：").grid(row=1, column=0)
        self.modify_type_var = tk.StringVar()
        self.modify_type_var.set("请选择")
        type_names = [item_type["name"] for item_type in self.item_types]
        self.modify_type_menu = tk.OptionMenu(modify_type_frame, self.modify_type_var, *type_names)
        self.modify_type_menu.grid(row=1, column=1)

        self.submit_modify_type_button = tk.Button(modify_type_frame, text="提交", command=self.submit_modify_type)
        self.submit_modify_type_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.back_to_admin_button = tk.Button(modify_type_frame, text="返回", command=modify_type_frame.pack_forget)

    def submit_modify_type(self):
        item_name = self.modify_item_name_entry.get()
        new_type = self.modify_type_var.get()
        for item in self.items:
            if item["name"] == item_name:
                item["category"] = new_type
                self.save_items()
                messagebox.showinfo("成功", "物品类型已修改。")
                self.show_admin_frame()
                return
        messagebox.showerror("错误", "未找到该物品。")

    def show_user_function_frames(self):
        user_function_frame = tk.Frame(self.root)
        user_function_frame.pack(pady=20)

        self.search_type_var = tk.StringVar()
        self.search_type_var.set("请选择")
        type_names = [item_type["name"] for item_type in self.item_types]
        tk.Label(user_function_frame, text="搜索物品类型：").grid(row=0, column=0)
        self.search_type_menu = tk.OptionMenu(user_function_frame, self.search_type_var, *type_names)
        self.search_type_menu.grid(row=0, column=1)

        tk.Label(user_function_frame, text="搜索关键字：").grid(row=1, column=0)
        self.search_keyword_entry = tk.Entry(user_function_frame)
        self.search_keyword_entry.grid(row=1, column=1)

        self.search_button = tk.Button(user_function_frame, text="搜索", command=self.search_user_items)
        self.search_button.grid(row=2, column=0, columnspan=2, pady=10)

    def search_user_items(self):
        search_type = self.search_type_var.get()
        keyword = self.search_keyword_entry.get()
        found_items = []
        for item in self.items:
            if item["category"] == search_type and (keyword in item["name"] or keyword in item["description"]):
                found_items.append(item)
        if found_items:
            item_info = ""
            for item in found_items:
                item_info += f"名称：{item['name']}\n描述：{item['description']}\n地址：{item['location']}\n手机：{item['phone']}\n邮箱：{item['email']}\n类别：{item['category']}\n\n"
            messagebox.showinfo("搜索结果", item_info)
        else:
            messagebox.showerror("错误", "未找到匹配的物品。")

    def update_pending_list(self):
        self.pending_listbox.delete(0, tk.END)
        for registration in self.user_manager.pending_registrations:
            self.pending_listbox.insert(tk.END, registration["username"])

    def approve_selected(self):
        selected_index = self.pending_listbox.curselection()
        if selected_index:
            selected_username = self.pending_listbox.get(selected_index)
            if self.user_manager.approve_registration(selected_username):
                self.update_pending_list()
                messagebox.showinfo("成功", f"{selected_username} 的注册已批准。")
            else:
                messagebox.showerror("错误", f"批准 {selected_username} 失败。")

    def hide_admin_frame(self):
        if self.admin_frame:
            self.admin_frame.pack_forget()

    def create_item_management_widgets(self):
        # 公共信息框架
        common_frame = tk.Frame(self.root)
        common_frame.pack(pady=10)

        tk.Label(common_frame, text="物品名称：").grid(row=0, column=0)
        self.item_name_entry = tk.Entry(common_frame)
        self.item_name_entry.grid(row=0, column=1)

        tk.Label(common_frame, text="物品说明：").grid(row=1, column=0)
        self.item_description_entry = tk.Entry(common_frame)
        self.item_description_entry.grid(row=1, column=1)

        tk.Label(common_frame, text="物品所在地址：").grid(row=2, column=0)
        self.location_entry = tk.Entry(common_frame)
        self.location_entry.grid(row=2, column=1)

        tk.Label(common_frame, text="联系人手机：").grid(row=3, column=0)
        self.phone_entry = tk.Entry(common_frame)
        self.phone_entry.grid(row=3, column=1)

        tk.Label(common_frame, text="邮箱：").grid(row=4, column=0)
        self.email_entry = tk.Entry(common_frame)
        self.email_entry.grid(row=4, column=1)

        # 类别选择框架
        category_frame = tk.Frame(self.root)
        category_frame.pack(pady=10)

        tk.Label(category_frame, text="物品类别：").grid(row=0, column=0)
        self.category_var = tk.StringVar()
        self.category_var.set("请选择")
        type_names = [item_type["name"] for item_type in self.item_types]
        self.category_menu = tk.OptionMenu(category_frame, self.category_var, *type_names)
        self.category_menu.grid(row=0, column=1)

        # 食品额外信息框架
        self.food_frame = tk.Frame(self.root)
        self.food_frame.pack(pady=10)

        tk.Label(self.food_frame, text="保质期：").grid(row=0, column=0)
        self.expiry_date_entry = tk.Entry(self.food_frame)
        self.expiry_date_entry.grid(row=0, column=1)

        tk.Label(self.food_frame, text="数量：").grid(row=1, column=0)
        self.quantity_entry = tk.Entry(self.food_frame)
        self.quantity_entry.grid(row=1, column=1)

        self.food_frame.pack_forget()

        # 书籍额外信息框架
        self.book_frame = tk.Frame(self.root)
        self.book_frame.pack(pady=10)

        tk.Label(self.book_frame, text="作者：").grid(row=0, column=0)
        self.author_entry = tk.Entry(self.book_frame)
        self.author_entry.grid(row=0, column=1)

        tk.Label(self.book_frame, text="出版社：").grid(row=1, column=0)
        self.publisher_entry = tk.Entry(self.book_frame)
        self.publisher_entry.grid(row=1, column=1)

        self.book_frame.pack_forget()

        # 工具额外信息框架（假设暂时无额外属性）
        self.tool_frame = tk.Frame(self.root)
        self.tool_frame.pack(pady=10)
        self.tool_frame.pack_forget()

        # 绑定类别选择事件
        self.category_var.trace("w", self.show_extra_fields)

        # 按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.add_button = tk.Button(button_frame, text="添加物品", command=self.add_item)
        self.add_button.grid(row=0, column=0, padx=10)

        self.delete_button = tk.Button(button_frame, text="删除物品", command=self.delete_item)
        self.delete_button.grid(row=0, column=1, padx=10)

        self.search_button = tk.Button(button_frame, text="查找物品", command=self.search_item)
        self.search_button.grid(row=0, column=2, padx=10)

        self.show_all_button = tk.Button(button_frame, text="显示物品列表", command=self.show_all_items)
        self.show_all_button.grid(row=0, column=3, padx=10)

    def show_extra_fields(self, *args):
        category = self.category_var.get()
        if category == "食品":
            self.food_frame.pack(pady=10)
            self.book_frame.pack_forget()
            self.tool_frame.pack_forget()
        elif category == "书籍":
            self.book_frame.pack(pady=10)
            self.food_frame.pack_forget()
            self.tool_frame.pack_forget()
        elif category == "工具":
            self.tool_frame.pack(pady=10)
            self.food_frame.pack_forget()
            self.book_frame.pack_forget()

    def add_item(self):
        name = self.item_name_entry.get()
        description = self.item_description_entry.get()
        location = self.location_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        category = self.category_var.get()

        if not all([name, description, location, phone, email, category]):
            messagebox.showerror("错误", "请填写完整的公共信息和物品类别。")
            return

        item = {
            "name": name,
            "description": description,
            "location": location,
            "phone": phone,
            "email": email,
            "category": category
        }

        if category == "食品":
            expiry_date = self.expiry_date_entry.get()
            quantity = self.quantity_entry.get()
            if not all([expiry_date, quantity]):
                messagebox.showerror("错误", "请填写完整的食品额外信息。")
                return
            item["expiry_date"] = expiry_date
            item["quantity"] = quantity

        elif category == "书籍":
            author = self.author_entry.get()
            publisher = self.publisher_entry.get()
            if not all([author, publisher]):
                messagebox.showerror("错误", "请填写完整的书籍额外信息。")
                return
            item["author"] = author
            item["publisher"] = publisher

        self.items.append(item)
        self.save_items()
        messagebox.showinfo("成功", "物品信息已添加。")
        self.clear_entries()

    def delete_item(self):
        name_to_delete = self.item_name_entry.get()
        for item in self.items:
            if item["name"] == name_to_delete:
                self.items.remove(item)
                self.save_items()
                messagebox.showinfo("成功", "物品信息已删除。")
                self.clear_entries()
                return
        messagebox.showerror("错误", "未找到该物品。")

    def search_item(self):
        name_to_search = self.item_name_entry.get()
        for item in self.items:
            if item["name"] == name_to_search:
                item_info = f"名称：{item['name']}\n描述：{item['description']}\n地址：{item['location']}\n手机：{item['phone']}\n邮箱：{item['email']}\n类别：{item['category']}"
                if item["category"] == "食品":
                    item_info += f"\n保质期：{item['expiry_date']}\n数量：{item['quantity']}"
                elif item["category"] == "书籍":
                    item_info += f"\n作者：{item['author']}\n出版社：{item['publisher']}"
                messagebox.showinfo("物品信息", item_info)
                return
        messagebox.showerror("错误", "未找到该物品。")

    def show_all_items(self):
        if not self.items:
            messagebox.showinfo("物品列表", "无物品信息。")
        else:
            item_list_window = tk.Toplevel(self.root)
            item_list_window.title("物品列表")

            text_widget = tk.Text(item_list_window)
            text_widget.pack(pady=10)

            for item in self.items:
                item_info = f"名称：{item['name']}\n描述：{item['description']}\n地址：{item['location']}\n手机：{item['phone']}\n邮箱：{item['email']}\n类别：{item['category']}"
                if item["category"] == "食品":
                    item_info += f"\n保质期：{item['expiry_date']}\n数量：{item['quantity']}"
                elif item["category"] == "书籍":
                    item_info += f"\n作者：{item['author']}\n出版社：{item['publisher']}"
                text_widget.insert(tk.END, item_info + "\n\n")
            text_widget.config(state=tk.DISABLED)

    def clear_entries(self):
        self.item_name_entry.delete(0, tk.END)
        self.item_description_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.category_var.set("请选择")
        self.expiry_date_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.publisher_entry.delete(0, tk.END)

    def load_items(self):
        try:
            with open('items.json', 'r', encoding='utf-8') as file:
                self.items = json.load(file)
        except FileNotFoundError:
            self.items = []

    def save_items(self):
        with open('items.json', 'w', encoding='utf-8') as file:
            json.dump(self.items, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    item_manager = ItemManager()
    item_manager.root.mainloop()