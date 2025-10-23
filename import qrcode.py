import json
import os
from datetime import datetime
import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# File data
USERS_FILE = 'users.json'
ORDERS_FILE = 'orders.json'

# Simpan user login global
current_user = None

# Produk data lengkap
products = {
    "Herbal": [
        {
            "name": "Minyak Herbal Sinergi",
            "price": 45000,
            "description": "Melegakan pernapasan saat asma, meredakan pegal linu dan nyeri sendi, serta mengobati luka memar dan terkena air panas.",
            "image": "minyak herbal sinergi.png"
        },
        {
            "name": "Gamat Kapsul",
            "price": 130000,
            "description": "Membantu meringankan gejala wasir dan memelihara kesehatan tubuh.",
            "image": "gamat.png"
        },
        {
            "name": "Diabextrac",
            "price": 130000,
            "description": "Membantu meringankan gejala diabetes.",
            "image": "diabextrac.png"
        },
        {
            "name": "Magafit",
            "price": 90000,
            "description": "Membantu memelihara kesehatan fungsi saluran pencernaan.",
            "image": "magafit.png"
        },
        {
            "name": "Langsingin",
            "price": 120000,
            "description": "Membantu mengurangi lemak dan menurunkan berat badan.",
            "image": "langsingin.png"
        }
    ],
    "Kesehatan": [
        {
            "name": "HNI Coffee",
            "price": 125000,
            "description": "Membantu meningkatkan stamina dan energi.",
            "image": "hni coffe (1).png"
        },
        {
            "name": "Realco Ginseng Coffee",
            "price": 65000,
            "description": "Membantu meningkatkan stamina dan energi dengan kandungan ginseng.",
            "image": "realco gingseng coffe.png"
        },
        {
            "name": "Sari Kurma",
            "price": 50000,
            "description": "Membantu memelihara kesehatan tubuh dan menambah energi.",
            "image": "sari kurma.png"
        },
        {
            "name": "Susu Bubuk Full Cream",
            "price": 75000,
            "description": "Membantu memenuhi kebutuhan nutrisi tubuh.",
            "image": "susu bubuk.png"
        }
    ],
    "Kecantikan": [
        {
            "name": "Sabun Kolagen",
            "price": 25000,
            "description": "Membantu membersihkan kulit tubuh dan melembabkan.",
            "image": "sabun kolagen.png"
        },
        {
            "name": "Sabun Madu",
            "price": 20000,
            "description": "Membantu membersihkan kulit tubuh dan melembabkan dengan kandungan madu.",
            "image": "sabun madu.png"
        },
        {
            "name": "Day Cream",
            "price": 75000,
            "description": "Membantu melindungi kulit dari efek buruk sinar matahari.",
            "image": "daycream.png"
        },
        {
            "name": "Night Cream",
            "price": 85000,
            "description": "Membantu melembabkan kulit dan membuatnya tetap sehat.",
            "image": "night cream.png"
        }
    ],
    "Kesehatan Wanita": [
        {
            "name": "Harumi",
            "price": 70000,
            "description": "Membantu memelihara kesehatan kewanitaan dan mengurangi lendir yang berlebihan.",
            "image": "harumi.png"
        },
        {
            "name": "Hibis",
            "price": 225000,
            "description": "Membantu memelihara kesehatan kewanitaan dan membuat tubuh tetap sehat.",
            "image": "hibis.png"
        }
    ]
}

# Fungsi simpan dan load data
def load_json_file(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)
    with open(filename, 'r') as f:
        return json.load(f)

def save_json_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
# Sambungan kode dari data dan fungsi load/save
# ... (lanjutan dari kode Anda)

# --- Variabel Global Aplikasi GUI ---
cart = {}  # Keranjang belanja: {product_name: quantity}
product_images = {} # Untuk menyimpan referensi gambar agar tidak hilang (garbage collected)

# --- FUNGSI UTILITAS ---

def format_rupiah(angka):
    """Mengubah angka menjadi format Rupiah."""
    return f"Rp.{angka:,.0f}".replace(",", ".")

def generate_qr_code(pesanan_data, order_id):
    """Membuat dan menyimpan QR Code dari data pesanan."""
    filename = f"QR_Pesanan_{order_id}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(pesanan_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{filename}.png")
    return f"{filename}.png"

def clear_frame(frame):
    """Menghapus semua widget dari sebuah frame."""
    for widget in frame.winfo_children():
        widget.destroy()

