import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
from ttkthemes import ThemedTk
import database as db

class QuanLyTivi(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        self.pack(fill=tk.BOTH, expand=True)
        
      
        self.current_action = "idle" 

       
        title_font = tkFont.Font(family="Arial", size=18, weight="bold")
       
        title_label = ttk.Label(self, text="QUẢN LÝ CỬA HÀNG TI VI", 
                                font=title_font, anchor=tk.CENTER)
       
        title_label.pack(pady=10)
     
        input_frame = ttk.LabelFrame(self, text="Thông tin Ti Vi")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)

       
        ttk.Label(input_frame, text="Mã TV:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ma_tv_entry = ttk.Entry(input_frame, state="readonly") 
        self.ma_tv_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Tên Ti Vi:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ten_tv_entry = ttk.Entry(input_frame)
        self.ten_tv_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Hãng sản xuất:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.hang_sx_combo = ttk.Combobox(input_frame, values=["Sony", "Samsung", "LG", "TCL", "Panasonic", "Sharp", "Xiaomi", "Khác"])
        self.hang_sx_combo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Model:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.model_entry = ttk.Entry(input_frame)
        self.model_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Giá bán (VNĐ):").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.gia_ban_entry = ttk.Entry(input_frame)
        self.gia_ban_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Số lượng tồn:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.so_luong_spin = ttk.Spinbox(input_frame, from_=0, to=9999)
        self.so_luong_spin.grid(row=2, column=3, padx=5, pady=5, sticky="ew")


     
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=5, pady=10)

        self.them_btn = ttk.Button(button_frame, text="Thêm", command=self.them_moi)
        self.them_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.luu_btn = ttk.Button(button_frame, text="Lưu", command=self.luu, state="disabled")
        self.luu_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.sua_btn = ttk.Button(button_frame, text="Sửa", command=self.sua, state="disabled")
        self.sua_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.huy_btn = ttk.Button(button_frame, text="Hủy", command=self.huy, state="disabled")
        self.huy_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.xoa_btn = ttk.Button(button_frame, text="Xóa", command=self.xoa, state="disabled")
        self.xoa_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.thoat_btn = ttk.Button(button_frame, text="Thoát", command=self.thoat)
        self.thoat_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

      
        tree_frame = ttk.LabelFrame(self, text="Danh sách Ti Vi")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ('ma_tv', 'ten_tv', 'hang_sx', 'model', 'gia_ban', 'ton_kho')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

      
        self.tree.heading('ma_tv', text='Mã TV')
        self.tree.heading('ten_tv', text='Tên Ti Vi')
        self.tree.heading('hang_sx', text='Hãng')
        self.tree.heading('model', text='Model')
        self.tree.heading('gia_ban', text='Giá bán')
        self.tree.heading('ton_kho', text='Tồn kho')

   
        self.tree.column('ma_tv', width=60, anchor=tk.CENTER)
        
       
        self.tree.column('ten_tv', width=250)
        self.tree.column('hang_sx', width=100)
        self.tree.column('model', width=100)
        
       
        self.tree.column('gia_ban', width=120, anchor=tk.E) 
        
        self.tree.column('ton_kho', width=80, anchor=tk.CENTER)
      
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

      
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)

       
        self.load_data()

    

    def on_item_select(self, event):
        """Khi người dùng chọn một mục trên TreeView, điền thông tin lên các ô entry"""
        selected_item_id = self.tree.focus() 
        if not selected_item_id:
            return
            
        item = self.tree.item(selected_item_id, 'values')
        
        self.clear_form() 
        
        self.ma_tv_entry.config(state="normal")
        self.ma_tv_entry.insert(0, item[0]) 
        self.ma_tv_entry.config(state="readonly")
        
        self.ten_tv_entry.insert(0, item[1]) 
        self.hang_sx_combo.set(item[2])      
        self.model_entry.insert(0, item[3])  
        
        gia_ban_str = str(item[4]).replace(",", "")
        self.gia_ban_entry.insert(0, gia_ban_str)
        
        self.so_luong_spin.set(item[5]) 
        
        self.sua_btn.config(state="normal")
        self.xoa_btn.config(state="normal")
        self.huy_btn.config(state="normal")
        self.luu_btn.config(state="disabled") 
        self.them_btn.config(state="disabled") 
        self.current_action = "idle" 

    def clear_form(self):
        """Xóa trắng các ô nhập liệu"""
        self.ma_tv_entry.config(state="normal")
        self.ma_tv_entry.delete(0, tk.END)
        self.ma_tv_entry.config(state="readonly")
        
        self.ten_tv_entry.delete(0, tk.END)
        self.hang_sx_combo.set("")
        self.model_entry.delete(0, tk.END)
        self.gia_ban_entry.delete(0, tk.END)
        self.so_luong_spin.set(0)
        self.ten_tv_entry.focus() 
    
    def reset_buttons(self):
        """Đặt lại trạng thái các nút (như ban đầu)"""
        self.sua_btn.config(state="disabled")
        self.xoa_btn.config(state="disabled")
        self.huy_btn.config(state="disabled")
        self.luu_btn.config(state="disabled")
        self.them_btn.config(state="normal") 
        self.current_action = "idle"

    def load_data(self):
        """Lấy dữ liệu từ CSDL và hiển thị lên TreeView"""
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        data = db.lay_danh_sach_tivi() 
        
        if data:
            for item in data:
                gia_ban_formatted = f"{item['gia_ban']:,.0f}"
                
                self.tree.insert('', tk.END, values=(
                    item['id_tv'],
                    item['ten_tv'],
                    item['hang_san_xuat'],
                    item['model'],
                    gia_ban_formatted, 
                    item['so_luong_ton']
                ))

    def them_moi(self):
        """Kích hoạt trạng thái thêm mới"""
        self.clear_form() 
        self.luu_btn.config(state="normal")
        self.huy_btn.config(state="normal")
        self.them_btn.config(state="disabled")
        self.sua_btn.config(state="disabled")
        self.xoa_btn.config(state="disabled")
        self.current_action = "adding" 

    def sua(self):
        """Kích hoạt trạng thái sửa (khi đã chọn 1 item)"""
        self.luu_btn.config(state="normal")
        self.huy_btn.config(state="normal")
        self.them_btn.config(state="disabled")
        self.sua_btn.config(state="disabled")
        self.xoa_btn.config(state="disabled")
        self.current_action = "editing" 

    def luu(self):
        """Lưu (Thêm mới hoặc Cập nhật) vào CSDL"""
        try:
            ten_tv = self.ten_tv_entry.get()
            hang_sx = self.hang_sx_combo.get()
            model = self.model_entry.get()
            gia_ban = float(self.gia_ban_entry.get().replace(",", ""))
            so_luong = int(self.so_luong_spin.get()) 
        except ValueError:
            messagebox.showerror("Lỗi", "Giá bán và Số lượng phải là số.")
            return

        if not ten_tv or not hang_sx or not model:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ Tên, Hãng, và Model.")
            return

        success = False
        if self.current_action == "adding":
            success = db.them_tivi(ten_tv, hang_sx, model, gia_ban, so_luong)
            if success:
                messagebox.showinfo("Thành công", "Đã thêm Ti Vi mới thành công.")
            
        elif self.current_action == "editing":
            try:
                id_tv = int(self.ma_tv_entry.get())
            except ValueError:
                messagebox.showerror("Lỗi", "Không tìm thấy Mã TV để sửa.")
                return
                
            success = db.sua_tivi(id_tv, ten_tv, hang_sx, model, gia_ban, so_luong)
            if success:
                messagebox.showinfo("Thành công", "Đã cập nhật Ti Vi thành công.")
        
        if success:
            self.load_data() 
            self.clear_form()
            self.reset_buttons()
        else:
            messagebox.showerror("Lỗi", "Thao tác CSDL thất bại.\nKiểm tra xem Model này đã tồn tại chưa.")


    def huy(self):
        """Hủy thao tác (thêm/sửa), xóa trắng form và reset nút"""
        self.clear_form()
        self.reset_buttons()
        selected_item = self.tree.focus()
        if selected_item:
            self.tree.selection_remove(selected_item)

    def xoa(self):
        """Xóa Ti Vi đang được chọn"""
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một Ti Vi để xóa.")
            return
        
        item_values = self.tree.item(selected_item_id, 'values')
        id_tv = item_values[0]
        ten_tv = item_values[1]
        
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa Ti Vi '{ten_tv}' (ID: {id_tv}) không?"):
            
            success = db.xoa_tivi(id_tv)
            
            if success:
                messagebox.showinfo("Thành công", f"Đã xóa Ti Vi: {ten_tv}")
                self.load_data() 
                self.clear_form()
                self.reset_buttons()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa Ti Vi.\nLỗi này thường xảy ra khi Ti Vi này đã có trong một Hóa đơn.")

    def thoat(self):
        """Thoát ứng dụng"""
        if messagebox.askyesno("Thoát", "Bạn có muốn thoát ứng dụng không?"):
            self.master.destroy() 


if __name__ == "__main__":
    root = ThemedTk(theme="arc") 
    root.title("Quản lý Cửa hàng Ti Vi")
    
   
    window_width = 900
    window_height = 600
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    root.resizable(False, False) 
    
    root.withdraw() 

    conn = db.create_connection() 
    
    if conn:
        conn.close()
        app = QuanLyTivi(root)
        root.deiconify()
        root.mainloop()
    else:
        root.destroy()