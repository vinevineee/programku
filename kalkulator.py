def tambah(x, y):
    """Menambahkan dua angka"""
    return x + y

def kurang(x, y):
    """Mengurangi dua angka"""
    return x - y

def kali(x, y):
    """Mengalikan dua angka"""
    return x * y

def bagi(x, y):
    """Membagi dua angka"""
    if y == 0:
        return "Error: Tidak bisa membagi dengan 0"
    return x / y

def kalkulator():
    """Program kalkulator interaktif"""
    print("=" * 40)
    print("        KALKULATOR SEDERHANA")
    print("=" * 40)
    
    while True:
        print("\nPilihan operasi:")
        print("1. Penjumlahan (+)")
        print("2. Pengurangan (-)")
        print("3. Perkalian (*)")
        print("4. Pembagian (/)")
        print("5. Keluar")
        
        pilihan = input("\nMasukkan pilihan (1/2/3/4/5): ")
        
        if pilihan == '5':
            print("\nTerima kasih telah menggunakan kalkulator!")
            break
        
        if pilihan in ['1', '2', '3', '4']:
            try:
                angka1 = float(input("Masukkan angka pertama: "))
                angka2 = float(input("Masukkan angka kedua: "))
                
                if pilihan == '1':
                    hasil = tambah(angka1, angka2)
                    print(f"\n{angka1} + {angka2} = {hasil}")
                
                elif pilihan == '2':
                    hasil = kurang(angka1, angka2)
                    print(f"\n{angka1} - {angka2} = {hasil}")
                
                elif pilihan == '3':
                    hasil = kali(angka1, angka2)
                    print(f"\n{angka1} × {angka2} = {hasil}")
                
                elif pilihan == '4':
                    hasil = bagi(angka1, angka2)
                    print(f"\n{angka1} ÷ {angka2} = {hasil}")
                    
            except ValueError:
                print("\nError: Masukkan angka yang valid!")
        else:
            print("\nPilihan tidak valid. Silakan coba lagi!")

if __name__ == "__main__":
    kalkulator()