def load_all_data():
    """Memuat semua data dari file JSON saat aplikasi dimulai."""
    global users_data, orders_data
    users_data = load_json_file(USERS_FILE)
    orders_data = load_json_file(ORDERS_FILE)

# --- FUNGSI UTAMA TKINTER ---

class HNIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Pemesanan Produk HNI")
        self.geometry("800x600")
        
        load_all_data() # Muat data saat startup

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LoginPage, CatalogPage, CartPage, CheckoutPage, HistoryPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        """Menampilkan halaman (frame) yang diminta."""
        frame = self.frames[page_name]
        frame.tkraise()
        # Panggil fungsi refresh jika ada
        if hasattr(frame, 'refresh_content'):
            frame.refresh_content()

# --- HALAMAN LOGIN/REGISTRASI ---

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Halaman Login / Registrasi", font=('Arial', 18, 'bold')).pack(pady=20)

        # Frame untuk input
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Email:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = tk.Entry(input_frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Kata Sandi:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = tk.Entry(input_frame, width=30, show='*')
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Nama (Regis):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self, text="LOGIN", command=self.login).pack(pady=5)
        tk.Button(self, text="REGISTRASI", command=self.register).pack(pady=5)

    def login(self):
        global current_user, users_data
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email in users_data and users_data[email]['password'] == password:
            current_user = users_data[email]
            messagebox.showinfo("Sukses", f"Selamat datang, {current_user['name']}!")
            self.controller.show_frame("CatalogPage")
        else:
            messagebox.showerror("Error", "Email atau Kata Sandi salah!")

    def register(self):
        global users_data
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not name or not email or not password:
            messagebox.showerror("Error", "Semua kolom harus diisi untuk registrasi.")
            return

        if email in users_data:
            messagebox.showerror("Error", "Email sudah terdaftar. Silakan login.")
            return

        users_data[email] = {'name': name, 'email': email, 'password': password, 'orders': []}
        save_json_file(USERS_FILE, users_data)
        messagebox.showinfo("Sukses", "Registrasi berhasil! Silakan Login.")
        self.name_entry.delete(0, tk.END) # Bersihkan field nama setelah registrasi

# --- HALAMAN KATALOG PRODUK ---

class CatalogPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Frame Menu Atas
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(menu_frame, text="Keranjang", command=lambda: controller.show_frame("CartPage")).pack(side='right', padx=5)
        tk.Button(menu_frame, text="Riwayat", command=lambda: controller.show_frame("HistoryPage")).pack(side='right', padx=5)
        tk.Button(menu_frame, text="Logout", command=self.logout).pack(side='right', padx=5)
        
        tk.Label(menu_frame, text="KATALOG PRODUK HNI", font=('Arial', 16, 'bold')).pack(side='left')

        # Notebook (Tab) untuk kategori
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.load_catalog()

    def load_catalog(self):
        """Membuat tab untuk setiap kategori dan memuat produk."""
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
            
        for category, product_list in products.items():
            tab_frame = tk.Frame(self.notebook, padx=10, pady=10)
            self.notebook.add(tab_frame, text=category)
            
            # Canvas dan Scrollbar untuk setiap tab
            canvas = tk.Canvas(tab_frame)
            scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Muat Produk dalam Scrollable Frame
            self.display_products(scrollable_frame, product_list)

    def display_products(self, frame, product_list):
        """Menampilkan daftar produk dalam sebuah frame."""
        for i, product in enumerate(product_list):
            item_frame = tk.Frame(frame, relief=tk.RIDGE, borderwidth=1, padx=5, pady=5)
            item_frame.pack(fill='x', pady=5)

            # --- Kolom 1: Gambar ---
            try:
                img_path = product['image']
                original_img = Image.open(img_path)
                resized_img = original_img.resize((50, 50))
                photo_img = ImageTk.PhotoImage(resized_img)
                
                # Simpan referensi gambar agar tidak hilang
                product_images[product['name']] = photo_img 
                
                img_label = tk.Label(item_frame, image=photo_img)
                img_label.grid(row=0, column=0, rowspan=2, padx=10)
            except FileNotFoundError:
                tk.Label(item_frame, text="No Image", width=8).grid(row=0, column=0, rowspan=2, padx=10)
            except Exception as e:
                print(f"Error loading image {product['image']}: {e}")
                tk.Label(item_frame, text="Error Load", width=8).grid(row=0, column=0, rowspan=2, padx=10)

            # --- Kolom 2: Info Produk ---
            tk.Label(item_frame, text=product['name'], font=('Arial', 10, 'bold'), anchor='w').grid(row=0, column=1, sticky='w')
            tk.Label(item_frame, text=format_rupiah(product['price']), font=('Arial', 10), fg='green', anchor='w').grid(row=1, column=1, sticky='w')
            
            # --- Kolom 3: Deskripsi ---
            tk.Label(item_frame, text=product['description'][:60] + '...', wraplength=300, justify='left').grid(row=0, column=2, rowspan=2, padx=10, sticky='w')

            # --- Kolom 4: Tombol Beli ---
            tk.Button(item_frame, text="Tambah ke Keranjang", command=lambda p=product: self.add_to_cart(p)).grid(row=0, column=3, rowspan=2, padx=10)
            
            # Tambahkan info detail produk
            tk.Button(item_frame, text="Detail", command=lambda p=product: self.show_detail(p)).grid(row=1, column=3, padx=10)


    def show_detail(self, product):
        """Menampilkan detail produk dalam window baru."""
        detail_window = tk.Toplevel(self.controller)
        detail_window.title(product['name'])
        detail_window.geometry("400x300")
        
        tk.Label(detail_window, text=product['name'], font=('Arial', 14, 'bold')).pack(pady=10)
        tk.Label(detail_window, text=format_rupiah(product['price']), fg='green').pack()
        tk.Label(detail_window, text=product['description'], wraplength=380, justify='left').pack(padx=10, pady=10)
        tk.Button(detail_window, text="Tutup", command=detail_window.destroy).pack(pady=10)

    def add_to_cart(self, product):
        """Menambahkan produk ke keranjang belanja."""
        name = product['name']
        
        # Ambil input jumlah
        quantity = simpledialog.askinteger("Jumlah Pesanan", f"Masukkan jumlah {name}:", initialvalue=1, minvalue=1)
        
        if quantity is not None:
            if name in cart:
                cart[name]['quantity'] += quantity
            else:
                cart[name] = {'product': product, 'quantity': quantity}
            
            messagebox.showinfo("Sukses", f"{quantity}x {name} ditambahkan ke keranjang.")
        
    def logout(self):
        global current_user, cart
        current_user = None
        cart.clear()
        messagebox.showinfo("Logout", "Anda berhasil Logout.")
        self.controller.show_frame("LoginPage")

# --- HALAMAN KERANJANG BELANJA ---

class CartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="KERANJANG BELANJA", font=('Arial', 18, 'bold')).pack(pady=10)
        
        self.cart_frame = tk.Frame(self)
        self.cart_frame.pack(fill='both', expand=True, padx=10)
        
        self.total_label = tk.Label(self, text="", font=('Arial', 14, 'bold'), fg='blue')
        self.total_label.pack(pady=10)
        
        tk.Button(self, text="Lanjut ke Checkout", command=self.go_to_checkout).pack(side='left', padx=10, pady=10)
        tk.Button(self, text="Kembali ke Katalog", command=lambda: controller.show_frame("CatalogPage")).pack(side='right', padx=10, pady=10)

    def refresh_content(self):
        """Memuat ulang isi keranjang setiap kali halaman dibuka."""
        clear_frame(self.cart_frame)
        
        if not cart:
            tk.Label(self.cart_frame, text="Keranjang Anda kosong.").pack(pady=50)
            self.total_label.config(text="")
            return

        total_price = 0
        
        # Header
        header_frame = tk.Frame(self.cart_frame)
        header_frame.pack(fill='x', pady=5)
        ttk.Label(header_frame, text="Produk", width=30, font=('Arial', 10, 'bold')).pack(side='left')
        ttk.Label(header_frame, text="Harga", width=15, font=('Arial', 10, 'bold')).pack(side='left')
        ttk.Label(header_frame, text="Jumlah", width=10, font=('Arial', 10, 'bold')).pack(side='left')
        ttk.Label(header_frame, text="Subtotal", width=18, font=('Arial', 10, 'bold')).pack(side='left')
        
        # Daftar Item
        for item_name, item_data in cart.items():
            product = item_data['product']
            quantity = item_data['quantity']
            subtotal = product['price'] * quantity
            total_price += subtotal
            
            item_frame = tk.Frame(self.cart_frame)
            item_frame.pack(fill='x', pady=2)
            
            tk.Label(item_frame, text=item_name, width=30, anchor='w').pack(side='left')
            tk.Label(item_frame, text=format_rupiah(product['price']), width=15, anchor='w').pack(side='left')
            
            # Tombol +/- untuk mengubah jumlah
            tk.Button(item_frame, text="-", command=lambda name=item_name: self.update_quantity(name, -1)).pack(side='left', padx=2)
            tk.Label(item_frame, text=str(quantity), width=4).pack(side='left')
            tk.Button(item_frame, text="+", command=lambda name=item_name: self.update_quantity(name, 1)).pack(side='left', padx=2)
            
            tk.Label(item_frame, text=format_rupiah(subtotal), width=18, anchor='w', font=('Arial', 10, 'bold')).pack(side='left')
            tk.Button(item_frame, text="Hapus", fg='red', command=lambda name=item_name: self.remove_item(name)).pack(side='left', padx=5)

        self.total_label.config(text=f"TOTAL PEMBAYARAN: {format_rupiah(total_price)}")

    def update_quantity(self, item_name, delta):
        """Mengubah jumlah produk di keranjang."""
        new_quantity = cart[item_name]['quantity'] + delta
        
        if new_quantity <= 0:
            self.remove_item(item_name)
        else:
            cart[item_name]['quantity'] = new_quantity
            self.refresh_content()

    def remove_item(self, item_name):
        """Menghapus item dari keranjang."""
        del cart[item_name]
        messagebox.showinfo("Hapus Item", f"{item_name} berhasil dihapus dari keranjang.")
        self.refresh_content()

    def go_to_checkout(self):
        if not cart:
            messagebox.showwarning("Keranjang Kosong", "Silakan tambahkan produk ke keranjang terlebih dahulu.")
            return
        self.controller.show_frame("CheckoutPage")
        
# --- HALAMAN CHECKOUT ---

class CheckoutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Label(self, text="CHECKOUT PEMESANAN", font=('Arial', 18, 'bold')).pack(pady=10)
        
        self.total_frame = tk.Frame(self)
        self.total_frame.pack(pady=10)
        self.label_total_pembayaran = tk.Label(self.total_frame, text="", font=('Arial', 14, 'bold'), fg='red')
        self.label_total_pembayaran.pack()

        # Metode Pembayaran
        tk.Label(self, text="Pilih Metode Pembayaran:", font=('Arial', 12)).pack(pady=10)
        self.payment_method = tk.StringVar(self)
        self.payment_method.set("E-Wallet") # Default
        
        tk.Radiobutton(self, text="E-Wallet (OVO/Gopay/Dana)", variable=self.payment_method, value="E-Wallet").pack(anchor='w', padx=20)
        tk.Radiobutton(self, text="Transfer Bank (BCA/Mandiri)", variable=self.payment_method, value="Transfer Bank").pack(anchor='w', padx=20)
        
        tk.Button(self, text="KONFIRMASI & BAYAR", command=self.confirm_order).pack(pady=20)
        tk.Button(self, text="Kembali ke Keranjang", command=lambda: controller.show_frame("CartPage")).pack(pady=5)

    def refresh_content(self):
        """Hitung ulang total dan tampilkan."""
        self.total_bayar = sum(item['product']['price'] * item['quantity'] for item in cart.values())
        self.label_total_pembayaran.config(text=f"Total Bayar: {format_rupiah(self.total_bayar)}")

    def confirm_order(self):
        global current_user, users_data, orders_data, cart
        
        if not cart:
            messagebox.showerror("Error", "Keranjang kosong! Tidak bisa checkout.")
            self.controller.show_frame("CartPage")
            return
            
        metode = self.payment_method.get()
        order_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Format item untuk penyimpanan
        items_for_save = [{'name': item['product']['name'], 'price': item['product']['price'], 'quantity': item['quantity']} for item in cart.values()]
        
        # Data untuk QR Code
        qr_data = f"ID:{order_id}|User:{current_user['name']}|Total:{self.total_bayar}|Metode:{metode}"
        qr_filename = generate_qr_code(qr_data, order_id)

        # Objek Pesanan
        order = {
            'order_id': order_id,
            'user_email': current_user['email'],
            'date': datetime.now().strftime("%d-%m-%Y %H:%M"),
            'total': self.total_bayar,
            'method': metode,
            'items': items_for_save,
            'status': 'Menunggu Pembayaran',
            'qr_file': qr_filename
        }
        
        # Simpan ke data global dan file
        orders_data[order_id] = order
        save_json_file(ORDERS_FILE, orders_data)
        
        # Tambahkan ke riwayat user (opsional, tapi bagus untuk struktur data)
        if current_user['email'] in users_data:
            users_data[current_user['email']]['orders'].append(order_id)
            save_json_file(USERS_FILE, users_data)

        # Bersihkan keranjang
        cart.clear()
        
        messagebox.showinfo("Sukses Pesanan", 
                            f"Pesanan #{order_id} berhasil dibuat!\n"
                            f"Total: {format_rupiah(self.total_bayar)}\n"
                            f"Pembayaran via: {metode}\n"
                            f"Kode QR sudah tersimpan sebagai: {qr_filename}")
                            
        self.controller.show_frame("HistoryPage")
        
