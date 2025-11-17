import pyodbc
from tkinter import messagebox

# ----- CẤU HÌNH KẾT NỐI -----
# (Hãy thay đổi các thông số này cho phù hợp với máy của bạn)

SERVER = '.\QUOCHUNG'         # Hoặc tên server của bạn, ví dụ: .\SQLEXPRESS
DATABASE = 'quanly_tivi'
DRIVER = 'SQL Server'      # Driver bạn đã cài. 
                             # Phổ biến là 'SQL Server' 
                             # hoặc 'ODBC Driver 17 for SQL Server'

# Tạo chuỗi kết nối (connection string)
# Dùng Trusted_Connection=yes nếu bạn đăng nhập SQL Server bằng tài khoản Windows
# Nếu dùng tài khoản (user/pass) của SQL Server, hãy thay bằng:
# 'UID=your_username;PWD=your_password'
CONNECTION_STRING = f"""
    DRIVER={{{DRIVER}}};
    SERVER={SERVER};
    DATABASE={DATABASE};
    Trusted_Connection=yes;
"""

def create_connection():
    """Tạo và trả về một đối tượng kết nối CSDL"""
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '28000':
            messagebox.showerror("Lỗi kết nối", "Lỗi xác thực. Kiểm tra lại Username/Password hoặc Trusted_Connection.")
        elif sqlstate == '08001':
            messagebox.showerror("Lỗi kết nối", "Không tìm thấy Server hoặc Driver. Kiểm tra lại tên Server và Driver.")
        elif sqlstate == '42000':
             messagebox.showerror("Lỗi kết nối", f"Không tìm thấy Database '{DATABASE}'.")
        else:
            messagebox.showerror("Lỗi kết nối", f"Lỗi: {ex}")
        return None
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi không xác định: {e}")
        return None

def fetch_all(query, params=None):
    """Chạy lệnh SELECT và trả về TẤT CẢ các hàng (dưới dạng list of dicts)"""
    conn = create_connection()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        # Chuyển đổi kết quả (list of tuples) sang (list of dicts)
        # để dễ dàng sử dụng hơn
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
            
        return results
        
    except pyodbc.Error as e:
        messagebox.showerror("Lỗi truy vấn", f"Lỗi fetch: {e}")
        return []
    finally:
        if conn:
            conn.close()

def execute_query(query, params=None):
    """Chạy lệnh (INSERT, UPDATE, DELETE) và trả về True/False"""
    conn = create_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit() # Rất quan trọng: commit để lưu thay đổi
        return True
    except pyodbc.Error as e:
        conn.rollback() # Hoàn tác nếu có lỗi
        messagebox.showerror("Lỗi truy vấn", f"Lỗi execute: {e}")
        return False
    finally:
        if conn:
            conn.close()

# ----- CÁC HÀM NGHIỆP VỤ (GỌI TỪ GIAO DIỆN) -----

def lay_danh_sach_tivi():
    """Lấy toàn bộ TV từ CSDL"""
    query = "SELECT id_tv, ten_tv, hang_san_xuat, model, gia_ban, so_luong_ton FROM tivi"
    return fetch_all(query)

def them_tivi(ten_tv, hang_sx, model, gia_ban, so_luong):
    """Thêm một TV mới vào CSDL"""
    query = """
    INSERT INTO tivi (ten_tv, hang_san_xuat, model, gia_ban, so_luong_ton)
    VALUES (?, ?, ?, ?, ?)
    """
    # pyodbc dùng dấu ? làm tham số
    params = (ten_tv, hang_sx, model, gia_ban, so_luong)
    return execute_query(query, params)

def sua_tivi(id_tv, ten_tv, hang_sx, model, gia_ban, so_luong):
    """Cập nhật thông tin một TV dựa vào ID"""
    query = """
    UPDATE tivi
    SET ten_tv = ?, hang_san_xuat = ?, model = ?, gia_ban = ?, so_luong_ton = ?
    WHERE id_tv = ?
    """
    params = (ten_tv, hang_sx, model, gia_ban, so_luong, id_tv)
    return execute_query(query, params)

def xoa_tivi(id_tv):
    """Xóa một TV khỏi CSDL dựa vào ID"""
    query = "DELETE FROM tivi WHERE id_tv = ?"
    params = (id_tv,)
    return execute_query(query, params)