import sqlite3

def create_db():
    conn = sqlite3.connect('omborn.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS mahsulotlar
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nom TEXT NOT NULL,
                  kategoriya TEXT,
                  olcham TEXT,
                  miqdor REAL DEFAULT 0,
                  narx REAL DEFAULT 0,
                  min_miqdor REAL DEFAULT 5)''')
    c.execute('''CREATE TABLE IF NOT EXISTS harakatlar
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  mahsulot_id INTEGER,
                  tur TEXT,
                  miqdor REAL,
                  izoh TEXT,
                  sana TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def mahsulot_qosh(nom, kategoriya, olcham, miqdor, narx):
    conn = sqlite3.connect('omborn.db')
    c = conn.cursor()
    c.execute("INSERT INTO mahsulotlar (nom,kategoriya,olcham,miqdor,narx) VALUES (?,?,?,?,?)",
              (nom, kategoriya, olcham, miqdor, narx))
    conn.commit()
    conn.close()

def mahsulotlar_royxat():
    conn = sqlite3.connect('omborn.db')
    c = conn.cursor()
    c.execute("SELECT * FROM mahsulotlar ORDER BY kategoriya")
    data = c.fetchall()
    conn.close()
    return data

def kirim(mahsulot_id, miqdor, izoh):
    conn = sqlite3.connect('omborn.db')
    c = conn.cursor()
    c.execute("UPDATE mahsulotlar SET miqdor=miqdor+? WHERE id=?", (miqdor, mahsulot_id))
    c.execute("INSERT INTO harakatlar (mahsulot_id,tur,miqdor,izoh) VALUES (?,?,?,?)",
              (mahsulot_id, 'kirim', miqdor, izoh))
    conn.commit()
    conn.close()

def chiqim(mahsulot_id, miqdor, izoh):
    conn = sqlite3.connect('omborn.db')
    c = conn.cursor()
    c.execute("UPDATE mahsulotlar SET miqdor=miqdor-? WHERE id=?", (miqdor, mahsulot_id))
    c.execute("INSERT INTO harakatlar (mahsulot_id,tur,miqdor,izoh) VALUES (?,?,?,?)",
              (mahsulot_id, 'chiqim', miqdor, izoh))
    conn.commit()
    conn.close()

def harakatlar_tarixi():
    conn = sqlite3.connect('omborn.db')
    c = conn.cursor()
    c.execute('''SELECT h.sana, m.nom, h.tur, h.miqdor, h.izoh
                 FROM harakatlar h JOIN mahsulotlar m ON h.mahsulot_id=m.id
                 ORDER BY h.sana DESC LIMIT 20''')
    data = c.fetchall()
    conn.close()
    return data

def kam_qolganlar():
    conn = sqlite3.connect('omborn.db')
    c = conn.cursor()
    c.execute("SELECT * FROM mahsulotlar WHERE miqdor <= min_miqdor")
    data = c.fetchall()
    conn.close()
    return data