# --- HALAMAN RIWAYAT PEMESANAN ---

class HistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="RIWAYAT PEMESANAN", font=('Arial', 18, 'bold')).pack(pady=10)
        
        self.history_frame = tk.Frame(self)
        self.history_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        tk.Button(self, text="Kembali ke Katalog", command=lambda: controller.show_frame("CatalogPage")).pack(pady=10)

    def refresh_content(self):
        """Memuat ulang riwayat pesanan user saat halaman dibuka."""
        clear_frame(self.history_frame)
        
        if not current_user:
            tk.Label(self.history_frame, text="Silakan login terlebih dahulu.").pack(pady=50)
            return

        user_orders = [orders_data[oid] for oid in current_user.get('orders', []) if oid in orders_data]
        
        if not user_orders:
            tk.Label(self.history_frame, text="Anda belum memiliki riwayat pemesanan.").pack(pady=50)
            return

        # Header
        header_frame = tk.Frame(self.history_frame, relief=tk.SUNKEN, borderwidth=1)
        header_frame.pack(fill='x', pady=5)
        
        ttk.Label(header_frame, text="ID Pesanan", width=15, font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        ttk.Label(header_frame, text="Tanggal", width=15, font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        ttk.Label(header_frame, text="Total", width=15, font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        ttk.Label(header_frame, text="Metode", width=15, font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        ttk.Label(header_frame, text="Status", width=15, font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        for order in user_orders:
            order_frame = tk.Frame(self.history_frame, relief=tk.RIDGE, borderwidth=1)
            order_frame.pack(fill='x', pady=2)
            
            tk.Label(order_frame, text=order['order_id'], width=15, anchor='w').pack(side='left', padx=5)
            tk.Label(order_frame, text=order['date'].split(' ')[0], width=15, anchor='w').pack(side='left', padx=5)
            tk.Label(order_frame, text=format_rupiah(order['total']), width=15, anchor='w', fg='blue').pack(side='left', padx=5)
            tk.Label(order_frame, text=order['method'], width=15, anchor='w').pack(side='left', padx=5)
            tk.Label(order_frame, text=order['status'], width=15, anchor='w', fg='orange').pack(side='left', padx=5)
            
            # Tombol untuk melihat detail QR Code
            tk.Button(order_frame, text="Lihat QR", command=lambda o=order: self.show_qr_code(o['qr_file'])).pack(side='right', padx=5)

    def show_qr_code(self, qr_file):
        """Menampilkan QR Code dalam window baru."""
        qr_window = tk.Toplevel(self.controller)
        qr_window.title("Kode QR Pesanan")
        qr_window.geometry("300x320")
        
        try:
            original_img = Image.open(qr_file)
            resized_img = original_img.resize((250, 250))
            photo_img = ImageTk.PhotoImage(resized_img)
            
            # Label untuk gambar
            img_label = tk.Label(qr_window, image=photo_img)
            img_label.image = photo_img # Simpan referensi
            img_label.pack(pady=10)
            
            tk.Label(qr_window, text=f"File: {qr_file}", font=('Arial', 8)).pack()
        except FileNotFoundError:
            tk.Label(qr_window, text="File QR Code tidak ditemukan.", fg='red').pack(pady=50)

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Inisialisasi data global (di luar kelas)
    users_data = {}
    orders_data = {}
    
    app = HNIApp()
    app.mainloop()